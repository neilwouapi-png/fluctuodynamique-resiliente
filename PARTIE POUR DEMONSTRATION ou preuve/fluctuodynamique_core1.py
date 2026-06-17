import numpy as np
import matplotlib.pyplot as plt

def analytical_solution(t, B0, R, k):
    """Solution analytique exacte du cours pour un IFPR constant."""
    return -R + (B0 + R) * np.exp(k * t)

def simulate_system(B0, R, k, T_max, dt):
    """Simulation numérique par la méthode d'Euler de l'équation fondamentale."""
    time_steps = np.arange(0, T_max + dt, dt)
    B_num = np.zeros(len(time_steps))
    B_num[0] = B0
    
    for i in range(1, len(time_steps)):
        # Équation fondamentale: dB/dt = IFPR * (B + R)
        dB = k * (B_num[i-1] + R) * dt
        B_num[i] = B_num[i-1] + dB
        
        # Condition d'effondrement physique (B ne peut pas être négatif en réalité)
        if B_num[i] <= 0:
            B_num[i:] = 0
            break
            
    return time_steps, B_num

# --- CONFIGURATION DES PARAMÈTRES ---
B0 = 100.0      # Base initiale
R = 50.0        # Seuil de résilience constant
T_max = 30.0    # Temps max de simulation
dt = 0.01       # Pas de temps

scenarios = {
    "Croissance Exponentielle (k = 0.1)": 0.1,
    "Déclin Modéré (k = -0.05)": -0.05,
    "Effondrement (k = -0.8)": -0.8
}

# --- GRAPHIQUE ---
plt.figure(figsize=(12, 8))

for label, k in scenarios.items():
    # Simulation numérique
    t_steps, B_num = simulate_system(B0, R, k, T_max, dt)
    # Calcul analytique pour comparaison
    B_anal = analytical_solution(t_steps, B0, R, k)
    
    # On masque les valeurs après effondrement pour le propre du graphique
    valid_idx = B_num > 0
    
    # Plot Numérique vs Analytique
    p = plt.plot(t_steps[valid_idx], B_num[valid_idx], label=f"{label} (Num)", linewidth=2)
    plt.plot(t_steps[valid_idx], B_anal[valid_idx], '--', color=p[0].get_color(), 
             label=f"{label} (Théorique)", alpha=0.7)

# Ligne de la résilience critique (Asymptote -R)
plt.axhline(y=-R, color='r', linestyle=':', label=f"Asymptote critique -R (-{R})")
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

plt.title("Validation Numérique de l'Équation Fondamentale de la Fluctuodynamique", fontsize=14)
plt.xlabel("Temps (t)", fontsize=12)
plt.ylabel("Base B(t)", fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(fontsize=10)
plt.show()