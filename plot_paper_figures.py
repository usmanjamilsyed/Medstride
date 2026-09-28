"""Re-plot key paper results from paper_data/*.csv into results/."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
D, OUT = ROOT / "paper_data", ROOT / "results"
OUT.mkdir(exist_ok=True)

# Fig 7-style: T1.2 modality-specific ASR at eps=1.0
t1 = pd.read_csv(D / "t1_2_wesad_results.csv")
t1 = t1[t1.epsilon == 1.0].set_index("model")[["ECG_ASR", "BVP_ASR", "ACC_ASR"]] * 100
t1.plot(kind="bar", figsize=(7, 4))
plt.ylabel("Targeted ASR (%)"); plt.title("T1.2: modality-specific attack success (eps=1.0)")
plt.xticks(rotation=0); plt.tight_layout(); plt.savefig(OUT / "t1_2_asr_by_modality.png", dpi=150); plt.close()

# Fig 9: T4.2 targeted PGD
t4 = pd.read_csv(D / "t4_2_targeted_pgd.csv")
plt.figure(figsize=(6, 4)); plt.plot(t4.epsilon, t4.asr * 100, "o-")
plt.xlabel("Perturbation budget eps"); plt.ylabel("Targeted ASR (%)")
plt.title("T4.2: targeted PGD alert suppression"); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig(OUT / "t4_2_targeted_pgd.png", dpi=150); plt.close()

# Fig 10: safety agent
s = pd.read_csv(D / "t4_2_safety_agent.csv")
w = 0.002
plt.figure(figsize=(6, 4))
plt.bar(s.epsilon - w/2, s.interception_rate * 100, w, label="Safety interception")
plt.bar(s.epsilon + w/2, s.residual_unsafe_rate * 100, w, label="Residual unsafe")
plt.xlabel("Perturbation budget eps"); plt.ylabel("Rate among successful attacks (%)")
plt.title("T4.2: safety-agent containment"); plt.legend()
plt.tight_layout(); plt.savefig(OUT / "t4_2_safety_agent.png", dpi=150); plt.close()

# Fig 11: T6.2 memory architectures
m = pd.read_csv(D / "t6_2_memory_architectures.csv").pivot(index="architecture", columns="attack", values="MPSR")
m = m.loc[["Global", "Provenance", "Scoped", "Secure"]] * 100
m.plot(kind="bar", figsize=(6, 4)); plt.ylabel("Memory-poisoning success rate (%)")
plt.title("T6.2: memory architectures"); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(OUT / "t6_2_memory_architectures.png", dpi=150); plt.close()
print("Figures saved in", OUT)
