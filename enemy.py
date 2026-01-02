import pygame # On importe pygame pour utiliser Rect et les fonctions de dessin


class Enemy: # Classe qui représente un ennemi simple
   
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha() # Charger l'image de la météorite
        self.image = pygame.transform.scale(self.image, (90, 90)) # Redimensionne la météorite

        self.rect = self.image.get_rect(center=(x, y)) # Création d'un rectangle autour de la météorite
        
        self.hitbox = pygame.Rect(0,0,0,0) # Création d'une hitbox vide pour éviter des bugs
        self.speed = 3 # Vitesse de départ de la météorite

    def draw_hitbox(self, window):
        """Dessine la hitbox de la météorite"""
        self.hitbox = pygame.draw.rect(window, 0, (self.rect.x + 10, self.rect.y + 10, 70, 70), 2)

    def move(self, difficulty = 0):
        """Déplace la météorite vers la gauche en fonction de la difficulté."""
        self.rect.x -= self.speed + difficulty * 0.1

        # Mettre à jour la hitbox si nécessaire
        self.hitbox.topleft = self.rect.topleft

    def draw(self, window):
        """Dessin de la météorite dans la fenêtre."""
        window.blit(self.image, self.rect)