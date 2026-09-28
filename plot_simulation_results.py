"""Plot T6.2 shared-memory simulation outputs (results/memory-simulation/*.csv)."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
S = ROOT / "results" / "memory-simulation"
OUT = ROOT / "results" / "simulation"
OUT.mkdir(parents=True, exist_ok=True)

# 1. Memory-poisoning success rate per architecture
a = pd.read_csv(S / "ablation_summary_df.csv")
p = a.pivot(index="Architecture", columns="Attack", values="MPSR").loc[["global", "provenance", "scoped", "secure"]] * 100
p.plot(kind="bar", figsize=(6.5, 4)); plt.ylabel("Memory-poisoning success rate (%)")
plt.title("Simulation: MPSR by memory architecture"); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(OUT / "sim_mpsr_by_architecture.png", dpi=150); plt.close()

# 2. Poison persistence over time
t = pd.read_csv(S / "persistence_table.csv")
plt.figure(figsize=(6.5, 4))
for arch, g in t.groupby("architecture"):
    plt.plot(g.time, g.Poison_Active_Rate * 100, marker="o", label=arch)
plt.xlabel("Time step after injection"); plt.ylabel("Poison active (%)")
plt.title("Simulation: poison persistence (TTL limits exposure)"); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig(OUT / "sim_poison_persistence.png", dpi=150); plt.close()

# 3. TTL sensitivity
l = pd.read_csv(S / "ttl_summary.csv")
plt.figure(figsize=(6, 4)); plt.plot(l.ttl, l.Poison_Active_Rate * 100, "o-")
plt.xlabel("TTL (time steps)"); plt.ylabel("Poison-active rate (%)")
plt.title("Simulation: TTL sensitivity"); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig(OUT / "sim_ttl_sensitivity.png", dpi=150); plt.close()

# 4. Semantic-validation utility cost
u = pd.read_csv(S / "utility_summary.csv")
plt.figure(figsize=(6, 4)); plt.bar(u.threshold.astype(str), u.Legitimate_Rejection_Rate * 100)
plt.xlabel("Glucose-change threshold"); plt.ylabel("Legitimate updates rejected (%)")
plt.title("Simulation: semantic validation utility cost")
plt.tight_layout(); plt.savefig(OUT / "sim_semantic_utility_cost.png", dpi=150); plt.close()
print("saved", sorted(x.name for x in OUT.iterdir()))
