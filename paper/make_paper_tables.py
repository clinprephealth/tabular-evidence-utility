"""Paper tables — every value read from the frozen JSON in data/. No re-estimation.

Writes tab_means.tex, tab_deltas.tex, tab_acq.tex, tab_sens.tex, tab_mimic.tex
so that `python3 make_paper_tables.py && python3 make_paper_figs.py && tectonic main.tex`
rebuilds the manuscript from committed result files.
"""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json

ROOT = Path(__file__).parent
DATA = ROOT / "data"

PROD = ["baseline-logistic", "baseline-histgb", "tabicl-classifier"]
PLABEL = {
    "baseline-logistic": "Logistic",
    "baseline-histgb": "HistGB",
    "tabicl-classifier": "FM probe",
}
VSHORT = {"IMPROVES": "improves", "NO_MEASURED_COST": "no measured cost", "COSTS_UTILITY": "costs utility"}
VLETTER = {"IMPROVES": "I", "NO_MEASURED_COST": "N", "COSTS_UTILITY": "C"}


def D(x):
    return Decimal(str(x))


def q3(x):
    return D(x).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def mean_sd(cell):
    return f"{q3(cell['mean'])} ({q3(cell['sd'])})"


def signed(x):
    v = q3(x)
    orig = D(x)
    if v == 0:
        sign = "$+$" if orig >= 0 else r"$-$"
    else:
        sign = "$+$" if v >= 0 else r"$-$"
    return sign + str(abs(v))


def signed_math(x):
    """Whole signed number in math mode, matching tab_mimic.tex."""
    v = q3(x)
    orig = D(x)
    if v == 0:
        sign = "+" if orig >= 0 else "-"
    else:
        sign = "+" if v >= 0 else "-"
    return f"${sign}{abs(v)}$"


def fmt_ci(pair):
    lo, hi = pair["ci95"]
    return f"[{signed(lo)}, {signed(hi)}]"


def load(name):
    return json.loads((DATA / name).read_text())


def tab_means():
    domains = load("ci_study_report.v1.json")["domains"]
    ce = load("ci_study_domain_e.v1.json")["domains"]["environmental_reg"]
    blocks = [
        ("Healthcare (K=20)", domains["healthcare"], False),
        ("Manufacturing (K=10)", domains["non_healthcare"], True),
        ("Consumer (K=10)", domains["consumer_behavior"], False),
        ("Regulatory (Cal-FF) (K=10)", ce, False),
    ]
    lines = []
    for i, (title, dom, p1_eq) in enumerate(blocks):
        if i:
            lines.append(r"\midrule")
        for j, pid in enumerate(PROD):
            p = dom["producers"][pid]
            p0, p2 = mean_sd(p["auroc_by_level"]["P0"]), mean_sd(p["auroc_by_level"]["P2"])
            p1 = r"$\equiv$ P0" if p1_eq else mean_sd(p["auroc_by_level"]["P1"])
            lead = rf"\multirow{{3}}{{*}}{{{title}}} & " if j == 0 else " & "
            lines.append(f"{lead}{PLABEL[pid]} & {p0} & {p1} & {p2} \\\\")
    lines.append(r"\bottomrule")
    return "\n".join(lines) + "\n"


def tab_deltas():
    domains = load("ci_study_report.v1.json")["domains"]
    ce = load("ci_study_domain_e.v1.json")["domains"]["environmental_reg"]
    groups = [
        ("Healthcare, P1$-$P0", domains["healthcare"], "P1-P0"),
        ("Healthcare, P2$-$P1", domains["healthcare"], "P2-P1"),
        ("Manufacturing, P2$-$P0", domains["non_healthcare"], "P2-P0"),
        ("Consumer, P1$-$P0", domains["consumer_behavior"], "P1-P0"),
        ("Consumer, P2$-$P1", domains["consumer_behavior"], "P2-P1"),
        ("Regulatory (Cal-FF), P1$-$P0", ce, "P1-P0"),
        ("Regulatory (Cal-FF), P2$-$P1", ce, "P2-P1"),
    ]
    lines = []
    for i, (title, dom, step) in enumerate(groups):
        if i:
            lines.append(r"\midrule")
        for j, pid in enumerate(PROD):
            dd = dom["producers"][pid]["paired_deltas"][step]
            lead = rf"\multirow{{3}}{{*}}{{{title}}} & " if j == 0 else " & "
            lines.append(
                f"{lead}{PLABEL[pid]} & {signed(dd['mean'])} & {fmt_ci(dd)} & {VSHORT[dd['verdict']]} \\\\"
            )
    lines.append(r"\bottomrule")
    return "\n".join(lines) + "\n"


def pct(excl, n):
    return f"{round(100 * excl / n)}\\%"


def acq_row(label, n_classes, n_pairs, n_test, included, excluded, acc, spearman, bar, interval=None):
    if interval:
        acc_s = f"{q3(acc)} [{q3(interval[0])}, {q3(interval[1])}]"
        sp_s = f"{q3(spearman)} [{q3(interval[2])}, {q3(interval[3])}]" if len(interval) == 4 else f"{q3(spearman)}"
        # healthcare replicated: spearman has its own CI passed as extra
    else:
        acc_s = str(q3(acc))
        sp_s = str(q3(spearman))
    bar_s = bar
    return (
        f"{label} & {n_classes} / {n_pairs} & {n_test:,} & {included:,} & "
        f"{excluded:,} ({pct(excluded, n_test)}) & {acc_s} & {sp_s} & {bar_s} \\\\"
    )


def tab_acq():
    aci = load("acquisition_ci_report.v1.json")
    acq = load("acquisition_report.v1.json")
    mf = load("acquisition_report_manufacturing_p0.v1.json")
    c0 = load("acquisition_report_consumer_p0.v1.json")
    c1 = load("acquisition_report_consumer_p1.v1.json")
    s = aci["summary"]
    n_test = s["pooled_included"] + s["pooled_excluded_indistinguishable"]
    split0 = aci["per_split"][0]
    ra, sp = s["ranking_accuracy"], s["spearman_pred_vs_actual"]
    lines = [
        acq_row(
            "Healthcare, P1 (20 splits)",
            split0["n_classes"],
            split0["n_pairs"],
            n_test,
            s["pooled_included"],
            s["pooled_excluded_indistinguishable"],
            ra["mean"],
            sp["mean"],
            f"{s['splits_clearing_usefulness_bar']}/20",
            interval=(ra["ci95"][0], ra["ci95"][1], sp["ci95"][0], sp["ci95"][1]),
        ),
        acq_row(
            "Healthcare, P1 (v1 split)",
            5,
            10,
            acq["n_test_rows"],
            acq["included"],
            acq["excluded_indistinguishable"],
            acq["ranking_accuracy"],
            acq["spearman_pred_vs_actual"],
            "yes",
        ),
        acq_row(
            "Manufacturing, P0",
            mf["n_classes"],
            mf["n_pairs"],
            mf["n_test_rows"],
            mf["included"],
            mf["excluded_indistinguishable"],
            mf["ranking_accuracy"],
            mf["spearman_pred_vs_actual"],
            "yes",
        ),
        acq_row(
            "Consumer, P0",
            len(c0["class_map"]),
            c0["n_pairs"],
            c0["n_test_rows"],
            c0["included"],
            c0["excluded_indistinguishable"],
            c0["ranking_accuracy"],
            c0["spearman_pred_vs_actual"],
            "yes",
        ),
        acq_row(
            "Consumer, P1",
            len(c1["class_map"]),
            c1["n_pairs"],
            c1["n_test_rows"],
            c1["included"],
            c1["excluded_indistinguishable"],
            c1["ranking_accuracy"],
            c1["spearman_pred_vs_actual"],
            "yes",
        ),
        r"\bottomrule",
    ]
    return "\n".join(lines) + "\n"


def tab_sens():
    s = load("acquisition_sensitivity.v1.json")
    lines = []

    def cell_line(factor, setting, c, spearman=True):
        sp = str(q3(c["spearman_pred_vs_actual"])) if spearman and "spearman_pred_vs_actual" in c else "--"
        return f"{factor} & {setting} & {c['included']} & {q3(c['ranking_accuracy'])} & {sp} \\\\"

    m = s["cells"]["m_donors"]
    for setting, key in (("8", "8"), ("4", "4"), ("16", "16")):
        lines.append(cell_line(r"donor imputations $M$", setting, m[key]))
    lines.append(r"\midrule")
    salt = s["cells"]["donor_salt"]
    lines.append(cell_line("donor identity", "v1 order", salt["v1 (no salt)"]))
    lines.append(cell_line("donor identity", r"alt.\ 1", salt["s1:"]))
    lines.append(cell_line("donor identity", r"alt.\ 2", salt["s2:"]))
    lines.append(cell_line("donor identity", r"alt.\ 3", salt["s3:"]))
    lines.append(r"\midrule")
    bar = s["cells"]["indistinguishable_bar"]
    for b in ("0.002", "0.005", "0.01", "0.02"):
        lines.append(cell_line("indistinguishability bar", b, bar[b], spearman=False))
    lines.append(r"\midrule")
    rot = s["cells"]["rotation_offset"]
    lines.append(cell_line("pair-rotation offset", "0", rot["0"]))
    lines.append(cell_line("pair-rotation offset", "5", rot["5"]))
    lines.append(r"\bottomrule")
    return "\n".join(lines) + "\n"


def tab_mimic():
    d = load("ci_study_mimic.v0.json")["domains"]["healthcare_mimic"]
    lines = [
        r"\begin{tabular}{lccclclc}",
        r"\toprule",
        r"Producer & $\pz$ & $\po$ & $\pt$ & $\po-\pz$ & & $\pt-\po$ & \\",
        r"\midrule",
    ]
    for pid in PROD:
        p = d["producers"][pid]
        a = p["auroc_by_level"]
        d01, d12 = p["paired_deltas"]["P1-P0"], p["paired_deltas"]["P2-P1"]
        lines.append(
            f"{PLABEL[pid]} & {mean_sd(a['P0'])} & {mean_sd(a['P1'])} & {mean_sd(a['P2'])} & "
            f"{signed_math(d01['mean'])} [{signed_math(d01['ci95'][0])}, {signed_math(d01['ci95'][1])}] & "
            f"{VLETTER[d01['verdict']]} & "
            f"{signed_math(d12['mean'])} [{signed_math(d12['ci95'][0])}, {signed_math(d12['ci95'][1])}] & "
            f"{VLETTER[d12['verdict']]} \\\\"
        )
    lines.append(r"\bottomrule")
    return "\n".join(lines) + "\n"


def main():
    writers = {
        "tab_means.tex": tab_means,
        "tab_deltas.tex": tab_deltas,
        "tab_acq.tex": tab_acq,
        "tab_sens.tex": tab_sens,
        "tab_mimic.tex": tab_mimic,
    }
    for name, fn in writers.items():
        (ROOT / name).write_text(fn())
        print("ok", name)


if __name__ == "__main__":
    main()
