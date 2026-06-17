import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DU SYSTÈME ---
labels = ["Climat", "Économie", "Population"]
n_systems = len(labels)
B0 = np.array([100.0, 100.0, 100.0])
R = np.array([40.0, 60.0, 50.0])
k = np.array([-0.08, 0.02, 0.01]) # Le climat décline naturellement

# Matrice de couplage
M = np.zeros((n_systems, n_systems))
M[1, 0] = 0.45  # Climat -> Économie
M[2, 1] = 0.60  # Économie -> Population

# Paramètres de simulation
T_max = 50.0
dt = 0.01
time_steps = np.arange(0, T_max + dt, dt)
n_steps = len(time_steps)

def run_simulation(with_control=False):
    B_history = np.zeros((n_steps, n_systems))
    B_history[0] = B0
    u_history = np.zeros(n_steps)
    
    # Paramètres du contrôleur optimal (Pontryagin proxy)
    # Plus R[0] est grand, plus le gain est lissé pour simuler le coût de l'effort
    gain_controle = 0.15 / (1.0 + 0.01 * R[0]) 
    
    for t in range(1, n_steps):
        B_prev = B_history[t-1].copy()
        dB = np.zeros(n_systems)
        
        # Calcul du contrôle actif sur le Climat (système 0)
        u = 0.0
        if with_control:
            # L'effort est proportionnel au déficit du climat
            erreur = 100.0 - B_prev[0]
            u = max(0.0, gain_controle * erreur) 
        u_history[t] = u
        
        for i in range(n_systems):
            if B_prev[i] <= 0:
                B_history[t:, i] = 0
                continue
            
            # Application du contrôle u(t) uniquement sur le système 0 (Climat)
            if i == 0:
                term_propre = (k[i] + u) * (B_prev[i] + R[i])
            else:
                term_propre = k[i] * (B_prev[i] + R[i])
            
            # Couplage tensoriel
            term_couplage = 0.0
            for j in range(n_systems):
                if i != j:
                    term_couplage += M[i, j] * (B_prev[j] - 100.0)
            
            dB[i] = (term_propre + term_couplage) * dt
            
        B_next = B_prev + dB
        B_next[B_next < 0] = 0
        B_history[t] = B_next
        
    return B_history, u_history

# --- RECHERCHE DES DEUX SCÉNARIOS ---
B_sans, _ = run_simulation(with_control=False)
B_avec, u_actuel = run_simulation(with_control=True)

# --- GRAPHIQUE COMPARATIF ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

colors = ['#2ca02c', '#1f77b4', '#d62728']

# Plot 1 : Sans Contrôle (Effondrement)
for i in range(n_systems):
    ax1.plot(time_steps, B_sans[:, i], color=colors[i], linestyle='--', alpha=0.6)
    ax1.plot(time_steps, B_avec[:, i], color=colors[i], linewidth=2.5, label=f"{labels[i]} (Contrôlé)")

ax1.axhline(y=100, color='black', linestyle=':', alpha=0.5, label="Cible de Stabilité")
ax1.set_title("Contrôle Optimal de la Fluctuodynamique : Sauvegarde du Système vs Effondrement Libres (Pointillés)", fontsize=13)
ax1.set_ylabel("Niveau des Bases B_i(t)", fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='lower left', fontsize=10)

# Plot 2 : Effort de contrôle u(t) appliqué
ax2.plot(time_steps, u_actuel, color='purple', linewidth=2, label="Effort de contrôle $u(t)$ (Ajustement IFPR)")
ax2.set_title("Profil de l'Effort de Contrôle Optimal Injecté au cours du temps", fontsize=13)
ax2.set_xlabel("Temps (t)", fontsize=11)
ax2.set_ylabel("Intensité de u(t)", fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(fontsize=10)

plt.tight_layout()
plt.show()