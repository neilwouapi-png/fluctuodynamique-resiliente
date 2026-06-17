import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DU RÉSEAU (MODÈLE TERRE) ---
labels = ["Climat", "Économie", "Population"]
n_systems = len(labels)

# États initiaux et résiliences
B0 = np.array([100.0, 100.0, 100.0])
R = np.array([40.0, 60.0, 50.0])

# Tendances intrinsèques (Sans couplage, l'économie et la pop veulent croître, le climat décline)
k = np.array([-0.08, 0.02, 0.01]) 

# Matrice de Couplage M[i, j] : Impact de j sur i
# M[1, 0] = 0.4 -> L'Économie (1) dépend fortement du Climat (0)
# M[2, 1] = 0.6 -> La Population (2) dépend fortement de l'Économie (1)
M = np.zeros((n_systems, n_systems))
M[1, 0] = 0.45  # Climat -> Économie
M[2, 1] = 0.60  # Économie -> Population

# --- PARAMÈTRES DE SIMULATION ---
T_max = 50.0
dt = 0.01
time_steps = np.arange(0, T_max + dt, dt)
n_steps = len(time_steps)

# Historique des bases (Lignes: Temps, Colonnes: Systèmes)
B_history = np.zeros((n_steps, n_systems))
B_history[0] = B0

# --- SIMULATION NUMÉRIQUE DE LA CASCADE ---
for t in range(1, n_steps):
    B_prev = B_history[t-1].copy()
    dB = np.zeros(n_systems)
    
    for i in range(n_systems):
        if B_prev[i] <= 0:
            B_history[t:, i] = 0 # Déjà effondré
            continue
            
        # 1. Dynamique interne propre
        term_propre = k[i] * (B_prev[i] + R[i])
        
        # 2. Impact du couplage tensoriel (Écart par rapport à la référence stable 100)
        term_couplage = 0.0
        for j in range(n_systems):
            if i != j:
                # Si le système j est dégradé (< 100), il applique une force négative sur i
                term_couplage += M[i, j] * (B_prev[j] - 100.0)
        
        dB[i] = (term_propre + term_couplage) * dt
        
    # Mise à jour globale
    B_next = B_prev + dB
    B_next[B_next < 0] = 0 # Seuil d'effondrement
    B_history[t] = B_next

# --- GRAPHIQUE DES EFFONDREMENTS EN CASCADE ---
plt.figure(figsize=(12, 6))
colors = ['#2ca02c', '#1f77b4', '#d62728'] # Vert pour Climat, Bleu pour Éco, Rouge pour Pop

for i in range(n_systems):
    plt.plot(time_steps, B_history[:, i], label=labels[i], color=colors[i], linewidth=2.5)

plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.title("Simulation de la Fluctuodynamique : Effondrement en Cascade (Modèle Terre)", fontsize=14)
plt.xlabel("Temps (t)", fontsize=12)
plt.ylabel("Niveau des Bases B_i(t)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=12)
plt.show()