import pygame

class Player:
    def __init__(self, x, y, image_path):
        self.original_image = pygame.image.load(image_path).convert_alpha() # Charger l'image de la soucoupe
        self.original_image = pygame.transform.scale(self.original_image, (90, 90)) # Redimensionne la soucoupe
        
        self.image = self.original_image.copy() # Image courante (modifiable lors de l'explosion)

        self.rect = self.image.get_rect(center=(x, y)) # Création d'un rectangle autour de la soucoupe
        self.rect = self.rect.inflate(0 , -35) # Modifie la hauteur du rectangle 
        self.can_jump = True
        self.hitbox = None
        
        self.vy = 0                 # Vitesse verticale
        self.gravity = 0.3          # Gravité
        self.jump_strength = -7     # Saut

        
        self.explosion_frames = [] # Liste vide qui va contenir toutes les images nécessaires pour l'explosion
        for i in range(1, 22):
            img = pygame.image.load(f"EXPLOSIONS/explo{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (90, 90))
            self.explosion_frames.append(img) # Implémentation de l'image d'un bout d'explosion dans la liste 

        self.explosion_index = 0
        self.exploding = False
        self.explosion_speed = 0.6

        # Animation soucoupe flottante dans menu
        self.float_angle = 0
        self.float_speed = 0.05
        self.float_amplitude = 8

    # Animation explosion
    def update_explosion(self):
        if self.exploding:
            self.explosion_index += self.explosion_speed
            # Fin de l'animation
            if self.explosion_index >= len(self.explosion_frames):
                self.exploding = False
                self.explosion_index = len(self.explosion_frames) - 1

            # Frame affichée
            self.image = self.explosion_frames[int(self.explosion_index)]


    def draw_hitbox(self, window):
        """Dessine la hitbox réduite de la soucoupe"""
        self.hitbox = pygame.draw.rect(window, (0,255, 255), (self.rect.x + 10, self.rect.y + 20, 73, 45), 2)
                     
    def jump(self):
        """Fait sauter la soucoupe"""
        if self.can_jump:
            self.vy = self.jump_strength


    def update(self):
        """Mettre à jour la position du joueur."""
        self.vy += self.gravity
        self.rect.y += self.vy

    def draw(self, window):
        """Dessin de la soucoupe dans la fenêtre."""
        window.blit(self.image, self.rect)

    def apply_gravity(self, ground_y):
        """Fait subir la gravité sur le joueur"""
        if self.exploding:
            return  # Freeze pendant explosion
        # Gravité
        self.vy += self.gravity
        self.rect.y += self.vy

        # Limite de sol 
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y 
            self.vy = 0
            self.can_jump = False  # Pas de saut au sol
            self.exploding = True
            self.explosion_index = 0
            return

        # Limite du plafond
        elif self.rect.top <= -20: # -20 car avec 0 ça marche pas
            self.rect.top = -20
            self.vy = 0
            self.can_jump = False  # Pas de saut au plafond
            self.exploding = True
            self.explosion_index = 0
            return
        
        else:
            # Dans les airs → peut sauter uniquement si vitesse < 0 
            self.can_jump = True

