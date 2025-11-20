import pygame

import pygame

class Player:
    def __init__(self, x, y, image_path):
        # Charger l'image de la soucoupe
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Physique
        self.vy = 0                 # vitesse verticale
        self.gravity = 0.4          # gravité
        self.jump_strength = -7     # saut

    def jump(self):
        """Lancer un saut vers le haut."""
        self.vy = self.jump_strength

    def update(self):
        """Mettre à jour la position du joueur."""
        self.vy += self.gravity
        self.rect.y += self.vy

    def draw(self, window):
        """Dessin de la soucoupe dans la fenêtre."""
        window.blit(self.image, self.rect)
