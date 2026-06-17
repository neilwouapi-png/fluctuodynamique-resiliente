import numpy as np

class Fluctuodynamique:
    def __init__(self, B0, R, k, sigma=0.0):
        """
        Initialise le système de Fluctuodynamique Résiliente.
        B0    : Base initiale
        R     : Masse résiliente
        k     : Valeur de l'IFPR (Indice de Fluctuation Pondérée Relative)
        sigma : Volatilité environnementale (pour le modèle stochastique)
        """
        self.B0 = B0
        self.R = R
        self.k = k
        self.sigma = sigma

    def simuler_deterministe(self, t_max, pas):
        """Calcule la trajectoire analytique exacte."""
        t = np.arange(0, t_max, pas)
        B = -self.R + (self.B0 + self.R) * np.exp(self.k * t)
        return t, B

    def simuler_stochastique_ito(self, t_max, pas, seed=None):
        """Simule la trajectoire stochastique via le schéma d'Euler-Maruyama (Lemme d'Itô)."""
        if seed is not None:
            np.random.seed(seed)
            
        t = np.arange(0, t_max, pas)
        N = len(t)
        B = np.zeros(N)
        B[0] = self.B0
        
        dt = pas
        for i in range(1, N):
            if B[i-1] <= 0:  # Barrière absorbante de viabilité (Effondrement)
                B[i-1:] = 0
                break
            
            # Formule d'Itô discrétisée
            dW = np.random.normal(0, np.sqrt(dt))
            moteur_dynamique = B[i-1] + self.R
            dB = self.k * moteur_dynamique * dt + self.sigma * moteur_dynamique * dW
            B[i] = B[i-1] + dB
            
        return t, B

    def simuler_controle_pontryagin(self, t_max, pas, gamma):
        """Applique le contrôle optimal de Pontryagin pour neutraliser le déclin."""
        t = np.arange(0, t_max, pas)
        N = len(t)
        B = np.zeros(N)
        B[0] = self.B0
        
        dt = pas
        # Trajectoire de contrôle simulée par rétroaction directe u*(t) = -k
        for i in range(1, N):
            u_optimal = -self.k  # Annulation active de la dérive négative
            dB = (self.k + u_optimal) * (B[i-1] + self.R) * dt
            B[i] = B[i-1] + dB
            
        return t, B