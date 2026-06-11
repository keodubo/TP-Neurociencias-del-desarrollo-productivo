from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "PRÁCTICO LABORATORIO EQUIPO 1.xlsx"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"


DEFINITION_SCORING: dict[str, dict[str, tuple[bool, str]]] = {
    "Sujeto 1": {
        "NOMON": (True, "reloj solar conserva el significado de reloj de sol"),
        "ZORCICO": (False, "danza de algo es demasiado inespecifico"),
        "MARMITÓN": (True, "ayudante de cocina exacto"),
        "EPINICIO": (True, "grito/canto de victoria conserva la idea central"),
        "ERGOTINA": (False, "receta de algo no recupera remedio para hemorragias"),
        "RETEL": (True, "red para cangrejos recupera la funcion"),
        "CAURO": (True, "viento del noroeste exacto"),
        "QUIMA": (True, "rama de algo recupera parcialmente la categoria"),
        "PILTRO": (False, "habitacion de algo no especifica templo"),
        "FISGA": (False, "arpa de algo no recupera arpon para pescar"),
        "POSMA": (True, "lentitud para hacer algo exacto"),
        "LASTO": (True, "recibo de algo conserva recibo/pago"),
        "GREBA": (True, "armadura para la rodilla exacto"),
        "MAINEL": (True, "baranda de una escalera exacto"),
        "JABARDO": (False, "sin respuesta"),
        "SAMARUGO": (True, "renacuajo de sapo conserva renacuajo"),
        "BADINA": (True, "charco de agua exacto"),
        "TINELO": (False, "sin respuesta"),
        "NENIA": (True, "poema funebre exacto"),
        "CÍTOLA": (True, "instrumento musical antiguo exacto"),
    },
    "Sujeto 2": {
        "NOMON": (True, "exacto"),
        "ZORCICO": (True, "exacto"),
        "MARMITÓN": (True, "exacto"),
        "EPINICIO": (True, "celebracion de victoria conserva significado"),
        "ERGOTINA": (True, "exacto"),
        "RETEL": (True, "red para pescar conserva funcion"),
        "CAURO": (True, "exacto"),
        "QUIMA": (True, "exacto"),
        "PILTRO": (True, "exacto"),
        "FISGA": (True, "exacto"),
        "POSMA": (True, "lentitud para hacer las cosas conserva significado"),
        "LASTO": (True, "exacto"),
        "GREBA": (True, "exacto"),
        "MAINEL": (True, "baranda para la escalera conserva significado"),
        "JABARDO": (True, "exacto"),
        "SAMARUGO": (True, "exacto"),
        "BADINA": (True, "exacto"),
        "TINELO": (True, "exacto"),
        "NENIA": (True, "poema de un entierro conserva significado"),
        "CÍTOLA": (True, "instrumento antiguo conserva categoria suficiente"),
    },
    "Sujeto 3": {
        "NOMON": (True, "exacto"),
        "ZORCICO": (True, "exacto"),
        "MARMITÓN": (True, "exacto"),
        "EPINICIO": (True, "festejo de victoria conserva significado"),
        "ERGOTINA": (True, "remedio para hemorragias exacto"),
        "RETEL": (True, "exacto"),
        "CAURO": (True, "exacto"),
        "QUIMA": (True, "exacto"),
        "PILTRO": (True, "exacto"),
        "FISGA": (False, "tridente no equivale de forma suficiente a arpon para pescar"),
        "POSMA": (True, "lentitud en hacer algo conserva significado"),
        "LASTO": (True, "exacto"),
        "GREBA": (True, "armadura de rodilla conserva significado"),
        "MAINEL": (True, "exacto"),
        "JABARDO": (True, "conglomerado de gente conserva aglomeracion"),
        "SAMARUGO": (True, "renacuajo de sapo conserva renacuajo"),
        "BADINA": (True, "exacto"),
        "TINELO": (True, "comedor de la servidumbre conserva significado"),
        "NENIA": (True, "poema de entierro conserva significado"),
        "CÍTOLA": (False, "instrumento de la antiguedad omite que es musical"),
    },
    "Sujeto 4": {
        "NOMON": (True, "exacto"),
        "ZORCICO": (True, "exacto"),
        "MARMITÓN": (True, "exacto"),
        "EPINICIO": (True, "exacto"),
        "ERGOTINA": (True, "exacto"),
        "RETEL": (True, "red para pescar conserva funcion"),
        "CAURO": (True, "exacto"),
        "QUIMA": (True, "exacto"),
        "PILTRO": (True, "exacto"),
        "FISGA": (True, "exacto"),
        "POSMA": (True, "hacer algo con lentitud conserva significado"),
        "LASTO": (True, "recibo de compra conserva categoria de recibo"),
        "GREBA": (True, "exacto"),
        "MAINEL": (True, "exacto"),
        "JABARDO": (True, "exacto"),
        "SAMARUGO": (True, "exacto"),
        "BADINA": (True, "exacto"),
        "TINELO": (True, "cuarto de la servidumbre conserva contexto funcional"),
        "NENIA": (True, "exacto"),
        "CÍTOLA": (True, "exacto"),
    },
}


def normalize(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip().upper()
    text = "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
    text = re.sub(r"[^A-Z0-9 ]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_sheet(path: Path, sheet: str) -> tuple[pd.DataFrame, str]:
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    sujeto = str(df.iloc[0, 0]).strip().title()
    condicion = str(df.iloc[1, 0]).replace("CONDICION", "").strip().title()
    eval_block = df.iloc[27:47, 0:4].copy()
    eval_block.columns = ["palabra_objetivo", "respuesta_palabra", "definicion", "respuesta_definicion"]
    eval_block["sujeto"] = sujeto
    eval_block["condicion"] = condicion
    return eval_block, sujeto


def build_results() -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[pd.DataFrame] = []
    for sheet in pd.ExcelFile(DATA).sheet_names:
        block, sujeto = parse_sheet(DATA, sheet)
        rows.append(block)
    detail = pd.concat(rows, ignore_index=True)
    detail["palabra_correcta"] = detail.apply(
        lambda row: normalize(row["palabra_objetivo"]) == normalize(row["respuesta_palabra"]),
        axis=1,
    )

    definition_ok = []
    definition_notes = []
    for row in detail.itertuples(index=False):
        ok, note = DEFINITION_SCORING[row.sujeto][row.palabra_objetivo]
        definition_ok.append(ok)
        definition_notes.append(note)
    detail["definicion_correcta"] = definition_ok
    detail["nota_scoring_definicion"] = definition_notes

    summary = (
        detail.groupby(["sujeto", "condicion"], sort=False)
        .agg(
            palabra_objetivo=("palabra_correcta", "sum"),
            definicion=("definicion_correcta", "sum"),
            items=("palabra_objetivo", "count"),
        )
        .reset_index()
    )
    summary["palabra_objetivo_pct"] = summary["palabra_objetivo"] / summary["items"] * 100
    summary["definicion_pct"] = summary["definicion"] / summary["items"] * 100
    return detail, summary


def save_figure(summary: pd.DataFrame) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig_path = FIGURES / "2026-06-11_memoria_scores_v1.png"

    colors = {"Vigilia": "#61788f", "Sueño": "#d07a38"}
    x = range(len(summary))
    labels = [f"{s}\n{c}" for s, c in zip(summary["sujeto"], summary["condicion"])]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    metrics = [
        ("palabra_objetivo", "Palabra objetivo", "Coincidencia formal normalizada"),
        ("definicion", "Definicion", "Scoring semantico manual"),
    ]

    for ax, (col, title, subtitle) in zip(axes, metrics):
        bar_colors = [colors[c] for c in summary["condicion"]]
        ax.bar(x, summary[col], color=bar_colors, width=0.62)
        ax.set_title(f"{title}\n{subtitle}", loc="left", fontsize=11)
        ax.set_xticks(list(x), labels, fontsize=9)
        ax.set_ylim(0, 22)
        ax.set_yticks([0, 5, 10, 15, 20])
        ax.grid(axis="y", color="#d8dde3", linewidth=0.8)
        ax.set_axisbelow(True)
        for i, val in enumerate(summary[col]):
            ax.text(i, min(val + 0.45, 21.2), f"{int(val)}/20", ha="center", va="bottom", fontsize=9)

    axes[0].set_ylabel("Respuestas correctas sobre 20")
    fig.suptitle("Tarea de palabras: resultados descriptivos por sujeto", x=0.02, ha="left", fontsize=14, fontweight="bold")
    fig.text(
        0.02,
        0.02,
        "Condicion sueño: n=1; resultados descriptivos, sin inferencia estadistica.",
        fontsize=8,
        color="#475569",
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.93])
    fig.savefig(fig_path, dpi=220)
    plt.close(fig)
    return fig_path


def save_markdown(detail: pd.DataFrame, summary: pd.DataFrame, fig_path: Path) -> Path:
    output = OUTPUTS / "2026-06-11_resultados-memoria_v1.md"
    detail_csv = OUTPUTS / "2026-06-11_resultados-memoria-detalle_v1.csv"
    summary_csv = OUTPUTS / "2026-06-11_resultados-memoria-resumen_v1.csv"
    detail.to_csv(detail_csv, index=False)
    summary.to_csv(summary_csv, index=False)

    condition_summary = (
        summary.groupby("condicion", sort=False)
        .agg(
            n=("sujeto", "count"),
            palabra_objetivo_promedio=("palabra_objetivo", "mean"),
            definicion_promedio=("definicion", "mean"),
        )
        .reset_index()
    )

    lines = [
        "# Resultados de memoria - tarea de palabras",
        "",
        "Fecha: 2026-06-11",
        "",
        "## Fuente y procedencia",
        "",
        "- Fuente: `data/PRÁCTICO LABORATORIO EQUIPO 1.xlsx`.",
        "- Hojas leidas: cuatro sujetos, con condicion indicada en cada hoja.",
        "- Derivados generados: este informe, CSV de detalle, CSV de resumen y figura en `outputs/figures/`.",
        "",
        "## Metodo de scoring",
        "",
        "- **Palabra objetivo:** coincidencia formal exacta luego de normalizar mayusculas, acentos y signos.",
        "- **Definicion:** scoring semantico manual binario, documentado item por item en el CSV de detalle.",
        "- El analisis es descriptivo. La condicion sueño tiene `n=1`, por lo que no corresponde inferencia estadistica fuerte.",
        "",
        "## Tabla por sujeto",
        "",
        summary[["sujeto", "condicion", "palabra_objetivo", "definicion", "items"]].to_markdown(index=False),
        "",
        "## Resumen por condicion",
        "",
        condition_summary.to_markdown(index=False, floatfmt=".1f"),
        "",
        "## Figura",
        "",
        f"![Resultados de memoria](figures/{fig_path.name})",
        "",
        "## Lectura prudente",
        "",
        "- En palabra objetivo, el sujeto en condicion sueño conserva mas formas lexicales correctas que los sujetos en vigilia.",
        "- En definicion, el rendimiento es alto en casi todos los sujetos; esto sugiere que la recuperacion semantica fue menos exigente que la recuperacion formal de pseudopalabras.",
        "- La diferencia observada no debe atribuirse causalmente al sueño sin aclarar el tamaño muestral y el caracter descriptivo del practico.",
        "",
        "## Archivos derivados",
        "",
        f"- `outputs/{detail_csv.name}`",
        f"- `outputs/{summary_csv.name}`",
        f"- `outputs/figures/{fig_path.name}`",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main() -> None:
    detail, summary = build_results()
    fig_path = save_figure(summary)
    md_path = save_markdown(detail, summary, fig_path)
    print(f"wrote {md_path.relative_to(ROOT)}")
    print(f"wrote {fig_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
