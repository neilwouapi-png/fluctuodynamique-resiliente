import matplotlib.pyplot as plt
from core import Fluctuodynamique

# 1. Configuration des scénarios
t_max = 50
pas = 0.01

print("--- Lancement des simulations de la Fluctuodynamique Résiliente ---")

# Cas 1 : Déclin Déterministe tendant vers -R
sys_det = Fluctuodynamique(B0=10.0, R=15.0, k=-0.05)
t_det, B_det = sys_det.simuler_deterministe(t_max, pas)

# Cas 2 : Risque Stochastique d'Itô (Effondrement de Premier Passage)
sys_stoch = Fluctuodynamique(B0=10.0, R=5.0, k=0.02, sigma=0.25)
t_stoch, B_stoch = sys_stoch.simuler_stochastique_ito(t_max, pas, seed=42)

# Cas 3 : Contrôle de Pontryagin (Stabilisation active)
sys_ctrl = Fluctuodynamique(B0=10.0, R=20.0, k=-0.08)
t_ctrl, B_ctrl = sys_ctrl.simuler_controle_pontryagin(t_max, pas, gamma=1.0)

# 2. Génération des graphiques
plt.figure(figsize=(12, 8))

plt.plot(t_det, B_det, label="Déterministe (k = -0.05, R = 15) -> Asymptote -R", color="blue", lw=2)
plt.plot(t_stoch, B_stoch, label="Stochastique Itô (k = 0.02, σ = 0.25, R = 5) -> Effondrement", color="red", lw=1.5)
plt.plot(t_ctrl, B_ctrl, label="Contrôle Pontryagin (Rétroaction Active)", color="green", lw=2, linestyle="--")

plt.axhline(0, color="black", linestyle=":", label="Seuil Critique de Viabilité (B=0)")
plt.title("Preuves Empiriques de la Fluctuodynamique Résiliente", fontsize=14, fontweight="bold")
plt.xlabel("Temps (t)", fontsize=12)
plt.ylabel("Base du Système (B)", fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# Sauvegarde de la figure pour le GitHub
plt.savefig("simulation_results.png", dpi=300)
print("Graphique sauvegardé avec succès : simulation_results.png")
plt.show()