import pygame

class Player:
    def __init__(self, x, y, image_path):
        self.original_image = pygame.image.load(image_path).convert_alpha() # Charger l'image de la soucoupe
        self.original_image = pygame.transform.scale(self.original_image, (90, 90)) # Redimensionne la soucoupe
        
        self.image = self.original_image.copy() # Image courante (modifiable lors de l'explosion)

        self.rect = self.image.get_rect(center=(x, y)) # Création d'un rectangle autour de la soucoupe
        self.rect = self.rect.inflate(0 , -35) # Modifie la hauteur du rectangle 
        self.can_jump = True # Booléen pour savoir si la soucoupe peut sauter 
        self.hitbox = None # Création d'une hitbox vide pour éviter des bugs
        
        self.vy = 0                 # Vitesse verticale
        self.gravity = 0.3          # Gravité
        self.jump_strength = -7     # Saut

        
        self.explosion_frames = [] # Liste vide qui va contenir toutes les images nécessaires pour l'explosion
        for i in range(1, 22):
            img = pygame.image.load(f"EXPLOSIONS/explo{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (90, 90))
            self.explosion_frames.append(img) # Implémentation de l'image d'un bout d'explosion dans la liste 

        self.explosion_index = 0 # Indice de l’image actuelle dans l’animation de l’explosion
        self.exploding = False # Indique si le joueur est en train d’exploser ou non
        self.explosion_speed = 0.6 # Indique si le joueur est en train d’exploser ou non

        # Animation soucoupe flottante dans menu
        self.float_angle = 0 # Angle utilisé pour calculer le mouvement sinusoïdal
        self.float_speed = 0.05 # Vitesse du flottement
        self.float_amplitude = 8 # Amplitude du flottement

    # Animation explosion
    def update_explosion(self):
        if self.exploding: # Si la soucoupe explose car elle a eu une collision 
            self.explosion_index += self.explosion_speed # Alors on ajoute à l'index la vitesse de l'animation 
            # Fin de l'animation
            if self.explosion_index >= len(self.explosion_frames): # Si index est plus grand que le nombre d'images d'explosion
                self.exploding = False # Alors on arrête l'explosion
                self.explosion_index = len(self.explosion_frames) - 1 # Bloque l’index sur la dernière image de l’explosion

            # Image de la soucoupe remplacée par l'image actuel d'explosion
            self.image = self.explosion_frames[int(self.explosion_index)]


    def draw_hitbox(self, window):
        """Dessine la hitbox réduite de la soucoupe"""
        self.hitbox = pygame.draw.rect(window, (0,255, 255), (self.rect.x + 10, self.rect.y + 20, 73, 45), 2)
                     
    def jump(self):
        """Fait sauter la soucoupe"""
        if self.can_jump:
            self.vy = self.jump_strength
            
    def draw(self, window):
        """Dessin de la soucoupe dans la fenêtre. (Mais aussi les images d'explosions quand il y a une collision)"""
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
            self.rect.bottom = ground_y # On arrête la soucoupe au sol, elle ne peut pas descendre plus bas
            self.vy = 0  # On met la vitesse verticale à 0 (la soucoupe ne peux plus bouger)
            self.can_jump = False  # Pas de saut au sol
            self.exploding = True # Collision avec le sol 
            self.explosion_index = 0 # On met l'index d'explosion à la première image
            return

        # Limite du plafond
        elif self.rect.top <= -20: # -20 car avec 0 ça marche pas
            self.rect.top = -20 # On arrête la soucoupe au plafond, elle ne peut pas monter plus haut
            self.vy = 0 # On met la vitesse verticale à 0 (la soucoupe ne peux plus bouger)
            self.can_jump = False  # Pas de saut au plafond
            self.exploding = True # Collision avec le plafond 
            self.explosion_index = 0 # On met l'index d'explosion à la première image
            return
        
        else:
            # Dans les airs → peut sauter uniquement si vitesse < 0 
            self.can_jump = True

