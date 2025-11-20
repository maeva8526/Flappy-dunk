import pygame

class Player:
    def __init__(self, x, y, image_path):
        # Charger l'image de la soucoupe
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect(center=(x, y))

        self.height = 60

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

    def apply_gravity(self, ground_y):
        # Applique la gravité et gère la collision avec le sol
        self.vy += self.gravity
        # On ajoute la gravité à la vitesse verticale
        self.rect.y += self.vy
        # On met à jour la position verticale
        if self.rect.bottom + self.height >= ground_y:
            # Si le bas du joueur passe sous le sol
            self.rect.bottom = ground_y - self.height
            # On replace le joueur juste sur le sol
            self.vy = 0
            # On annule la vitesse verticale
            self.on_ground = True
            # On indique qu'il est au sol
        else:
            self.on_ground = False
            # Sinon, il est en l'air