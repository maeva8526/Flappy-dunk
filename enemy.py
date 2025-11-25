import pygame# On importe pygame pour utiliser Rect et les fonctions de dessin


class Enemy:# Classe qui représente un ennemi simple
   
    def __init__(self, x, y, image_path):
        # Charger l'image de la soucoupe
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect(center=(x, y))
        
        self.height = 60

   
    def move(self):
        self.rect.x -= 3

    def draw(self, window):
        """Dessin de la météorite dans la fenêtre."""
        window.blit(self.image, self.rect)