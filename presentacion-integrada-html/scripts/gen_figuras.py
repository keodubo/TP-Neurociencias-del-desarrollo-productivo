"""Genera figuras editoriales (estilo Nature, tema claro) para la presentacion.

Etiquetas de fase CORREGIDAS por la catedra (codigos 0/1/2/3):
    0 = Vigilia
    1 = S1
    2 = S3      (NO S2)
    3 = S4      (sueno de ondas lentas mas profundo)
No hay S2 ni REM en este registro. SWS profundo = S3 + S4.
Orden por profundidad: Vigilia -> S1 -> S3 -> S4.

Figs 1-7: datos provistos (numeros exactos, sin recomputar).
Fig 8 (best effort): PSD y espectrograma re-corriendo MNE sobre la senal real (C3).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PRES_DIR = SCRIPT_DIR.parent                       # presentacion-integrada-html/
ROOT = PRES_DIR.parent                             # repo root
FIGURES = PRES_DIR / "assets" / "figuras"
DATA = ROOT / "data"
VHDR = DATA / "S3practica.vhdr"
SCORING = DATA / "S3PRACTICA.txt"
FIGURES.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Tema editorial
# ---------------------------------------------------------------------------
PAPER = "#FBFAF7"
INK = "#1F2430"
SPINE = "#C9C6BE"
GRID = "#E7E4DC"

# Paleta de bandas
COL = {
    "delta": "#312E81",   # indigo profundo
    "theta": "#4338CA",   # indigo
    "alpha": "#6366F1",   # indigo claro
    "sigma": "#0E7C7B",   # teal (banda destacada = proxy de husos)
    "beta": "#9CA3AF",    # gris
}
# Rampa de profundidad Vigilia -> S4
DEPTH = {
    "Vigilia": "#B8B5AD",
    "S1": "#7FB5B4",
    "S3": "#4338CA",
    "S4": "#312E81",
}
ACCENT = "#4338CA"   # indigo de acento
TEAL = "#0E7C7B"
CORAL = "#C2410C"
GRAY = "#9CA3AF"

# Etiquetas CORREGIDAS por codigo
STAGE_LABEL = {0: "Vigilia", 1: "S1", 2: "S3", 3: "S4"}
STAGE_ORDER = ["Vigilia", "S1", "S3", "S4"]

plt.rcParams.update({
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "text.color": INK,
    "axes.edgecolor": SPINE,
    "axes.labelcolor": INK,
    "axes.titlecolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.titlesize": 15,
})


def style_axes(ax, grid_axis="y"):
    """Aplica tema editorial: sin spines top/right, grid suave detras de los datos."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK)


def save(fig, name):
    path = FIGURES / name
    fig.savefig(path, facecolor=PAPER, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Datos provistos (numeros exactos)
# ---------------------------------------------------------------------------
# code, label, epochs, minutes, %time, delta_rel, theta_rel, alpha_rel, sigma_rel, beta_rel, sigma_abs
STAGES = [
    (0, "Vigilia", 22, 11.0, 13.84, 56.97, 8.59, 15.38, 2.31, 14.33, 4.32),
    (1, "S1", 28, 14.0, 17.61, 55.09, 18.56, 9.18, 2.54, 11.27, 2.56),
    (2, "S3", 65, 32.5, 40.88, 68.63, 15.49, 4.93, 5.22, 2.51, 11.63),
    (3, "S4", 44, 22.0, 27.67, 91.59, 4.98, 1.66, 0.59, 0.20, 5.00),
]
LABELS = [s[1] for s in STAGES]
PCT = [s[4] for s in STAGES]
MINUTES = [s[3] for s in STAGES]
DELTA_REL = [s[5] for s in STAGES]
THETA_REL = [s[6] for s in STAGES]
ALPHA_REL = [s[7] for s in STAGES]
SIGMA_REL = [s[8] for s in STAGES]
BETA_REL = [s[9] for s in STAGES]
SIGMA_ABS = [s[10] for s in STAGES]

# Arquitectura
LUZ_OFF = 1.05
LUZ_ON = 79.68
S4_BLOCK = (45.5, 68.0)
EPOCH_SEC = 30

# Tarea de memoria (por sujeto, /20)
# (sujeto, condicion, TR, TS, definicion)
MEM = [
    (1, "Vigilia", 0, 0, 14),
    (2, "Vigilia", 10, 14, 20),
    (3, "Vigilia", 1, 1, 18),
    (4, "SUEÑO", 15, 17, 20),
]


# ---------------------------------------------------------------------------
# Fig 1: Hipnograma
# ---------------------------------------------------------------------------
def fig_hipnograma():
    codes = np.loadtxt(SCORING, dtype=int)[:, 0]   # solo columna 1
    assert codes.size == 159, f"esperaba 159 epocas, hay {codes.size}"
    t = np.arange(codes.size) * EPOCH_SEC / 60.0    # minutos

    fig, ax = plt.subplots(figsize=(12, 3.8))
    # y = codigo (0..3); con eje invertido, mayor codigo (mas profundo) queda abajo
    ax.step(t, codes.astype(float), where="post", color=INK, linewidth=1.3, zorder=3)
    # Sombrear bloque S4
    ax.axvspan(S4_BLOCK[0], S4_BLOCK[1], color=ACCENT, alpha=0.12, zorder=1,
               label="Bloque S4 (45.5-68.0 min)")
    # Lineas de luz
    for x, lab in [(LUZ_OFF, "Luz OFF"), (LUZ_ON, "Luz ON")]:
        ax.axvline(x, color=CORAL, linestyle="--", linewidth=1.0, zorder=2)
        ax.text(x + 0.4, -0.35, lab, rotation=90, va="bottom", ha="left",
                fontsize=8, color=CORAL)

    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["Vigilia", "S1", "S3", "S4"])
    ax.set_ylim(-0.6, 3.4)
    ax.invert_yaxis()   # profundo (S4) abajo
    ax.set_xlim(0, 79.5)
    ax.set_xlabel("Minutos desde el inicio del registro")
    ax.set_ylabel("Fase del sueño")
    ax.set_title("Hipnograma — épocas de 30 s (C3)", loc="left", fontweight="bold")
    style_axes(ax, grid_axis="x")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.tight_layout()
    return save(fig, "hipnograma.png")


# ---------------------------------------------------------------------------
# Fig 2: Distribucion de fases
# ---------------------------------------------------------------------------
def fig_fases_distribucion():
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    colors = [DEPTH[l] for l in LABELS]
    bars = ax.bar(LABELS, PCT, color=colors, width=0.62, zorder=3)
    ax.set_ylabel("% del tiempo registrado")
    ax.set_title("Distribución de fases del sueño", loc="left", fontweight="bold")
    ax.set_ylim(0, max(PCT) * 1.2)
    style_axes(ax)
    for bar, p, m in zip(bars, PCT, MINUTES):
        ax.text(bar.get_x() + bar.get_width() / 2, p + 0.8,
                f"{p:.1f}%\n({m:.1f} min)", ha="center", va="bottom",
                fontsize=9, color=INK)
    fig.tight_layout()
    return save(fig, "fases-distribucion.png")


# ---------------------------------------------------------------------------
# Fig 3: Delta relativa por fase
# ---------------------------------------------------------------------------
def fig_delta_por_fase():
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    x = np.arange(len(LABELS))
    ax.plot(x, DELTA_REL, color=ACCENT, linewidth=2.2, marker="o",
            markersize=9, markerfacecolor=ACCENT, markeredgecolor=PAPER,
            markeredgewidth=1.2, zorder=3)
    for xi, v in zip(x, DELTA_REL):
        dy = 2.5 if xi < len(x) - 1 else -5.5
        va = "bottom" if xi < len(x) - 1 else "top"
        ax.text(xi, v + dy, f"{v:.1f}%", ha="center", va=va,
                fontsize=9.5, color=INK, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(LABELS)
    ax.set_ylabel("Delta relativa (%)")
    ax.set_ylim(45, 100)
    ax.set_title("La potencia delta crece con la profundidad", loc="left",
                 fontweight="bold")
    style_axes(ax)
    # Anotacion coral cerca de S4
    ax.annotate("máxima en S4 (91.6%)",
                xy=(3, DELTA_REL[3]), xytext=(2.05, 86),
                fontsize=9.5, color=CORAL, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.3))
    fig.tight_layout()
    return save(fig, "delta-por-fase.png")


# ---------------------------------------------------------------------------
# Fig 4: Sigma absoluta por fase
# ---------------------------------------------------------------------------
def fig_sigma_por_fase():
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    colors = [TEAL if l == "S3" else GRAY for l in LABELS]
    bars = ax.bar(LABELS, SIGMA_ABS, color=colors, width=0.62, zorder=3)
    ax.set_ylabel("Potencia sigma 12–15 Hz (µV²)")
    ax.set_title("Sigma (proxy de husos): máximo en S3", loc="left",
                 fontweight="bold")
    ax.set_ylim(0, max(SIGMA_ABS) * 1.22)
    style_axes(ax)
    for bar, v in zip(bars, SIGMA_ABS):
        ax.text(bar.get_x() + bar.get_width() / 2, v + max(SIGMA_ABS) * 0.02,
                f"{v:.2f}", ha="center", va="bottom", fontsize=9.5, color=INK)
    ax.text(0.99, 0.97, "husos = proxy; sin detector formal",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8, color=CORAL, style="italic")
    fig.tight_layout()
    return save(fig, "sigma-por-fase.png")


# ---------------------------------------------------------------------------
# Fig 5: Composicion espectral relativa apilada
# ---------------------------------------------------------------------------
def fig_bandas_composicion():
    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    x = np.arange(len(LABELS))
    band_data = {
        "delta": DELTA_REL,
        "theta": THETA_REL,
        "alpha": ALPHA_REL,
        "sigma": SIGMA_REL,
        "beta": BETA_REL,
    }
    bottom = np.zeros(len(LABELS))
    for band, vals in band_data.items():
        vals = np.array(vals)
        ax.bar(x, vals, 0.6, bottom=bottom, label=band, color=COL[band],
               edgecolor=PAPER, linewidth=0.7, zorder=3)
        bottom += vals
    ax.set_xticks(x)
    ax.set_xticklabels(LABELS)
    ax.set_ylabel("% de potencia relativa")
    ax.set_ylim(0, 105)
    ax.set_title("Composición espectral relativa por fase (C3)", loc="left",
                 fontweight="bold")
    style_axes(ax)
    ax.legend(ncol=5, frameon=False, fontsize=9.5, loc="upper center",
              bbox_to_anchor=(0.5, -0.10))
    fig.tight_layout()
    return save(fig, "bandas-composicion.png")


# ---------------------------------------------------------------------------
# Fig 6: Slope chart TR -> TS (palabra objetivo)
# ---------------------------------------------------------------------------
def fig_memoria_tr_ts():
    fig, ax = plt.subplots(figsize=(7.8, 5.4))
    xpos = [0, 1]
    CTRL = "#6B7280"
    # Sujetos individuales del grupo control (vigilia)
    vig = [(tr, ts) for _suj, cond, tr, ts, _d in MEM if cond != "SUEÑO"]
    for k, (tr, ts) in enumerate(vig):
        ax.plot(xpos, [tr, ts], color=GRAY, linewidth=1.4, marker="o",
                markersize=5, markerfacecolor=GRAY, markeredgecolor=PAPER,
                markeredgewidth=1.0, zorder=2, alpha=0.5,
                label="Vigilia · sujetos (control, n=3)" if k == 0 else None)
    # Promedio del grupo control
    tr_m = sum(t for t, _ in vig) / len(vig)
    ts_m = sum(s for _, s in vig) / len(vig)
    ax.plot(xpos, [tr_m, ts_m], color=CTRL, linewidth=2.6, marker="s",
            markersize=8, markerfacecolor=CTRL, markeredgecolor=PAPER,
            markeredgewidth=1.2, linestyle=(0, (5, 2)), zorder=3,
            label="Control · promedio")
    ax.text(1.05, ts_m, "Control %.1f→%.1f" % (tr_m, ts_m), color=CTRL,
            fontsize=10, fontweight="bold", va="center", ha="left")
    # Condición sueño
    for _suj, cond, tr, ts, _d in MEM:
        if cond == "SUEÑO":
            ax.plot(xpos, [tr, ts], color=ACCENT, linewidth=3.2, marker="o",
                    markersize=10, markerfacecolor=ACCENT, markeredgecolor=PAPER,
                    markeredgewidth=1.4, zorder=5, label="Sueño (n=1)")
            ax.text(1.05, ts, "Sueño 15→17", color=ACCENT, fontsize=11,
                    fontweight="bold", va="center", ha="left")

    ax.set_xticks(xpos)
    ax.set_xticklabels(["TR", "TS"])
    ax.set_xlim(-0.25, 1.62)
    ax.set_ylim(0, 20)
    ax.set_ylabel("Palabra objetivo (correctas /20)")
    ax.set_title("Recuerdo formal: sueño vs. control (vigilia)", loc="left", fontweight="bold")
    style_axes(ax, grid_axis="y")
    ax.legend(loc="upper left", frameon=False, fontsize=9.5, handlelength=2.4)
    fig.text(0.01, -0.02,
             "n=1 en condición sueño; lectura descriptiva, no causal",
             fontsize=8, color=CORAL, style="italic", ha="left")
    fig.tight_layout()
    return save(fig, "memoria-tr-ts.png")


# ---------------------------------------------------------------------------
# Fig 7: Barras palabra objetivo (TS) y definicion
# ---------------------------------------------------------------------------
def fig_memoria_barras():
    sujetos = [f"Sujeto {m[0]}" for m in MEM]
    ts_vals = [m[3] for m in MEM]            # palabra objetivo TS: 0,14,1,17
    def_vals = [m[4] for m in MEM]           # definicion: 14,20,18,20
    colors = [ACCENT if m[1] == "SUEÑO" else GRAY for m in MEM]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 4.9))
    for ax, vals, title in [(axL, ts_vals, "Palabra objetivo"),
                            (axR, def_vals, "Definición")]:
        bars = ax.bar(sujetos, vals, color=colors, width=0.62, zorder=3)
        ax.set_ylim(0, 21)
        ax.set_ylabel("Correctas /20")
        ax.set_title(title, loc="left", fontweight="bold", fontsize=12.5)
        style_axes(ax)
        ax.tick_params(axis="x", labelsize=9)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3,
                    f"{v}", ha="center", va="bottom", fontsize=9.5, color=INK)

    fig.suptitle("Tarea de palabras: desempeño final por sujeto",
                 x=0.01, ha="left", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.01, -0.02,
             "n=1 en condición sueño; lectura descriptiva, no causal",
             fontsize=8, color=CORAL, style="italic", ha="left")
    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    return save(fig, "memoria-barras.png")


# ---------------------------------------------------------------------------
# Fig 8 (best effort): PSD y espectrograma con MNE sobre la senal real (C3)
# ---------------------------------------------------------------------------
def fig_mne():
    import mne

    EEG_CH = "C3"
    NOTCH_HZ = 50.0
    BP_LOW, BP_HIGH = 0.3, 35.0
    EOG_CH = ["EOG I", "EOG D"]
    EMG_CH = ["EMGI", "EMGD"]

    codes = np.loadtxt(SCORING, dtype=int)[:, 0]
    n_ep = codes.size

    raw = mne.io.read_raw_brainvision(VHDR, preload=True, verbose="ERROR")
    ch_types = {c: "eog" for c in EOG_CH if c in raw.ch_names}
    ch_types.update({c: "emg" for c in EMG_CH if c in raw.ch_names})
    raw.set_channel_types(ch_types, verbose="ERROR")
    raw.notch_filter(freqs=[NOTCH_HZ], picks="eeg", verbose="ERROR")
    raw.filter(l_freq=BP_LOW, h_freq=BP_HIGH, picks="eeg",
               fir_design="firwin", verbose="ERROR")

    sfreq = raw.info["sfreq"]
    needed = n_ep * EPOCH_SEC
    raw_crop = raw.copy().crop(tmin=0.0, tmax=needed - 1.0 / sfreq)
    epochs = mne.make_fixed_length_epochs(raw_crop, duration=EPOCH_SEC,
                                          preload=True, verbose="ERROR")
    assert len(epochs) == n_ep, f"epocas {len(epochs)} != scoring {n_ep}"

    n_fft = int(4 * sfreq)
    n_overlap = int(2 * sfreq)
    spectrum = epochs.compute_psd(method="welch", fmin=0.3, fmax=35.0,
                                  n_fft=n_fft, n_overlap=n_overlap,
                                  picks=[EEG_CH], verbose="ERROR")
    psds, freqs = spectrum.get_data(return_freqs=True)   # (n_ep, 1, n_freq) V^2/Hz
    psd_uv2 = psds[:, 0, :] * 1e12                        # uV^2/Hz

    # --- PSD por fase ---
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    mask = (freqs >= 0.5) & (freqs <= 30)
    for code in [0, 1, 2, 3]:
        idx = np.where(codes == code)[0]
        if idx.size == 0:
            continue
        mean_psd = psd_uv2[idx].mean(axis=0)
        ax.semilogy(freqs[mask], mean_psd[mask], color=DEPTH[STAGE_LABEL[code]],
                    linewidth=2.0, label=STAGE_LABEL[code], zorder=3)
    ax.axvspan(12, 15, color=TEAL, alpha=0.12, zorder=1)
    ymax = ax.get_ylim()[1]
    ax.text(13.5, ymax * 0.45, "sigma\n12–15 Hz", ha="center", fontsize=8,
            color=TEAL)
    ax.set_xlim(0.5, 30)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("DEP (µV²/Hz, escala log)")
    ax.set_title("PSD promedio por fase (C3)", loc="left", fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(SPINE)
    ax.grid(True, which="both", color=GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=10, title="Fase")
    fig.tight_layout()
    p1 = save(fig, "psd-por-fase.png")

    # --- Espectrograma C3 con hipnograma alineado ---
    from scipy import signal as sp_signal
    data = raw_crop.get_data(picks=[EEG_CH])[0] * 1e6   # uV
    f, t, Sxx = sp_signal.spectrogram(
        data, fs=sfreq, window="hann", nperseg=int(8 * sfreq),
        noverlap=int(6 * sfreq), scaling="density", mode="psd")
    smask = (f >= 0.5) & (f <= 30)
    Sdb = 10 * np.log10(Sxx[smask] + 1e-12)

    fig, (axh, ax) = plt.subplots(
        2, 1, figsize=(12, 5.8), sharex=True,
        gridspec_kw={"height_ratios": [1, 4], "hspace": 0.08})
    th = np.arange(n_ep) * EPOCH_SEC / 60.0
    axh.step(th, codes.astype(float), where="post", color=INK, linewidth=1.2)
    axh.axvspan(S4_BLOCK[0], S4_BLOCK[1], color=ACCENT, alpha=0.12)
    axh.set_yticks([0, 1, 2, 3])
    axh.set_yticklabels(["Vigilia", "S1", "S3", "S4"], fontsize=8)
    axh.set_ylim(-0.5, 3.5)
    axh.invert_yaxis()
    axh.set_ylabel("Fase", fontsize=9)
    axh.spines["top"].set_visible(False)
    axh.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        axh.spines[s].set_color(SPINE)
    axh.grid(axis="x", color=GRID, linewidth=0.5)
    axh.set_axisbelow(True)
    axh.set_title("Espectrograma C3 con hipnograma alineado", loc="left",
                  fontweight="bold")

    im = ax.pcolormesh(t / 60, f[smask], Sdb, shading="auto", cmap="magma",
                       vmin=np.percentile(Sdb, 5), vmax=np.percentile(Sdb, 97))
    ax.set_ylim(0.5, 30)
    ax.set_xlim(0, 79.5)
    ax.set_xlabel("Minutos desde el inicio del registro")
    ax.set_ylabel("Frecuencia (Hz)")
    for x in (LUZ_OFF, LUZ_ON):
        ax.axvline(x, color="#FBE4D5", linestyle="--", linewidth=1.0)
    cbar = fig.colorbar(im, ax=[axh, ax], pad=0.01)
    cbar.set_label("Potencia (dB, µV²/Hz)", color=INK)
    cbar.ax.tick_params(colors=INK)
    p2 = save(fig, "espectrograma.png")
    return [p1, p2]


# ---------------------------------------------------------------------------
def main():
    generated = []
    generated.append(fig_hipnograma())
    generated.append(fig_fases_distribucion())
    generated.append(fig_delta_por_fase())
    generated.append(fig_sigma_por_fase())
    generated.append(fig_bandas_composicion())
    generated.append(fig_memoria_tr_ts())
    generated.append(fig_memoria_barras())
    print(f"Figs 1-7 OK: {len(generated)} archivos")

    # Fig 8: best effort
    try:
        mne_figs = fig_mne()
        generated.extend(mne_figs)
        print("Fig 8 (PSD + espectrograma) OK")
    except Exception as exc:  # noqa: BLE001
        print(f"Fig 8 OMITIDA — {type(exc).__name__}: {exc}")

    print("\nArchivos generados:")
    for p in generated:
        kb = p.stat().st_size / 1024
        print(f"  {p.name:28s} {kb:8.1f} KB")


if __name__ == "__main__":
    main()
