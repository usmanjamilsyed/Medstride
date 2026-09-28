"""Harm-Weighted Residual Risk (HWRR), Eq. (1) and Table 18 of the MedSTRIDE-AI paper.

HWRR = sum_i(w_i * r_i) / sum_i(w_i)
w_i: ISO 14971-inspired severity weight (Medium=2, High=3)
r_i: residual unsafe rate of threat i (values taken from paper Tables 14, 16, 17).
Writes results/hwrr_table18.csv and results/figure12_risk_aware_ids.png
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "results"
OUT.mkdir(exist_ok=True)

threats = pd.DataFrame({
    "threat": ["T1.2", "T4.2", "T6.2"],
    "tier": ["Medium", "High", "High"],
    "w": [2, 3, 3],
    "r_no_response": [0.6066, 1.0, 1.0],
    "r_risk_aware": [0.0164, 0.1622, 0.75],
})

def hwrr(w, r):
    return float((w * r).sum() / w.sum())

base = hwrr(threats.w, threats.r_no_response)
aware = hwrr(threats.w, threats.r_risk_aware)
reduction = 100 * (base - aware) / base
print(f"HWRR no response : {base:.4f}")
print(f"HWRR risk-aware  : {aware:.4f}")
print(f"Reduction        : {reduction:.1f}%")

table = threats.copy()
table.loc[len(table)] = ["HWRR", "-", "-", round(base, 4), round(aware, 4)]
table.to_csv(OUT / "hwrr_table18.csv", index=False)

fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [2, 1]})
x = range(3)
a.bar([i - 0.2 for i in x], threats.r_no_response * 100, 0.4, label="No response")
a.bar([i + 0.2 for i in x], threats.r_risk_aware * 100, 0.4, label="Risk-aware response")
a.set_xticks(list(x))
a.set_xticklabels([f"{t}\n({k})" for t, k in zip(threats.threat, threats.tier)])
a.set_ylabel("Residual unsafe rate (%)")
a.set_title("(a) Per-threat residual unsafe rate")
a.legend()
b.bar(["No\nresponse", "Risk-aware\nresponse"], [base * 100, aware * 100], color=["#1f77b4", "#ff7f0e"])
b.set_ylabel("HWRR (%)")
b.set_title(f"(b) HWRR (-{reduction:.0f}%)")
plt.tight_layout()
plt.savefig(OUT / "figure12_risk_aware_ids.png", dpi=150)
