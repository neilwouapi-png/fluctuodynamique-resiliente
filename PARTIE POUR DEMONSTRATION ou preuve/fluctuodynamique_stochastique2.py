import numpy as np
import matplotlib.pyplot as plt

# --- PARAMÈTRES DE LA SIMULATION ---
B0 = 100.0          # Base initiale
R = 50.0            # Résilience
k = 0.02            # Tendance déterministe légèrement positive (croissance lente)
sigma = 0.25        # Volatilité élevée (gros chocs aléatoires)
T_max = 15.0        # Horizon temporel
dt = 0.01           # Pas de temps
n_trajectories = 100 # Nombre de mondes parallèles à simuler

# Axe temporel
time_steps = np.arange(0, T_max + dt, dt)
n_steps = len(time_steps)

# Matrice pour stocker toutes les trajectoires (Lignes: Temps, Colonnes: Trajectoires)
B = np.zeros((n_steps, n_trajectories))
B[0, :] = B0

# Indicateur pour savoir si une trajectoire s'est effondrée
collapsed = np.zeros(n_trajectories, dtype=bool)

# --- SIMULATION VECTORISÉE (EULER-MARUYAMA) ---
for t in range(1, n_steps):
    # Génération du bruit brownien pour TOUTES les trajectoires d'un coup
    Z = np.random.normal(0, 1, n_trajectories)
    dW = Z * np.sqrt(dt)
    
    # Équation d'Itô appliquée à ton framework
    # dB = k*(B+R)*dt + sigma*(B+R)*dW
    dB = k * (B[t-1, :] + R) * dt + sigma * (B[t-1, :] + R) * dW
    B[t, :] = B[t-1, :] + dB
    
    # Application de la barrière d'effondrement physique (B <= 0)
    # Si une trajectoire a touché 0 au coup d'avant, elle reste à 0 (état absorbant)
    B[t, B[t-1, :] <= 0] = 0

# --- ANALYSE DES RÉSULTATS ---
# Une trajectoire est effondrée si sa valeur finale est égale à 0
collapsed_final = B[-1, :] <= 0
prob_collapse = np.mean(collapsed_final) * 100

# --- GRAPHIQUE ---
plt.figure(figsize=(14, 7))

# Trajectoire déterministe moyenne pour comparaison
B_det = -R + (B0 + R) * np.exp(k * time_steps)
plt.plot(time_steps, B_det, color='black', linewidth=3, label="Tendance Déterministe Théorique", zorder=5)

# Affichage des trajectoires stochastiques
for j in range(n_trajectories):
    if collapsed_final[j]:
        plt.plot(time_steps, B[:, j], color='crimson', alpha=0.15) # Rouge si effondrement
    else:
        plt.plot(time_steps, B[:, j], color='teal', alpha=0.2)     # Bleu/Vert si survie

# Lignes de repère
plt.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
plt.axhline(y=-R, color='purple', linestyle=':', label=f"Asymptote de rupture -R (-{R})")

plt.title(f"Extension Stochastique de la Fluctuodynamique ({n_trajectories} simulations)\n"
          f"Volatilité $\sigma$ = {sigma} | Probabilité d'effondrement final = {prob_collapse:.1f}%", fontsize=14)
plt.xlabel("Temps (t)", fontsize=12)
plt.ylabel("Base B(t)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11, loc='upper left')

plt.show()