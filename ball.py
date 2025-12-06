import pygame

class Player:
    def __init__(self, x, y, image_path):
        # Charger l'image de la soucoupe
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect = self.rect.inflate(0 , -35) #modifier la hauteur du rectangle 
        self.can_jump = True
        self.hitbox = None
        # Physique
        self.vy = 0                 # vitesse verticale
        self.gravity = 0.3          # gravité
        self.jump_strength = -7     # saut

        # --- ANIMATION EXPLOSION ---
        self.explosion_frames = []
        for i in range(1, 22):
            img = pygame.image.load(f"EXPLOSIONS/explo{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (90, 90))
            self.explosion_frames.append(img)

        self.explosion_index = 0
        self.exploding = False
        self.explosion_speed = 0.6

    # ANIMATION EXPLOSION
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
        """Dessine la hitbox réduite de la soucoupe (pour debug)."""
        self.hitbox = pygame.draw.rect(window, (0,255, 255), (self.rect.x + 10, self.rect.y + 20, 73, 45), 2)
                     
    def jump(self):
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
        if self.exploding:
            return  # freeze pendant explosion
        # Gravité
        self.vy += self.gravity
        self.rect.y += self.vy

        # ---- SOL ----
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y 
            self.vy = 0
            self.can_jump = False  # pas de saut au sol
            self.exploding = True
            self.explosion_index = 0
            return

        # ---- PLAFOND ----
        elif self.rect.top <= -20: #-20 car avec 0 ça marche pas
            self.rect.top = -20
            self.vy = 0
            self.can_jump = False  # pas de saut au plafond
            self.exploding = True
            self.explosion_index = 0
            return
        
        else:
            # Dans les airs → peut sauter uniquement si vitesse < 0 (pendant un vrai saut)
            self.can_jump = True

