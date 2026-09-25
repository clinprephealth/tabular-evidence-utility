"""Paper figures — every value read from the frozen JSON in data/. No re-estimation.
fig1  utility vs evidence level, four CI domains
fig2  paired-delta forest, seven step groups, coloured by frozen verdict
fig3  acquisition: 20 replicated splits + v1 split; predicted vs realized scatter (v1 split)
fig4  protocol-parameter sensitivity (v1 split)
fig5  ranking accuracy across tasks with exclusion fraction
fig6  accuracy by realized gap (calibration) and per-class predicted vs realized
"""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

ROOT = Path(__file__).parent
DATA, OUT = ROOT / "data", ROOT / "figs"
OUT.mkdir(exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXIS = "#ffffff", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SERIES = {"baseline-logistic": "#2a78d6", "baseline-histgb": "#eb6834", "tabicl-classifier": "#1baf7a"}
MARK = {"baseline-logistic": "o", "baseline-histgb": "s", "tabicl-classifier": "^"}
LABEL = {"baseline-logistic": "Logistic regression", "baseline-histgb": "HistGB", "tabicl-classifier": "FM probe (TabICL v2)"}
VERDICT = {"IMPROVES": "#0ca30c", "NO_MEASURED_COST": "#898781", "COSTS_UTILITY": "#d03b3b"}
VTXT = {"IMPROVES": "improves", "NO_MEASURED_COST": "no measured cost", "COSTS_UTILITY": "costs utility"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "legend.frameon": False})


def r3(x):
    q = Decimal(str(abs(x))).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    return ("+" if x >= 0 else "−") + str(q)


ci = json.load(open(DATA / "ci_study_report.v1.json"))["domains"]
ce = json.load(open(DATA / "ci_study_domain_e.v1.json"))["domains"]["environmental_reg"]
DOM = {**ci, "environmental_reg": ce}
ORDER = ["healthcare", "non_healthcare", "consumer_behavior", "environmental_reg"]
TITLE = {"healthcare": "Healthcare — acute utilization", "non_healthcare": "Manufacturing — machine failure",
         "consumer_behavior": "Consumer — purchase intent", "environmental_reg": "Regulatory — unpermitted facility"}
SHORT = {"healthcare": "Healthcare", "non_healthcare": "Manufacturing", "consumer_behavior": "Consumer", "environmental_reg": "Regulatory (Cal-FF)"}
LVL = {"P0": "P0", "P1": "P1", "P2": "P2"}
XPOS = {"P0": 0, "P1": 1, "P2": 2}
AXIS_NAME = {"healthcare": "field-count axis", "non_healthcare": "field-count axis", "consumer_behavior": "field-count axis",
             "environmental_reg": "location-precision axis"}


def fig1():
    fig, axes = plt.subplots(1, 4, figsize=(13.5, 3.6), dpi=300)
    ylims = {"healthcare": (0.46, 0.72), "non_healthcare": (0.84, 1.0), "consumer_behavior": (0.87, 0.95), "environmental_reg": (0.55, 0.86)}
    for ax, dom in zip(axes, ORDER):
        d = DOM[dom]; levels = list(d["levels"])
        for pid, p in d["producers"].items():
            xs = [XPOS[l] for l in levels]; ms = [p["auroc_by_level"][l]["mean"] for l in levels]; sds = [p["auroc_by_level"][l]["sd"] for l in levels]
            ax.errorbar(xs, ms, yerr=sds, color=SERIES[pid], marker=MARK[pid], markersize=5.5, linewidth=1.5, capsize=3, capthick=1,
                        markeredgecolor=SURFACE, markeredgewidth=0.8, zorder=3, label=LABEL[pid])
        labs = [f"{LVL[l]}\n{d['levels'][l]['n_features']} fields" for l in levels]
        if dom == "non_healthcare":
            ax.set_xticks([0, 1, 2]); ax.set_xticklabels([labs[0], "P1\n≡ P0", labs[1]])
        else:
            ax.set_xticks([XPOS[l] for l in levels]); ax.set_xticklabels(labs)
        ax.set_xlim(-0.4, 2.4); ax.set_ylim(*ylims[dom])
        ax.set_title(f"{TITLE[dom]}\nn = {d['levels']['P0']['n_rows']:,} · K = {d['K']} · {AXIS_NAME[dom]}", fontsize=8.6, loc="left")
        ax.grid(axis="x", visible=False); ax.tick_params(axis="x", length=0, labelsize=8)
        if dom == "healthcare":
            ax.set_ylabel("AUROC (mean ± SD across splits)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02), fontsize=9)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(OUT / "fig1_frontier_4dom.pdf"); fig.savefig(OUT / "fig1_frontier_4dom.png"); plt.close(fig)


def fig2():
    groups = [("healthcare", "P1-P0"), ("healthcare", "P2-P1"), ("non_healthcare", "P2-P0"), ("consumer_behavior", "P1-P0"),
              ("consumer_behavior", "P2-P1"), ("environmental_reg", "P1-P0"), ("environmental_reg", "P2-P1")]
    order = ["baseline-logistic", "baseline-histgb", "tabicl-classifier"]
    rows, y = [], 0
    for dom, step in groups:
        a, b = step.split("-")
        rows.append(("h", y, f"{SHORT[dom]}   {a} − {b}   (K = {DOM[dom]['K']})")); y -= 1
        for pid in order:
            dd = DOM[dom]["producers"][pid]["paired_deltas"][step]
            rows.append(("r", y, LABEL[pid], dd["mean"], dd["ci95"][0], dd["ci95"][1], dd["verdict"], pid)); y -= 1
        y -= 0.5
    fig, ax = plt.subplots(figsize=(8.6, 9.2), dpi=300)
    ax.axvline(0, color=INK2, linewidth=0.9, zorder=2)
    for r in rows:
        if r[0] == "h":
            ax.text(-0.335, r[1], r[2], fontsize=8.8, fontweight="bold", color=INK, va="center", ha="left"); continue
        _, yy, lab, m, lo, hi, v, pid = r; c = VERDICT[v]
        ax.plot([lo, hi], [yy, yy], color=c, linewidth=2, zorder=3)
        for x in (lo, hi):
            ax.plot([x, x], [yy - 0.16, yy + 0.16], color=c, linewidth=1.2, zorder=3)
        ax.plot(m, yy, marker=MARK[pid], markersize=6, color=c, markeredgecolor=SURFACE, markeredgewidth=0.8, zorder=4)
        ax.text(-0.33, yy, lab, fontsize=8, color=INK2, va="center", ha="left")
        ax.text(0.07, yy, f"{r3(m)} [{r3(lo)}, {r3(hi)}]", fontsize=7.6, color=INK, va="center", ha="left", family="DejaVu Sans Mono")
        ax.text(0.205, yy, VTXT[v], fontsize=7.8, color=c, va="center", ha="left", fontweight="bold")
    ax.set_xlim(-0.34, 0.27); ax.set_ylim(y + 0.2, 1.0); ax.set_yticks([]); ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ticks = [-0.2, -0.15, -0.1, -0.05, 0, 0.05]
    ax.set_xticks(ticks); ax.set_xticklabels([f"{t:+.2f}" if t else "0" for t in ticks], fontsize=8)
    ax.set_xlabel("Paired Δ AUROC per split (later rung − earlier rung); mean and 95% t-interval", fontsize=8.8)
    ax.text(0.07, 0.55, "mean  [95% CI]", fontsize=7.6, color=MUTED, va="center"); ax.text(0.205, 0.55, "frozen verdict", fontsize=7.6, color=MUTED, va="center")
    handles = [Line2D([0], [0], color=VERDICT[k], linewidth=3, label=VTXT[k]) for k in ("IMPROVES", "NO_MEASURED_COST", "COSTS_UTILITY")]
    ax.legend(handles=handles, loc="upper center", fontsize=8, ncol=3, bbox_to_anchor=(0.5, -0.045), columnspacing=2.0,
              title="Verdict rule, fixed before any run:  95% interval entirely above 0 → improves;  covering 0 → no measured cost;  entirely below 0 → costs utility",
              title_fontsize=7.6)
    fig.tight_layout(); fig.savefig(OUT / "fig2_forest_7groups.pdf"); fig.savefig(OUT / "fig2_forest_7groups.png"); plt.close(fig)


def fig3():
    acq = json.load(open(DATA / "acquisition_report.v1.json")); aci = json.load(open(DATA / "acquisition_ci_report.v1.json"))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300, gridspec_kw={"width_ratios": [1.15, 1]})
    # left: 20 splits strip + interval; v1 split separate
    accs = [s["ranking_accuracy"] for s in aci["per_split"]]
    rng = np.random.default_rng(0); jit = rng.uniform(-0.12, 0.12, len(accs))
    a1.scatter(np.zeros(len(accs)) + jit, accs, s=26, color="#2a78d6", alpha=0.85, edgecolor=SURFACE, linewidth=0.5, zorder=3)
    s = aci["summary"]["ranking_accuracy"]
    a1.errorbar([0.45], [s["mean"]], yerr=[[s["mean"] - s["ci95"][0]], [s["ci95"][1] - s["mean"]]], fmt="D", color=INK, markersize=6, capsize=5, zorder=4)
    a1.text(0.55, s["mean"], f"mean {s['mean']:.3f}\n95% CI [{s['ci95'][0]:.3f}, {s['ci95'][1]:.3f}]", fontsize=8.5, va="center", color=INK)
    a1.scatter([1.3], [acq["ranking_accuracy"]], s=60, marker="*", color="#eb6834", zorder=4, edgecolor=SURFACE, linewidth=0.6)
    a1.text(1.4, acq["ranking_accuracy"], f"v1 pre-registered split\n{acq['ranking_accuracy']:.3f} on {acq['included']} evaluable", fontsize=8.5, va="center", color=INK)
    a1.axhline(0.60, color="#d03b3b", linewidth=0.9, linestyle=(0, (4, 3))); a1.text(-0.35, 0.607, "usefulness bar 0.60", fontsize=7.8, color="#d03b3b")
    a1.set_xlim(-0.4, 2.4); a1.set_ylim(0.55, 0.95); a1.set_xticks([0, 1.3]); a1.set_xticklabels(["20 grouped splits (healthcare, P1)\nand their mean ± 95% CI", "v1 pre-registered split"], fontsize=8.5)
    a1.set_ylabel("Ranking accuracy (evaluable cases)"); a1.grid(axis="x", visible=False); a1.tick_params(axis="x", length=0)
    a1.set_title(f"a  Split replication — {aci['summary']['splits_clearing_usefulness_bar']} of 20 splits clear the bar; "
                 f"{aci['summary']['pooled_included']:,} evaluable, {aci['summary']['pooled_excluded_indistinguishable']} excluded", fontsize=9, loc="left")
    # right: scatter v1
    CC = {"conditions": "#2a78d6", "encounters": "#eb6834", "medications": "#1baf7a", "observations": "#eda100", "immunizations": "#e87ba4"}
    MM = {"conditions": "o", "encounters": "s", "medications": "^", "observations": "D", "immunizations": "v"}
    lim = 0.54; a2.plot([0, lim], [0, lim], color=AXIS, linewidth=0.9, zorder=1)
    for cls in CC:
        xs = [r["predicted_sensitivity"][cls] for r in acq["rows"] if cls in r["withheld"]]
        ys = [r["actual_change"][cls] for r in acq["rows"] if cls in r["withheld"]]
        a2.scatter(xs, ys, s=14, marker=MM[cls], color=CC[cls], alpha=0.7, edgecolor=SURFACE, linewidth=0.3, label=f"{cls} (n = {len(xs)})", zorder=3)
    a2.set_xlim(-0.01, lim); a2.set_ylim(-0.01, lim); a2.set_aspect("equal")
    a2.set_xlabel("Predicted sensitivity (mean |Δp| over 8 donor imputations)"); a2.set_ylabel("Realized change |p(revealed) − p(withheld)|")
    a2.legend(loc="lower right", fontsize=7.6, title="withheld class", title_fontsize=7.8)
    a2.set_title(f"b  v1 split — Spearman ρ = {acq['spearman_pred_vs_actual']:.2f}; 401 cases × 2 classes", fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(OUT / "fig3_acquisition.pdf"); fig.savefig(OUT / "fig3_acquisition.png"); plt.close(fig)


def fig4():
    s = json.load(open(DATA / "acquisition_sensitivity.v1.json"))
    items = []
    for m in ("4", "8", "16"):
        c = s["cells"]["m_donors"][m]; items.append((f"donor imputations M = {m}", c["ranking_accuracy"], c["included"], m == "8"))
    for k in ("v1 (no salt)", "s1:", "s2:", "s3:"):
        c = s["cells"]["donor_salt"][k]; items.append((f"donor identity: {'v1 order' if k.startswith('v1') else 'alternative ' + k[1]}", c["ranking_accuracy"], c["included"], k.startswith("v1")))
    for b in ("0.002", "0.005", "0.01", "0.02"):
        c = s["cells"]["indistinguishable_bar"][b]; items.append((f"indistinguishability bar {b}", c["ranking_accuracy"], c["included"], b == "0.005"))
    for o in ("0", "5"):
        c = s["cells"]["rotation_offset"][o]; items.append((f"pair-rotation offset {o}", c["ranking_accuracy"], c["included"], o == "0"))
    fig, ax = plt.subplots(figsize=(8.2, 5.2), dpi=300)
    ys = np.arange(len(items))[::-1]
    for yy, (lab, acc, inc, isv1) in zip(ys, items):
        ax.plot([0.5, acc], [yy, yy], color=GRID, linewidth=1.2, zorder=2)
        ax.plot(acc, yy, marker="D" if isv1 else "o", markersize=7 if isv1 else 6, color="#eb6834" if isv1 else "#2a78d6", markeredgecolor=SURFACE, zorder=3)
        ax.text(acc + 0.008, yy, f"{acc:.3f}  ({inc} evaluable)", fontsize=8, va="center", color=INK, family="DejaVu Sans Mono")
    ax.axvline(0.60, color="#d03b3b", linewidth=0.9, linestyle=(0, (4, 3))); ax.text(0.602, len(items) - 0.6, "usefulness bar", fontsize=7.8, color="#d03b3b")
    ax.set_yticks(ys); ax.set_yticklabels([i[0] for i in items], fontsize=8.5); ax.set_xlim(0.5, 1.12); ax.set_ylim(-0.7, len(items) - 0.3)
    ax.grid(axis="y", visible=False); ax.tick_params(axis="y", length=0); ax.set_xlabel("Ranking accuracy on the v1 split (one factor changed at a time)")
    ax.set_title(f"Protocol-parameter sensitivity — range {s['range_of_ranking_accuracy_across_all_cells'][0]:.3f}–{s['range_of_ranking_accuracy_across_all_cells'][1]:.3f}; "
                 "orange diamond = the reported v1 protocol", fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(OUT / "fig4_sensitivity.pdf"); fig.savefig(OUT / "fig4_sensitivity.png"); plt.close(fig)


def fig5():
    aci = json.load(open(DATA / "acquisition_ci_report.v1.json"))
    mf = json.load(open(DATA / "acquisition_report_manufacturing_p0.v1.json"))
    c0 = json.load(open(DATA / "acquisition_report_consumer_p0.v1.json")); c1 = json.load(open(DATA / "acquisition_report_consumer_p1.v1.json"))
    s = aci["summary"]["ranking_accuracy"]
    tasks = [("Healthcare P1\n(20 splits)", s["mean"], s["ci95"], aci["summary"]["pooled_excluded_indistinguishable"] / (aci["summary"]["pooled_included"] + aci["summary"]["pooled_excluded_indistinguishable"]), aci["summary"]["pooled_included"]),
             ("Manufacturing P0\n(1 split)", mf["ranking_accuracy"], None, mf["excluded_indistinguishable"] / mf["n_test_rows"], mf["included"]),
             ("Consumer P0\n(1 split)", c0["ranking_accuracy"], None, c0["excluded_indistinguishable"] / c0["n_test_rows"], c0["included"]),
             ("Consumer P1\n(1 split)", c1["ranking_accuracy"], None, c1["excluded_indistinguishable"] / c1["n_test_rows"], c1["included"])]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=300, gridspec_kw={"width_ratios": [1.3, 1]})
    xs = np.arange(len(tasks))
    for i, (lab, acc, cint, excl, inc) in enumerate(tasks):
        a1.bar(i, acc, width=0.58, color="#2a78d6", zorder=3)
        if cint:
            a1.errorbar(i, acc, yerr=[[acc - cint[0]], [cint[1] - acc]], color=INK, capsize=4, linewidth=1.2, zorder=4)
        top = (cint[1] if cint else acc) + 0.012
        a1.text(i, top, f"{acc:.3f}\n{inc:,} evaluable", ha="center", va="bottom", fontsize=8.2, color=INK)
    a1.axhline(0.60, color="#d03b3b", linewidth=0.9, linestyle=(0, (4, 3))); a1.text(-0.42, 0.607, "usefulness bar", fontsize=7.6, color="#d03b3b")
    a1.set_xticks(xs); a1.set_xticklabels([t[0] for t in tasks], fontsize=8.2); a1.set_ylim(0.5, 1.02); a1.set_ylabel("Ranking accuracy"); a1.grid(axis="x", visible=False); a1.tick_params(axis="x", length=0)
    a1.set_title("a  Reveal-validated ranking accuracy, per tested task", fontsize=9, loc="left")
    for i, (lab, acc, cint, excl, inc) in enumerate(tasks):
        a2.bar(i, excl * 100, width=0.58, color="#898781", zorder=3); a2.text(i, excl * 100 + 1, f"{excl*100:.0f}%", ha="center", fontsize=8.5, color=INK)
    a2.set_xticks(xs); a2.set_xticklabels([t[0] for t in tasks], fontsize=8.2); a2.set_ylim(0, 55); a2.set_ylabel("Cases excluded as indistinguishable (%)")
    a2.grid(axis="x", visible=False); a2.tick_params(axis="x", length=0); a2.set_title("b  Exclusion under the pre-set bar (0.005)", fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(OUT / "fig5_tasks.pdf"); fig.savefig(OUT / "fig5_tasks.png"); plt.close(fig)


def fig6():
    cal = json.load(open(DATA / "acquisition_calibration.v1.json"))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=300)
    bins = list(cal["accuracy_by_realized_gap"].items())
    xs = np.arange(len(bins))
    for i, (b, v) in enumerate(bins):
        a1.bar(i, v["accuracy"], width=0.6, color="#2a78d6", zorder=3); a1.text(i, v["accuracy"] + 0.012, f"{v['accuracy']:.2f}\nn = {v['n']}", ha="center", fontsize=8, color=INK)
    a1.axhline(0.5, color=INK2, linewidth=0.8); a1.set_xticks(xs); a1.set_xticklabels([b for b, _ in bins], fontsize=8)
    a1.set_ylim(0.4, 1.08); a1.set_xlabel("Realized gap between the two withheld classes  |Δ₁ − Δ₂|"); a1.set_ylabel("Ranking accuracy"); a1.grid(axis="x", visible=False); a1.tick_params(axis="x", length=0)
    a1.set_title("a  Accuracy by realized gap (v1 split; descriptive)", fontsize=9, loc="left")
    cls = list(cal["per_class"].items())
    for i, (c, v) in enumerate(cls):
        a2.plot([v["mean_predicted"], v["mean_actual"]], [i, i], color=GRID, linewidth=1.5, zorder=2)
        a2.plot(v["mean_predicted"], i, marker="o", color="#2a78d6", markersize=6, zorder=3, markeredgecolor=SURFACE)
        a2.plot(v["mean_actual"], i, marker="s", color="#eb6834", markersize=6, zorder=3, markeredgecolor=SURFACE)
    a2.set_yticks(range(len(cls))); a2.set_yticklabels([c for c, _ in cls], fontsize=8.5); a2.set_xscale("log"); a2.set_xlim(0.003, 0.4)
    a2.set_xlabel("Mean over withheld cases (log scale)"); a2.grid(axis="y", visible=False); a2.tick_params(axis="y", length=0)
    a2.legend(handles=[Line2D([0], [0], marker="o", color="#2a78d6", linestyle="", label="predicted sensitivity"), Line2D([0], [0], marker="s", color="#eb6834", linestyle="", label="realized change")], fontsize=8, loc="upper left", bbox_to_anchor=(0.0, 0.62))
    a2.set_title("b  Predicted vs realized, per class (v1 split)", fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(OUT / "fig6_calibration.pdf"); fig.savefig(OUT / "fig6_calibration.png"); plt.close(fig)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6):
        f(); print("ok", f.__name__)
