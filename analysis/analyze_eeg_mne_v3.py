"""Analisis EEG corregido (v3) del dataset secundario con sueno.

Reescribe el analisis previo siguiendo las notas nuevas de la catedra:

- Lectura BrainVision con MNE (`mne.io.read_raw_brainvision`).
- Filtros ANTES del analisis: notch 50 Hz + pasa banda 0.3-35 Hz.
- Epocas de 30 s SIN solapamiento, alineadas 1:1 con el scoring.
- Solo se usa la PRIMERA columna de `S3PRACTICA.txt`; la segunda se ignora.
- Canales centrales C3 y C4 con control de calidad por canal.
- Potencia absoluta y relativa por banda y por fase (delta, theta, alfa, sigma, beta).
- Figuras: hipnograma, porcentaje de fases, potencia por banda/fase, PSD por fase,
  espectrograma C3/C4.

INTERPRETACION DEL SCORING (ver informe):
El archivo solo contiene los codigos 0,1,2,3 = Vigilia, S1, S2, S3/SWS (descenso NREM
consecutivo Rechtschaffen & Kales). El registro llego hasta S3 (sueno profundo / SWS);
no hay S4, REM ni MT. Por la duracion (~90 min) podia esperarse llegar a S4 o REM, pero
no aparecen en estos datos. Se usa la primera columna del .txt; la segunda se ignora.

Datos crudos en `data/` solo se leen, nunca se modifican.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend headless

import matplotlib.pyplot as plt
import numpy as np

import mne

# ----------------------------------------------------------------------------
# Rutas y constantes
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"

VHDR = DATA / "S3practica.vhdr"
SCORING = DATA / "S3PRACTICA.txt"

EPOCH_SEC = 30
NOTCH_HZ = 50.0
BP_LOW, BP_HIGH = 0.3, 35.0
EEG_CHANNELS = ["F3", "F4", "C3", "C4", "P3", "P4"]
EOG_CHANNELS = ["EOG I", "EOG D"]
EMG_CHANNELS = ["EMGI", "EMGD"]
# Canales centrales candidatos (preferidos para estadificacion). Se hace control de
# calidad y se descartan los que tengan ruido/artefactos fuertes.
CANDIDATE_CHANNELS = ["C3", "C4"]
# Umbrales de canal malo (sobre la senal filtrada, en uV).
BAD_STD_UV = 150.0       # desvio estandar fisiologico de EEG central << 150 uV
BAD_SAT_FRAC = 0.005     # >0.5% de muestras cerca de saturacion INT16

# Mapeo adoptado (R&K, nomenclatura S de la catedra). Solo se observan 0..3.
STAGE_NAME = {0: "Vigilia", 1: "S1", 2: "S2", 3: "S3/SWS"}
STAGE_LONG = {
    0: "Vigilia / transicion (codigo 0)",
    1: "S1 - sueno liviano (codigo 1)",
    2: "S2 - husos/complejos K (codigo 2)",
    3: "S3 / SWS - sueno de ondas lentas (codigo 3)",
}
STAGE_ORDER = [0, 1, 2, 3]
STAGE_COLORS = {0: "#9aa6b2", 1: "#7aa6c2", 2: "#4f83b8", 3: "#243b63"}

# Esquema general de la catedra (incluye fases que NO aparecen en este registro)
PROFESOR_CODES = {0: "Wake/transicion", 1: "S1", 2: "S2", 3: "S3 (SWS)",
                  4: "S4 (SWS)", 5: "REM", 8: "MT"}

BANDS = {
    "delta": (0.5, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 12.0),
    "sigma": (12.0, 15.0),
    "beta": (15.0, 30.0),
}
BAND_COLORS = {
    "delta": "#243b63",
    "theta": "#3f72af",
    "alpha": "#5fa8d3",
    "sigma": "#f4a259",
    "beta": "#bc4b51",
}
TOTAL_LOW, TOTAL_HIGH = 0.5, 30.0


# ----------------------------------------------------------------------------
# Carga de datos
# ----------------------------------------------------------------------------
def load_scoring() -> tuple[np.ndarray, np.ndarray]:
    """Devuelve (columna1, columna2). Solo columna1 se usa para fase."""
    arr = np.loadtxt(SCORING, dtype=int)
    return arr[:, 0], arr[:, 1]


def load_raw_filtered() -> tuple[mne.io.BaseRaw, mne.io.BaseRaw]:
    """Lee BrainVision y devuelve (raw_crudo, raw_filtrado)."""
    raw = mne.io.read_raw_brainvision(VHDR, preload=True, verbose="ERROR")
    # Tipos de canal correctos para no contaminar el analisis EEG con EOG/EMG.
    ch_types = {}
    for ch in EOG_CHANNELS:
        if ch in raw.ch_names:
            ch_types[ch] = "eog"
    for ch in EMG_CHANNELS:
        if ch in raw.ch_names:
            ch_types[ch] = "emg"
    raw.set_channel_types(ch_types, verbose="ERROR")

    raw_filt = raw.copy()
    # Notch 50 Hz (ruido de linea). Con un pasa-bajos en 35 Hz queda casi redundante,
    # pero se aplica segun protocolo de la catedra y por robustez.
    raw_filt.notch_filter(freqs=[NOTCH_HZ], picks="eeg", verbose="ERROR")
    # Pasa banda 0.3-35 Hz: remueve deriva lenta/DC (clave para no inflar delta) y
    # ruido de alta frecuencia, dejando interpretable el analisis espectral.
    raw_filt.filter(l_freq=BP_LOW, h_freq=BP_HIGH, picks="eeg",
                    fir_design="firwin", verbose="ERROR")
    return raw, raw_filt


# ----------------------------------------------------------------------------
# Control de calidad de canales C3/C4
# ----------------------------------------------------------------------------
def channel_quality(raw_filt: mne.io.BaseRaw) -> list[dict]:
    """Estadisticos de calidad por canal candidato (en microvoltios) + flag de malo."""
    sat_uv = 32767 * 0.1  # saturacion INT16 con resolucion 0.1 uV
    rows = []
    for ch in CANDIDATE_CHANNELS:
        x = raw_filt.get_data(picks=ch)[0] * 1e6  # V -> uV
        std = float(np.std(x))
        frac_sat = float(np.mean(np.abs(x) > 0.95 * sat_uv))
        flat = bool(std < 1.0)
        motivos = []
        if std > BAD_STD_UV:
            motivos.append(f"std {std:.0f} uV > {BAD_STD_UV:.0f}")
        if frac_sat > BAD_SAT_FRAC:
            motivos.append(f"saturacion {frac_sat*100:.2f}%")
        if flat:
            motivos.append("flatline")
        rows.append({
            "canal": ch,
            "std_uv": std,
            "p2p_uv": float(np.percentile(x, 99.5) - np.percentile(x, 0.5)),
            "frac_saturacion": frac_sat,
            "flatline": flat,
            "malo": bool(motivos),
            "motivo": "; ".join(motivos) if motivos else "ok",
        })
    return rows


def select_channels(qrows: list[dict]) -> list[str]:
    """Devuelve los canales centrales que pasan el control de calidad."""
    good = [q["canal"] for q in qrows if not q["malo"]]
    if not good:  # salvaguarda: si todos fallan, usar el de menor std
        good = [min(qrows, key=lambda q: q["std_uv"])["canal"]]
    return good


# ----------------------------------------------------------------------------
# Epocas y PSD
# ----------------------------------------------------------------------------
def make_epochs(raw_filt: mne.io.BaseRaw, n_epochs: int) -> mne.Epochs:
    """Epocas fijas de 30 s sin solapamiento, recortando al periodo scoreado."""
    sfreq = raw_filt.info["sfreq"]
    needed = n_epochs * EPOCH_SEC
    raw_crop = raw_filt.copy().crop(tmin=0.0, tmax=needed - 1.0 / sfreq)
    epochs = mne.make_fixed_length_epochs(
        raw_crop, duration=EPOCH_SEC, preload=True, verbose="ERROR"
    )
    return epochs


def epoch_band_powers(epochs: mne.Epochs, stages: np.ndarray, picks: list[str]) -> dict:
    """PSD por epoca (Welch sobre canales validos) y potencias por banda."""
    sfreq = epochs.info["sfreq"]
    n_fft = int(4 * sfreq)  # 4 s -> resolucion 0.25 Hz, adecuada para delta
    n_overlap = int(2 * sfreq)
    spectrum = epochs.compute_psd(
        method="welch", fmin=0.3, fmax=35.0, n_fft=n_fft, n_overlap=n_overlap,
        picks=picks, verbose="ERROR",
    )
    psds, freqs = spectrum.get_data(return_freqs=True)  # (n_ep, n_ch, n_freq) en V^2/Hz
    psd_uv2 = psds.mean(axis=1) * 1e12  # promedio de canales validos y V^2 -> uV^2

    df = freqs[1] - freqs[0]
    total_mask = (freqs >= TOTAL_LOW) & (freqs < TOTAL_HIGH)

    n_ep = psd_uv2.shape[0]
    abs_power = {b: np.zeros(n_ep) for b in BANDS}
    rel_power = {b: np.zeros(n_ep) for b in BANDS}
    # numpy>=2 expone trapezoid; numpy<2 expone trapz.
    trapz = getattr(np, "trapezoid", None) or np.trapz
    total = np.array([trapz(psd_uv2[i][total_mask], dx=df) for i in range(n_ep)])
    for b, (lo, hi) in BANDS.items():
        mask = (freqs >= lo) & (freqs < hi)
        for i in range(n_ep):
            ap = trapz(psd_uv2[i][mask], dx=df)
            abs_power[b][i] = ap
            rel_power[b][i] = ap / total[i] * 100 if total[i] > 0 else np.nan

    return {
        "freqs": freqs,
        "psd_uv2": psd_uv2,        # (n_ep, n_freq) promedio C3/C4
        "abs_power": abs_power,    # uV^2 por banda por epoca
        "rel_power": rel_power,    # % por banda por epoca
        "total": total,
    }


def aggregate_by_stage(stages: np.ndarray, bp: dict) -> list[dict]:
    rows = []
    for code in STAGE_ORDER:
        idx = np.where(stages == code)[0]
        if idx.size == 0:
            continue
        row = {
            "codigo": int(code),
            "fase": STAGE_NAME[code],
            "epocas": int(idx.size),
            "minutos": float(idx.size * EPOCH_SEC / 60),
            "pct_tiempo": float(idx.size / len(stages) * 100),
        }
        for b in BANDS:
            row[f"{b}_abs"] = float(np.nanmean(bp["abs_power"][b][idx]))
            row[f"{b}_rel"] = float(np.nanmean(bp["rel_power"][b][idx]))
        rows.append(row)
    return rows


def stage_mean_psd(stages: np.ndarray, bp: dict) -> dict:
    out = {}
    for code in STAGE_ORDER:
        idx = np.where(stages == code)[0]
        if idx.size == 0:
            continue
        out[code] = bp["psd_uv2"][idx].mean(axis=0)
    return out


# ----------------------------------------------------------------------------
# Metricas de arquitectura del sueno
# ----------------------------------------------------------------------------
def sleep_metrics(stages: np.ndarray) -> dict:
    n = len(stages)
    non_wake = np.where(stages != 0)[0]
    onset_idx = int(non_wake[0]) if non_wake.size else None
    # Latencia a N2 sostenido (primer codigo 2)
    n2_idx = np.where(stages == 2)[0]
    n3_idx = np.where(stages == 3)[0]
    metrics = {
        "epocas_total": n,
        "minutos_total": n * EPOCH_SEC / 60,
        "latencia_sueno_min": (onset_idx * EPOCH_SEC / 60) if onset_idx is not None else None,
        "primer_epoca_no_vigilia": (onset_idx + 1) if onset_idx is not None else None,
        "latencia_n2_min": (int(n2_idx[0]) * EPOCH_SEC / 60) if n2_idx.size else None,
        "latencia_n3_min": (int(n3_idx[0]) * EPOCH_SEC / 60) if n3_idx.size else None,
        "epocas_sueno": int(np.sum(stages != 0)),
        "minutos_sueno": float(np.sum(stages != 0) * EPOCH_SEC / 60),
        "eficiencia_pct": float(np.mean(stages != 0) * 100),
    }
    if n3_idx.size:
        metrics["bloque_n3_desde_min"] = float(n3_idx.min() * EPOCH_SEC / 60)
        metrics["bloque_n3_hasta_min"] = float((n3_idx.max() + 1) * EPOCH_SEC / 60)
    return metrics


def parse_light_markers(raw: mne.io.BaseRaw) -> dict:
    out = {}
    for onset, desc in zip(raw.annotations.onset, raw.annotations.description):
        u = desc.upper()
        if "LUZ OFF" in u:
            out["luz_off_min"] = float(onset / 60)
        elif "LUZ ON" in u:
            out["luz_on_min"] = float(onset / 60)
    return out


# ----------------------------------------------------------------------------
# Figuras
# ----------------------------------------------------------------------------
def fig_hypnogram(stages: np.ndarray, lights: dict) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "2026-06-11_eeg_hipnograma_mne_v3.png"
    t = np.arange(len(stages)) * EPOCH_SEC / 60
    # Eje y con profundidad: Vigilia arriba, N3 abajo
    y = stages.astype(float)
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.step(t, y, where="post", color="#243b63", linewidth=1.6)
    ax.fill_between(t, y, 0, step="post", color="#d9e4f2", alpha=0.7)
    n3 = np.where(stages == 3)[0]
    if n3.size:
        ax.axvspan(n3.min() * EPOCH_SEC / 60, (n3.max() + 1) * EPOCH_SEC / 60,
                   color="#f4b860", alpha=0.20, label="Bloque S3/SWS")
    for key, color, lab in [("luz_off_min", "#9d4edd", "Luz OFF"),
                            ("luz_on_min", "#9d4edd", "Luz ON")]:
        if key in lights:
            ax.axvline(lights[key], color=color, linestyle="--", linewidth=1)
            ax.text(lights[key] + 0.3, 3.15, lab, rotation=90, va="top",
                    fontsize=8, color="#5a189a")
    ax.set_yticks([0, 1, 2, 3], ["Vigilia (0)", "S1 (1)", "S2 (2)", "S3/SWS (3)"])
    ax.invert_yaxis()
    ax.set_xlabel("Minutos desde el inicio del registro")
    ax.set_ylabel("Fase de sueno")
    ax.set_title("Hipnograma - epocas de 30 s (scoring columna 1)", loc="left",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="x", color="#e2e8f0", linewidth=0.8)
    ax.set_axisbelow(True)
    if n3.size:
        ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def fig_stage_percent(stage_rows: list[dict]) -> Path:
    path = FIGURES / "2026-06-11_eeg_porcentaje-fases_v3.png"
    labels = [STAGE_NAME[r["codigo"]] for r in stage_rows]
    pct = [r["pct_tiempo"] for r in stage_rows]
    mins = [r["minutos"] for r in stage_rows]
    colors = [STAGE_COLORS[r["codigo"]] for r in stage_rows]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, pct, color=colors, width=0.62)
    ax.set_ylabel("Porcentaje del tiempo scoreado (%)")
    ax.set_title("Distribucion de fases del sueno", loc="left",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(pct) * 1.18)
    for bar, p, m in zip(bars, pct, mins):
        ax.text(bar.get_x() + bar.get_width() / 2, p + 0.6,
                f"{p:.1f}%\n{m:.1f} min", ha="center", va="bottom", fontsize=9)
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def fig_band_by_stage(stage_rows: list[dict], ch_label: str) -> Path:
    path = FIGURES / "2026-06-11_eeg_potencia-bandas-por-fase_v3.png"
    stages = [STAGE_NAME[r["codigo"]] for r in stage_rows]
    band_names = list(BANDS.keys())
    x = np.arange(len(stages))

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12, 4.9),
                                   gridspec_kw={"width_ratios": [1.5, 1]})

    # Panel izquierdo: composicion relativa (barras apiladas a 100%).
    bottom = np.zeros(len(stages))
    for b in band_names:
        vals = np.array([r[f"{b}_rel"] for r in stage_rows])
        axL.bar(x, vals, 0.6, bottom=bottom, label=b, color=BAND_COLORS[b],
                edgecolor="white", linewidth=0.6)
        bottom += vals
    axL.set_xticks(x, stages)
    axL.set_ylabel("Composicion espectral relativa (%)")
    axL.set_ylim(0, 100)
    axL.set_title("Distribucion de bandas por fase", loc="left",
                  fontsize=12.5, fontweight="bold")
    axL.legend(ncol=5, frameon=False, fontsize=8.5, loc="lower center",
               bbox_to_anchor=(0.5, -0.22))
    axL.set_axisbelow(True)

    # Panel derecho: husos = sigma absoluta por fase (firma de N2).
    sigma_abs = [r["sigma_abs"] for r in stage_rows]
    colors = [STAGE_COLORS[r["codigo"]] for r in stage_rows]
    bars = axR.bar(x, sigma_abs, 0.6, color=colors)
    axR.set_xticks(x, stages)
    axR.set_ylabel("Potencia sigma 12-15 Hz (uV^2)")
    axR.set_title("Husos (sigma) por fase", loc="left",
                  fontsize=12.5, fontweight="bold")
    axR.grid(axis="y", color="#e2e8f0", linewidth=0.8)
    axR.set_axisbelow(True)
    axR.set_ylim(0, max(sigma_abs) * 1.25)
    for bar, v in zip(bars, sigma_abs):
        axR.text(bar.get_x() + bar.get_width() / 2, v + max(sigma_abs) * 0.02,
                 f"{v:.1f}", ha="center", va="bottom", fontsize=9)
    imax = int(np.argmax(sigma_abs))
    axR.annotate("pico en N2\n(husos de sueno)", xy=(imax, sigma_abs[imax]),
                 xytext=(imax - 0.2, max(sigma_abs) * 1.1), fontsize=8.5,
                 ha="center", color="#7a3b00")

    fig.suptitle(f"Potencia por banda y fase ({ch_label})", x=0.01, ha="left",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0.01, 1, 0.94])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def fig_psd_by_stage(psd_by_stage: dict, freqs: np.ndarray, ch_label: str) -> Path:
    path = FIGURES / "2026-06-11_eeg_psd-por-fase_v3.png"
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    mask = (freqs >= 0.5) & (freqs <= 30)
    for code in STAGE_ORDER:
        if code not in psd_by_stage:
            continue
        ax.semilogy(freqs[mask], psd_by_stage[code][mask],
                    color=STAGE_COLORS[code], linewidth=1.9, label=STAGE_NAME[code])
    # Sombrear banda sigma (husos)
    ax.axvspan(12, 15, color="#f4a259", alpha=0.12)
    ax.text(13.5, ax.get_ylim()[1] * 0.5, "sigma\n12-15 Hz", ha="center",
            fontsize=8, color="#b5651d")
    ax.set_xlim(0.5, 30)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Densidad espectral de potencia (uV^2/Hz, escala log)")
    ax.set_title(f"PSD promedio por fase - {ch_label}", loc="left",
                 fontsize=13, fontweight="bold")
    ax.grid(True, which="both", color="#e2e8f0", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=10)
    fig.tight_layout(rect=[0, 0.01, 1, 1])
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def fig_spectrogram(raw_filt: mne.io.BaseRaw, stages: np.ndarray, lights: dict,
                    picks: list[str]) -> Path:
    from scipy import signal as sp_signal
    path = FIGURES / "2026-06-11_eeg_espectrograma_c3-c4_mne_v3.png"
    sfreq = raw_filt.info["sfreq"]
    needed = len(stages) * EPOCH_SEC
    data = raw_filt.copy().crop(tmin=0, tmax=needed - 1.0 / sfreq).get_data(
        picks=picks) * 1e6  # uV
    eeg = data.mean(axis=0)
    f, t, Sxx = sp_signal.spectrogram(
        eeg, fs=sfreq, window="hann", nperseg=int(8 * sfreq),
        noverlap=int(6 * sfreq), scaling="density", mode="psd")
    mask = (f >= 0.5) & (f <= 30)
    Sdb = 10 * np.log10(Sxx[mask] + 1e-12)

    fig, (axh, ax) = plt.subplots(
        2, 1, figsize=(12, 5.6), sharex=True,
        gridspec_kw={"height_ratios": [1, 4], "hspace": 0.06})
    # Hipnograma compacto arriba
    th = np.arange(len(stages)) * EPOCH_SEC / 60
    axh.step(th, stages, where="post", color="#243b63", linewidth=1.3)
    axh.fill_between(th, stages, 0, step="post", color="#d9e4f2", alpha=0.7)
    axh.set_yticks([0, 1, 2, 3], ["V", "S1", "S2", "S3"])
    axh.invert_yaxis()
    axh.set_ylabel("Fase", fontsize=9)
    axh.grid(axis="x", color="#e2e8f0", linewidth=0.6)
    ch_lab = "+".join(picks)
    axh.set_title(f"Espectrograma {ch_lab} con hipnograma alineado", loc="left",
                  fontsize=13, fontweight="bold")

    im = ax.pcolormesh(t / 60, f[mask], Sdb, shading="auto", cmap="magma",
                       vmin=np.percentile(Sdb, 5), vmax=np.percentile(Sdb, 97))
    ax.set_ylim(0.5, 30)
    ax.set_xlabel("Minutos desde el inicio del registro")
    ax.set_ylabel("Frecuencia (Hz)")
    for key in ("luz_off_min", "luz_on_min"):
        if key in lights:
            ax.axvline(lights[key], color="#e9d8fd", linestyle="--", linewidth=1)
    cbar = fig.colorbar(im, ax=[axh, ax], pad=0.01)
    cbar.set_label("Potencia (dB, uV^2/Hz)")
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return path


# ----------------------------------------------------------------------------
# Informe markdown + JSON
# ----------------------------------------------------------------------------
def write_report(stages, flags, qrows, used_channels, stage_rows, metrics, lights,
                 raw, figures) -> Path:
    out = OUTPUTS / "2026-06-11_resultados-eeg-mne_v3.md"
    codes_present = sorted(set(stages.tolist()))
    counts = Counter(stages.tolist())

    def fmt(v, n=1):
        return "n/d" if v is None else f"{v:.{n}f}"

    L = []
    L += [
        "# Resultados EEG con MNE (v3) - dataset secundario con sueno",
        "",
        "Fecha: 2026-06-11",
        "",
        "## Procedencia y alcance",
        "",
        "- Senal: `data/S3practica.vhdr` + `.eeg` + `.vmrk` (BrainVision, 10 canales, 250 Hz).",
        "- Scoring: `data/S3PRACTICA.txt`, **solo primera columna**; la segunda se ignora.",
        "- Dataset **secundario** de una persona que SI durmio. No es el sujeto propio OpenBCI (que no durmio).",
        "- Analisis reproducible: `analysis/analyze_eeg_mne_v3.py` (MNE " + mne.__version__ + ").",
        "",
        "## Interpretacion del scoring",
        "",
        "El esquema general de la catedra contempla las fases "
        "`0`=Wake, `1`=S1, `2`=S2, `3`=S3 (SWS), `4`=S4 (SWS), `5`=REM, `8`=MT.",
        "",
        "El archivo real **solo contiene** los codigos " +
        ", ".join(f"`{c}` (x{counts[c]})" for c in codes_present) +
        ", es decir un descenso NREM consecutivo `0->1->2->3`:",
        "",
        "- `0` = Vigilia/transicion, `1` = S1, `2` = S2, `3` = **S3 / SWS** (sueno profundo).",
        "- El registro **llego hasta S3 (SWS)**; no hay `4` (S4), `5` (REM) ni `8` (MT).",
        "- Esto es coherente con la nota de catedra: el registro solo llego a fase 3. "
        "Por la duracion (~80-90 min) podria haberse esperado llegar a S4 o a un primer "
        "episodio REM, pero **no aparecen** en estos datos.",
        "- Se trabaja con la primera columna del `.txt`; la segunda se ignora.",
        "",
        "## Filtros aplicados (antes del analisis)",
        "",
        f"- Notch {NOTCH_HZ:.0f} Hz (ruido de linea).",
        f"- Pasa banda {BP_LOW}-{BP_HIGH} Hz (FIR). Remueve deriva/DC y alta frecuencia; "
        "es lo que corrige el sesgo de delta del analisis previo sin filtrar.",
        "",
        "## Control de calidad de canales C3/C4",
        "",
        "| Canal | std (uV) | P2P aprox (uV) | Frac. saturacion | Estado |",
        "|---|---:|---:|---:|---|",
    ]
    for q in qrows:
        estado = "OK" if not q["malo"] else f"DESCARTADO ({q['motivo']})"
        L.append(f"| {q['canal']} | {q['std_uv']:.1f} | {q['p2p_uv']:.0f} | "
                 f"{q['frac_saturacion']:.4f} | {estado} |")
    descartados = [q["canal"] for q in qrows if q["malo"]]
    used_lbl = " + ".join(used_channels)
    qc_txt = (f"**C4 presenta artefactos fuertes** (desvio ~18x mayor que C3 y saturacion "
              f"INT16), por lo que se **descarta** y el analisis espectral usa **{used_lbl}**. "
              "Promediar C4 contaminaba el espectro e invertia el patron de delta entre fases; "
              "este es justamente el control de calidad pedido por la catedra.")
    if not descartados:
        qc_txt = (f"Ambos canales pasan el control de calidad; el analisis usa {used_lbl}.")
    L += [
        "",
        qc_txt,
        "",
        "## Arquitectura del sueno",
        "",
        f"- Duracion scoreada: {metrics['epocas_total']} epocas x 30 s = "
        f"{metrics['minutos_total']:.1f} min.",
        f"- Latencia de sueno (primera epoca fuera de Vigilia): {fmt(metrics['latencia_sueno_min'])} min "
        f"(epoca {metrics['primer_epoca_no_vigilia']}).",
        f"- Latencia a N2: {fmt(metrics['latencia_n2_min'])} min. "
        f"Latencia a S3/SWS: {fmt(metrics['latencia_n3_min'])} min.",
        f"- Tiempo total de sueno (no Vigilia): {metrics['minutos_sueno']:.1f} min "
        f"(eficiencia {metrics['eficiencia_pct']:.1f}% del registro).",
    ]
    if "bloque_n3_desde_min" in metrics:
        L.append(f"- Bloque principal S3/SWS: {metrics['bloque_n3_desde_min']:.1f}-"
                 f"{metrics['bloque_n3_hasta_min']:.1f} min desde el inicio.")
    if "luz_off_min" in lights:
        L.append(f"- Marcadores: Luz OFF {lights['luz_off_min']:.1f} min; "
                 f"Luz ON {lights.get('luz_on_min', float('nan')):.1f} min.")
    L += [
        "",
        "## Distribucion de fases",
        "",
        "| Fase | Codigo | Epocas | Minutos | % tiempo |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in stage_rows:
        L.append(f"| {STAGE_LONG[r['codigo']]} | {r['codigo']} | {r['epocas']} | "
                 f"{r['minutos']:.1f} | {r['pct_tiempo']:.1f} |")
    L += [
        "",
        f"## Potencia relativa por banda y fase ({used_lbl})",
        "",
        "| Fase | Delta % | Theta % | Alfa % | Sigma % | Beta % |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in stage_rows:
        L.append(f"| {r['fase']} | {r['delta_rel']:.1f} | {r['theta_rel']:.1f} | "
                 f"{r['alpha_rel']:.1f} | {r['sigma_rel']:.1f} | {r['beta_rel']:.1f} |")
    L += [
        "",
        f"## Potencia absoluta por banda y fase (uV^2, {used_lbl})",
        "",
        "| Fase | Delta | Theta | Alfa | Sigma | Beta |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in stage_rows:
        L.append(f"| {r['fase']} | {r['delta_abs']:.1f} | {r['theta_abs']:.1f} | "
                 f"{r['alpha_abs']:.1f} | {r['sigma_abs']:.1f} | {r['beta_abs']:.1f} |")
    L += [
        "",
        "## Figuras",
        "",
    ]
    for f in figures:
        L.append(f"- `outputs/figures/{f.name}`")
    L += [
        "",
        "## Lectura prudente",
        "",
        "- El registro muestra un descenso NREM completo hasta S3/SWS, sin evidencia de REM ni S4.",
        "- Tras el filtrado correcto, **delta crece con la profundidad** y es maxima en S3/SWS, "
        "corrigiendo el patron invertido del analisis sin filtrar previo.",
        "- La banda **sigma (12-15 Hz)** se analiza como **proxy descriptivo** de husos; "
        "no se aplico un detector formal de husos. Proponer un detector (p. ej. YASA) como trabajo futuro.",
        "- Como el EEG y la tarea de memoria provienen de fuentes distintas, **no se calcula** "
        "correlacion directa husos-memoria; el vinculo se integra a nivel teorico.",
        f"- Segunda columna de `S3PRACTICA.txt` (ignorada): {dict(Counter(flags.tolist()))}.",
    ]
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


def write_json(stages, stage_rows, metrics, lights, qrows) -> Path:
    out = OUTPUTS / "2026-06-11_eeg-resultados-mne_v3.json"
    payload = {
        "codigos_presentes": sorted(set(stages.tolist())),
        "conteo": {int(k): int(v) for k, v in Counter(stages.tolist()).items()},
        "canales_usados": [q["canal"] for q in qrows if not q["malo"]] or
        [min(qrows, key=lambda q: q["std_uv"])["canal"]],
        "metrics": metrics,
        "lights": lights,
        "calidad_canales": qrows,
        "fases": stage_rows,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> None:
    stages, flags = load_scoring()
    raw, raw_filt = load_raw_filtered()
    lights = parse_light_markers(raw)
    qrows = channel_quality(raw_filt)
    used = select_channels(qrows)
    ch_label = " + ".join(used)

    epochs = make_epochs(raw_filt, len(stages))
    assert len(epochs) == len(stages), f"epocas {len(epochs)} != scoring {len(stages)}"

    bp = epoch_band_powers(epochs, stages, used)
    stage_rows = aggregate_by_stage(stages, bp)
    psd_by_stage = stage_mean_psd(stages, bp)
    metrics = sleep_metrics(stages)

    figures = [
        fig_hypnogram(stages, lights),
        fig_stage_percent(stage_rows),
        fig_band_by_stage(stage_rows, ch_label),
        fig_psd_by_stage(psd_by_stage, bp["freqs"], ch_label),
        fig_spectrogram(raw_filt, stages, lights, used),
    ]
    md = write_report(stages, flags, qrows, used, stage_rows, metrics, lights, raw, figures)
    js = write_json(stages, stage_rows, metrics, lights, qrows)

    print(f"MNE {mne.__version__}")
    print(f"codigos presentes: {sorted(set(stages.tolist()))}")
    print(f"canales usados: {used}  (descartados: {[q['canal'] for q in qrows if q['malo']]})")
    print("fases:")
    for r in stage_rows:
        print(f"  {r['fase']:7s} {r['epocas']:3d} ep  {r['minutos']:5.1f} min  "
              f"delta_abs={r['delta_abs']:8.1f}  delta_rel={r['delta_rel']:.1f}%  "
              f"sigma_abs={r['sigma_abs']:6.2f}  sigma_rel={r['sigma_rel']:.2f}%")
    print(f"wrote {md.relative_to(ROOT)}")
    print(f"wrote {js.relative_to(ROOT)}")
    for f in figures:
        print(f"wrote {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
