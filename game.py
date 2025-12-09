import pygame
# On importe la bibliothèque pygame pour gérer la fenêtre et le jeu
import math
from player import Player
from enemy import Enemy
from random import randint

class Game:
    # Déclaration de la classe Game, qui va gérer l'ensemble du jeu
    def __init__(self):
        # Méthode constructeur, appelée quand on crée un objet Game
        self.width = 430
        # Largeur de la fenêtre en pixels
        self.height = 670
        # Hauteur de la fenêtre en pixels
        self.window = pygame.display.set_mode((self.width, self.height))
        # Création de la fenêtre Pygame avec la taille (largeur, hauteur)
        pygame.display.set_caption("Flappy Space")
        # Définition du titre de la fenêtre
        # FOND
        self.fond = pygame.image.load("fond_etoile.png").convert_alpha()
        self.fond = pygame.transform.scale(self.fond, (430, 670))
        # Positions initiales des deux fonds
        self.fond_x1 = 0
        self.fond_x2 = self.width
        self.fond_speed = 2

        self.clock = pygame.time.Clock()
        # Objet Clock pour limiter le nombre d'images par seconde
        self.running = True
        # Booléen qui indique si la boucle principale doit continuer
        self.state = "menu"
        # Etat du jeu : "menu" pour l'instant, plus tard "play"
        self.ground_y = 670
        # Position verticale du sol (Taille de l'écran + taille de la soucoupe)
        self.title_img = pygame.image.load("title.png").convert_alpha() #titre
        self.title_img = pygame.transform.scale(self.title_img, (450, 150))

        #  press_start chargé 
        self.start_img = pygame.image.load("start.gif").convert_alpha()
        self.start_img = pygame.transform.scale(self.start_img, (250, 90))

        # Alpha pour faire clignoter le press start 
        self.start_alpha = 255
        self.alpha_direction = -5

        # Joueur et ennemis
        self.player = None
        self.enemies = []

        self.start_x = 100
        self.start_y = 300

        # Difficulté du spawn des meteorites
        self.spawn_difficulty = 1.0      # commence doucement
        self.spawn_timer = 0             # compteur interne

        self.explosion_time = None
        self.score = 0
        self.frame_count = 0
        self.font_score = pygame.font.SysFont(None, 50)

        self.reset_level()
        # On initialise le niveau (joueur, etc.)
        
    def update_background(self):
        self.fond_x1 -= self.fond_speed
        self.fond_x2 -= self.fond_speed

        # boucle infinie
        if self.fond_x1 <= -self.width:
            self.fond_x1 = self.fond_x2 + self.width
        if self.fond_x2 <= -self.width:
            self.fond_x2 = self.fond_x1 + self.width

    def reset_level(self):
        # Réinitialise la position du joueur 
        self.player = Player(self.start_x, self.start_y, "soucoupe.png")
        # Crée un joueur au début 
        self.enemies = []
        self.explosion_time = None
        self.score = 0
        self.frame_count = 0
        self.spawn_difficulty = 1.0
        self.spawn_timer = 0

    def prepare_menu_player(self):
        self.player.rect.center = (self.width // 2, self.height // 2)
        self.player.vy = 0
        self.player.exploding = False
        self.player.explosion_index = 0
        self.player.image = self.player.original_image.copy()
       
    def run(self):
        while self.running:
            # Tant que running est True, la boucle continue
            for event in pygame.event.get():
            # On parcourt tous les événements envoyés par Pygame
                if event.type == pygame.QUIT:
                    # Si l'utilisateur ferme la fenêtre
                    self.running = False
                    # On arrête la boucle en mettant running à False
                if self.state == "menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Si on est dans le menu et qu'on appuie sur ENTREE
                    self.prepare_menu_player()
                    self.state = "transition"
                    # On passe en mode transition pour faire bouger la soucoupe 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.jump()
            if self.state == "menu":
                # Si on est dans l'écran de menu
                self.draw_menu()
                # On dessine le menu
            elif self.state == "transition":
                self.window.blit(self.fond, (0, 0))
                self.player.draw(self.window)
                self.update_transition()

            elif self.state == "play":
                # Si on est dans l'état de jeu
                self.update_game()
                # On met à jour la logique du jeu
                self.draw_game()
                # On dessine le jeu
            pygame.display.flip()
            # On met à jour l'affichage (affiche ce qui a été dessiné)
            self.clock.tick(60)
            # On limite la boucle à 60 images par seconde
        pygame.quit()
        # Quand la boucle est terminée, on ferme Pygame proprement

    def draw_menu(self):
        # Dessine l'écran de menu
        self.window.blit(self.fond, (0,0))
        # Affichage du titre 
        title_x = self.width // 2 - self.title_img.get_width() // 2
        title_y = 80
        self.window.blit(self.title_img, (title_x, title_y))

        # Utilise des valeurs par défaut si Player n'a pas encore float_angle, float_speed, float_amplitude
        angle = getattr(self.player, "float_angle", 0.0)
        speed = getattr(self.player, "float_speed", 0.05)
        amp = getattr(self.player, "float_amplitude", 8)
        angle += speed
        setattr(self.player, "float_angle", angle)  # stocke pour la frame suivante
        offset = int(math.sin(angle) * amp)
        self.player.rect.center = (self.width // 2, self.height // 2 + offset)
        self.player.draw(self.window)
        # --- PRESS START CLIGNOTANT (TAILLE ORIGINALE RESTAURÉE) ---
        self.start_alpha += self.alpha_direction
        if self.start_alpha <= 0 or self.start_alpha >= 255:
            self.alpha_direction *= -1

        start_img = self.start_img.copy()
        start_img.set_alpha(self.start_alpha)

        # centrer horizontalement le press start en gardant la taille originale de l'image
        x = self.width // 2 - start_img.get_width() // 2
        y = 500
        self.window.blit(start_img, (x, y))

    def draw_game(self):
        self.player.draw_hitbox(self.window)
        # Dessine la scène de jeu
        self.window.fill((0, 0, 20))
        # On remplit l'écran de bleu foncé      
        # Dessiner les deux fonds qui défilent
        self.window.blit(self.fond, (self.fond_x1, 0))
        self.window.blit(self.fond, (self.fond_x2, 0))
        self.player.draw(self.window)
        # On dessine le joueur
        for enemy in self.enemies:
            enemy.draw_hitbox(self.window)
            enemy.draw(self.window)
        score_text = self.font_score.render(f"Score : {self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (10, 10))
    
    def update_transition(self):    #pour faire bouger la soucoupe à la position de départ
        speed = 5
        dx = self.start_x - self.player.rect.x
        dy = self.start_y - self.player.rect.y

        if abs(dx) > 2:
            self.player.rect.x += dx / speed
        if abs(dy) > 2:
            self.player.rect.y += dy / speed

        if abs(dx) <= 2 and abs(dy) <= 2:
            self.player.rect.x = self.start_x
            self.player.rect.y = self.start_y
            self.state = "play"


    def update_game(self):
        self.update_background()  # ← AJOUT OBLIGATOIRE
        # Met à jour la logique du jeu
        keys = pygame.key.get_pressed()
        # On relit le clavier pour le saut
        if keys[pygame.K_SPACE]:
            # Si la barre d'espace est enfoncée
            self.player.jump()
            # On demande au joueur de sauter
        self.player.apply_gravity(self.ground_y)
        # On applique la gravité et on gère le sol
        self.player.update_explosion()   # <<< IMPORTANT : explosion se met à jour ICI
        # Lancer le timer de fin si explosion démarre
        if self.player.exploding and self.explosion_time is None:
            self.explosion_time = pygame.time.get_ticks()

        # Apparition aléatoire d'ennemis
        # Augmentation progressive de la difficulté (≈ toutes les 1 seconde)
        # Apparition aléatoire d'ennemis
        self.spawn_timer += 1
        if self.spawn_timer >= 60:  # toutes les secondes
            self.spawn_timer = 0
            self.spawn_difficulty += 0.1   # spawn de plus en plus vite 
            if self.spawn_difficulty > 30:
                self.spawn_difficulty = 30

        spawn_rate = max(20, int(300 / self.spawn_difficulty))

        # Choisir un emplacement vertical sûr
        gap = 80  # espace minimum pour la soucoupe
        def can_spawn(y_new, enemies, gap=80):
            for e in enemies:
                if abs(e.rect.y - y_new) < gap:
                    return False
            return True
        
        y_enemy = randint(0, self.height - 50)
        if randint(1, spawn_rate) == 1 and can_spawn(y_enemy, self.enemies):
            enemy = Enemy(self.width + 50, y_enemy, "meteorite.png")
            self.enemies.append(enemy)

        # Mise à jour des ennemis et collisions
        for enemy in self.enemies[:]:
            enemy.move(self.spawn_difficulty)
            if enemy.rect.right < 0:
                self.enemies.remove(enemy)
        # Si explosion en cours → attendre 1 seconde avant fin
        if self.explosion_time is not None:
            if pygame.time.get_ticks() - self.explosion_time >= 500:
                self.state = "menu"
                self.reset_level()
                self.prepare_menu_player()
                self.enemies.clear()
                return

        # Mise à jour des météorites
        for enemy in self.enemies[:]:
            enemy.move(self.spawn_difficulty)
            # Si elle sort de l'écran à gauche → suppression
            if enemy.rect.right < 0:
                self.enemies.remove(enemy)
            if self.player.hitbox.colliderect(enemy.hitbox):
                self.player.exploding = True
                if self.explosion_time is None:
                    self.explosion_time = pygame.time.get_ticks()
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            self.score += 1