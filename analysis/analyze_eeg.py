from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"

VHDR = DATA / "S3practica.vhdr"
VMRK = DATA / "S3practica.vmrk"
EEG = DATA / "S3practica.eeg"
SCORING = DATA / "S3PRACTICA.txt"

FS = 250
N_CHANNELS = 10
RESOLUTION_UV = 0.1
EPOCH_SEC = 30
CHANNELS = ["EOG I", "EOG D", "F3", "F4", "C3", "C4", "P3", "P4", "EMGI", "EMGD"]
STAGE_LABELS = {
    0: "0 - Vigilia/no sueno/artefacto probable",
    1: "1 - N1 probable",
    2: "2 - N2 probable",
    3: "3 - N3/SWS probable",
}
STAGE_SHORT = {0: "Vigilia", 1: "N1", 2: "N2", 3: "N3/SWS"}
STAGE_COLORS = {0: "#9aa6b2", 1: "#7aa6c2", 2: "#4f83b8", 3: "#243b63"}
BANDS = {
    "delta_0.5_4": (0.5, 4),
    "theta_4_8": (4, 8),
    "alpha_8_12": (8, 12),
    "sigma_12_15": (12, 15),
    "beta_15_30": (15, 30),
}


@dataclass(frozen=True)
class Marker:
    description: str
    sample: int
    seconds: float


def load_scoring() -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(SCORING, dtype=int)
    return data[:, 0], data[:, 1]


def load_signal() -> np.ndarray:
    raw = np.fromfile(EEG, dtype="<i2")
    if raw.size % N_CHANNELS != 0:
        raise ValueError(f"Unexpected EEG size: {raw.size} int16 values for {N_CHANNELS} channels")
    return raw.reshape(-1, N_CHANNELS).astype(np.float32) * RESOLUTION_UV


def parse_markers() -> list[Marker]:
    markers: list[Marker] = []
    for line in VMRK.read_text(encoding="utf-8").splitlines():
        if not line.startswith("Mk"):
            continue
        _, payload = line.split("=", 1)
        parts = payload.split(",")
        if len(parts) < 3:
            continue
        description = parts[1] or parts[0]
        sample = int(parts[2])
        markers.append(Marker(description=description, sample=sample, seconds=(sample - 1) / FS))
    return markers


def contiguous_runs(stages: np.ndarray) -> list[tuple[int, int, int, float]]:
    runs: list[tuple[int, int, int, float]] = []
    start = 0
    for idx in range(1, len(stages) + 1):
        if idx == len(stages) or stages[idx] != stages[start]:
            runs.append((int(stages[start]), start + 1, idx, (idx - start) * EPOCH_SEC / 60))
            start = idx
    return runs


def band_power(freq: np.ndarray, power: np.ndarray, low: float, high: float) -> float:
    mask = (freq >= low) & (freq < high)
    if not np.any(mask):
        return float("nan")
    return float(np.trapezoid(power[mask], freq[mask]))


def compute_band_table(signal_uv: np.ndarray, stages: np.ndarray) -> list[dict[str, float | str]]:
    scored_samples = len(stages) * EPOCH_SEC * FS
    c3 = signal_uv[:scored_samples, CHANNELS.index("C3")]
    c4 = signal_uv[:scored_samples, CHANNELS.index("C4")]
    eeg = (c3 + c4) / 2
    rows: list[dict[str, float | str]] = []

    for code in sorted(set(stages)):
        mask_epochs = stages == code
        samples: list[np.ndarray] = []
        for epoch_idx, include in enumerate(mask_epochs):
            if include:
                start = epoch_idx * EPOCH_SEC * FS
                end = start + EPOCH_SEC * FS
                samples.append(eeg[start:end])
        if not samples:
            continue
        stage_signal = np.concatenate(samples)
        freq, psd = signal.welch(stage_signal, fs=FS, nperseg=FS * 4, noverlap=FS * 2)
        row: dict[str, float | str] = {
            "codigo": int(code),
            "interpretacion": STAGE_SHORT[int(code)],
            "duracion_min": float(mask_epochs.sum() * EPOCH_SEC / 60),
        }
        total = band_power(freq, psd, 0.5, 30)
        for name, (low, high) in BANDS.items():
            absolute = band_power(freq, psd, low, high)
            row[f"{name}_uv2"] = absolute
            row[f"{name}_pct"] = absolute / total * 100 if total else float("nan")
        rows.append(row)
    return rows


def save_hypnogram(stages: np.ndarray, markers: list[Marker]) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "2026-06-11_eeg_hipnograma_v1.png"
    epoch_time_min = np.arange(len(stages)) * EPOCH_SEC / 60

    fig, ax = plt.subplots(figsize=(12, 4.2))
    y = np.array([3 - s for s in stages])
    ax.step(epoch_time_min, y, where="post", color="#243b63", linewidth=1.8)
    ax.fill_between(epoch_time_min, y, 3, step="post", color="#d9e4f2", alpha=0.8)

    n3_epochs = np.where(stages == 3)[0]
    if n3_epochs.size:
        ax.axvspan(n3_epochs.min() * EPOCH_SEC / 60, (n3_epochs.max() + 1) * EPOCH_SEC / 60, color="#f4b860", alpha=0.22, label="Tramo N3/SWS probable")

    for marker in markers:
        if marker.description.upper() in {"LUZ OFF", "LUZ ON"}:
            ax.axvline(marker.seconds / 60, color="#9d4edd", linestyle="--", linewidth=1)
            ax.text(marker.seconds / 60 + 0.4, -0.18, marker.description, rotation=90, va="bottom", fontsize=8, color="#5a189a")

    ax.set_yticks([3, 2, 1, 0], ["Vigilia/0", "N1/1", "N2/2", "N3/3"])
    ax.set_xlabel("Minutos desde inicio del registro")
    ax.set_ylabel("Scoring tentativo")
    ax.set_title("Hipnograma tentativo del dataset secundario con sueño", loc="left", fontsize=14, fontweight="bold")
    ax.grid(axis="x", color="#d8dde3", linewidth=0.8)
    ax.legend(loc="upper right", frameon=False)
    fig.text(0.01, 0.01, "Fuente: data/S3PRACTICA.txt y marcadores data/S3practica.vmrk. Codificacion tentativa, no estadificacion clinica.", fontsize=8, color="#475569")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def save_spectrogram(signal_uv: np.ndarray, stages: np.ndarray, markers: list[Marker]) -> Path:
    path = FIGURES / "2026-06-11_eeg_espectrograma_c3_c4_v1.png"
    scored_samples = len(stages) * EPOCH_SEC * FS
    c3 = signal_uv[:scored_samples, CHANNELS.index("C3")]
    c4 = signal_uv[:scored_samples, CHANNELS.index("C4")]
    eeg = (c3 + c4) / 2

    sos = signal.butter(4, [0.3, 35], btype="bandpass", fs=FS, output="sos")
    filtered = signal.sosfiltfilt(sos, eeg)
    freq, time_sec, spec = signal.spectrogram(
        filtered,
        fs=FS,
        window="hann",
        nperseg=FS * 8,
        noverlap=FS * 6,
        scaling="density",
        mode="psd",
    )
    mask = (freq >= 0.3) & (freq <= 35)
    spec_db = 10 * np.log10(spec[mask] + 1e-12)

    fig, ax = plt.subplots(figsize=(12, 4.8))
    im = ax.pcolormesh(time_sec / 60, freq[mask], spec_db, shading="auto", cmap="magma", vmin=np.percentile(spec_db, 5), vmax=np.percentile(spec_db, 97))
    ax.set_ylim(0.3, 35)
    ax.set_xlabel("Minutos desde inicio del registro")
    ax.set_ylabel("Frecuencia (Hz)")
    ax.set_title("Espectrograma EEG C3/C4 promedio", loc="left", fontsize=14, fontweight="bold")
    for marker in markers:
        if marker.description.upper() in {"LUZ OFF", "LUZ ON"}:
            ax.axvline(marker.seconds / 60, color="#e9d8fd", linestyle="--", linewidth=1)
            ax.text(marker.seconds / 60 + 0.4, 34, marker.description, rotation=90, va="top", fontsize=8, color="#ffffff")

    n3_epochs = np.where(stages == 3)[0]
    if n3_epochs.size:
        ax.axvspan(n3_epochs.min() * EPOCH_SEC / 60, (n3_epochs.max() + 1) * EPOCH_SEC / 60, color="#ffffff", alpha=0.10)
        ax.text(n3_epochs.min() * EPOCH_SEC / 60 + 0.5, 31, "N3/SWS probable", color="#ffffff", fontsize=9)

    cbar = fig.colorbar(im, ax=ax, pad=0.01)
    cbar.set_label("Potencia espectral (dB, uV^2/Hz)")
    fig.text(0.01, 0.01, "Fuente: data/S3practica.eeg + data/S3practica.vhdr. Filtro 0.3-35 Hz, espectrograma Welch/Hann.", fontsize=8, color="#475569")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def save_rhythm_table() -> Path:
    path = FIGURES / "2026-06-11_eeg_ritmos_v1.png"
    rows = [
        ("Delta", "0.5-4 Hz", "Mas prominente en N3/SWS", "Sueño de ondas lentas; recuperacion y consolidacion"),
        ("Theta", "4-8 Hz", "Transicion y sueño liviano", "Somnolencia/N1 y procesamiento mnemonico"),
        ("Alfa", "8-12 Hz", "Vigilia relajada, ojos cerrados", "Disminuye con sueño consolidado"),
        ("Sigma", "12-15 Hz", "Husos de sueño en N2", "Vinculo con consolidacion declarativa"),
        ("Beta", "15-30 Hz", "Activacion cortical/vigilia", "Puede aumentar con alerta o artefactos musculares"),
    ]
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.axis("off")
    table = ax.table(
        cellText=rows,
        colLabels=["Ritmo", "Banda", "Lectura EEG", "Relevancia para el TP"],
        loc="center",
        cellLoc="left",
        colLoc="left",
        colWidths=[0.12, 0.12, 0.28, 0.48],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor("#243b63")
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#f8fafc" if row % 2 else "#ffffff")
    ax.set_title("Ritmos EEG relevantes para interpretar sueño", loc="left", fontsize=14, fontweight="bold")
    fig.text(0.01, 0.01, "Fuente teorica local: Clase 9 EEG y clases de sueño/memoria del repo padre.", fontsize=8, color="#475569")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def save_delta_by_stage(band_rows: list[dict[str, float | str]]) -> Path:
    path = FIGURES / "2026-06-11_eeg_delta_por_scoring_v1.png"
    labels = [str(row["interpretacion"]) for row in band_rows]
    values = [float(row["delta_0.5_4_pct"]) for row in band_rows]
    colors = [STAGE_COLORS[int(row["codigo"])] for row in band_rows]
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.bar(labels, values, color=colors, width=0.58)
    ax.set_ylabel("Delta como % de potencia 0.5-30 Hz")
    ax.set_title("Potencia delta relativa por codigo de scoring", loc="left", fontsize=13, fontweight="bold")
    ax.grid(axis="y", color="#d8dde3", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", rotation=12)
    for i, val in enumerate(values):
        ax.text(i, val + 0.8, f"{val:.1f}%", ha="center", fontsize=9)
    fig.text(0.01, 0.01, "Fuente: potencia Welch sobre C3/C4 promedio por epocas scoreadas; interpretacion tentativa, no validacion clinica.", fontsize=8, color="#475569")
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def save_markdown(
    signal_uv: np.ndarray,
    stages: np.ndarray,
    flags: np.ndarray,
    markers: list[Marker],
    runs: list[tuple[int, int, int, float]],
    band_rows: list[dict[str, float | str]],
    figures: list[Path],
) -> Path:
    output = OUTPUTS / "2026-06-11_resultados-eeg_v1.md"
    duration_sec = signal_uv.shape[0] / FS
    scoring_duration_sec = len(stages) * EPOCH_SEC
    light_off = next((m for m in markers if m.description.upper() == "LUZ OFF"), None)
    light_on = next((m for m in markers if m.description.upper() == "LUZ ON"), None)
    n3_epochs = np.where(stages == 3)[0]

    stage_counts = Counter(stages.tolist())
    stage_rows = []
    for code in sorted(stage_counts):
        stage_rows.append(
            {
                "codigo": code,
                "interpretacion": STAGE_LABELS[code],
                "epocas": stage_counts[code],
                "minutos": stage_counts[code] * EPOCH_SEC / 60,
            }
        )

    runs_rows = [
        {"codigo": code, "desde_epoca": start, "hasta_epoca": end, "duracion_min": duration}
        for code, start, end, duration in runs
        if code == 3 or duration >= 3
    ]

    band_df = [
        {
            "codigo": row["codigo"],
            "interpretacion": row["interpretacion"],
            "duracion_min": row["duracion_min"],
            "delta_pct": row["delta_0.5_4_pct"],
            "theta_pct": row["theta_4_8_pct"],
            "alpha_pct": row["alpha_8_12_pct"],
            "sigma_pct": row["sigma_12_15_pct"],
            "beta_pct": row["beta_15_30_pct"],
        }
        for row in band_rows
    ]

    markers_md = "\n".join(
        f"| {m.description} | {m.sample} | {m.seconds:.2f} | {m.seconds/60:.2f} |" for m in markers
    )
    lines = [
        "# Resultados EEG/EOG/EMG - dataset secundario con sueño",
        "",
        "Fecha: 2026-06-11",
        "",
        "## Procedencia y alcance",
        "",
        "- Fuente fisiologica: `data/S3practica.vhdr`, `data/S3practica.eeg`, `data/S3practica.vmrk`.",
        "- Fuente de scoring/codificacion: `data/S3PRACTICA.txt`.",
        "- Estos datos se tratan como dataset secundario de una persona que si durmio. No corresponden al sujeto propio OpenBCI que no durmio.",
        "- La codificacion `0-3` se interpreta en forma tentativa porque no hay clave oficial adjunta.",
        "",
        "## Metadatos del registro",
        "",
        f"- Canales: {N_CHANNELS} (`{', '.join(CHANNELS)}`).",
        f"- Frecuencia de muestreo: {FS} Hz.",
        f"- Resolucion: {RESOLUTION_UV} uV por unidad INT16.",
        f"- Duracion del archivo EEG: {duration_sec:.2f} s ({duration_sec/60:.2f} min).",
        f"- Duracion cubierta por scoring: {scoring_duration_sec:.2f} s ({scoring_duration_sec/60:.2f} min).",
        "",
        "## Marcadores",
        "",
        "| Marcador | Muestra | Segundo | Minuto |",
        "|---|---:|---:|---:|",
        markers_md,
        "",
    ]
    if light_off and light_on:
        lines.extend(
            [
                f"- Luz apagada: {light_off.seconds:.2f} s ({light_off.seconds/60:.2f} min).",
                f"- Luz encendida: {light_on.seconds:.2f} s ({light_on.seconds/60:.2f} min).",
                f"- Intervalo luz off/on: {(light_on.seconds-light_off.seconds)/60:.2f} min.",
                "",
            ]
        )
    lines.extend(
        [
            "## Scoring tentativo",
            "",
            "| Codigo | Interpretacion tentativa | Epocas | Minutos |",
            "|---:|---|---:|---:|",
        ]
    )
    lines.extend(
        f"| {row['codigo']} | {row['interpretacion']} | {row['epocas']} | {row['minutos']:.1f} |"
        for row in stage_rows
    )
    lines.extend(
        [
            "",
            f"- Segunda columna de `S3PRACTICA.txt`: {Counter(flags.tolist())}. Se reporta como bandera/codificacion no interpretada.",
            "",
            "## Tramos relevantes",
            "",
            "| Codigo | Desde epoca | Hasta epoca | Duracion min |",
            "|---:|---:|---:|---:|",
        ]
    )
    lines.extend(
        f"| {row['codigo']} | {row['desde_epoca']} | {row['hasta_epoca']} | {row['duracion_min']:.1f} |"
        for row in runs_rows
    )
    if n3_epochs.size:
        start_min = n3_epochs.min() * EPOCH_SEC / 60
        end_min = (n3_epochs.max() + 1) * EPOCH_SEC / 60
        off_start = start_min - (light_off.seconds / 60 if light_off else 0)
        off_end = end_min - (light_off.seconds / 60 if light_off else 0)
        lines.extend(
            [
                "",
                f"- Tramo compatible con N3/SWS probable: {start_min:.1f}-{end_min:.1f} min desde inicio; {off_start:.1f}-{off_end:.1f} min desde luz off.",
                "- Formulacion recomendada: tramo compatible con sueño de ondas lentas probable, no estadificacion clinica definitiva.",
            ]
        )
    lines.extend(
        [
            "",
            "## Potencia por banda en C3/C4",
            "",
            "| Codigo | Interpretacion | Duracion min | Delta % | Theta % | Alfa % | Sigma % | Beta % |",
            "|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    lines.extend(
        f"| {row['codigo']} | {row['interpretacion']} | {row['duracion_min']:.1f} | {row['delta_pct']:.1f} | {row['theta_pct']:.1f} | {row['alpha_pct']:.1f} | {row['sigma_pct']:.1f} | {row['beta_pct']:.1f} |"
        for row in band_df
    )
    lines.extend(
        [
            "",
            "## Figuras",
            "",
        ]
    )
    for fig in figures:
        lines.append(f"- `outputs/figures/{fig.name}`")
    lines.extend(
        [
            "",
            "## Lectura prudente",
            "",
            "- El scoring secundario muestra una secuencia compatible con arquitectura de sueño NREM, con un bloque prolongado de codigo 3.",
            "- En C3/C4, el analisis espectral permite observar el peso de actividad lenta y ubicar el tramo compatible con ondas lentas.",
            "- Como la clave oficial de `S3PRACTICA.txt` no esta adjunta, la conclusion debe formularse como interpretacion fisiologica probable y no como diagnostico o estadificacion clinica.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main() -> None:
    stages, flags = load_scoring()
    signal_uv = load_signal()
    markers = parse_markers()
    runs = contiguous_runs(stages)
    band_rows = compute_band_table(signal_uv, stages)
    figures = [
        save_hypnogram(stages, markers),
        save_spectrogram(signal_uv, stages, markers),
        save_rhythm_table(),
        save_delta_by_stage(band_rows),
    ]
    md_path = save_markdown(signal_uv, stages, flags, markers, runs, band_rows, figures)
    print(f"wrote {md_path.relative_to(ROOT)}")
    for fig in figures:
        print(f"wrote {fig.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
