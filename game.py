import pygame   # On importe la bibliothèque pygame pour gérer la fenêtre et le jeu

import math
import json
from Player import Player
from Enemy import Enemy
from random import randint

pygame.mixer.pre_init(44100, -16, 2, 512) # Configure le système de son de Pygame avant son initialisation pour éviter un décalage

class Game:  # Déclaration de la classe Game, qui va gérer l'ensemble du jeu
    def __init__(self): # Méthode constructeur, appelée quand on crée un objet Game
        with open("score.json", "r", encoding="utf-8") as f: # Ouvre le fichier score.json pour le meilleur score
            self.donnees = json.load(f)
        self.width = 430    # Largeur de la fenêtre en pixels
        self.height = 670   # Hauteur de la fenêtre en pixels
        
        # Création de la fenêtre Pygame avec la taille (largeur, hauteur)
        self.window = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption("Flappy Space")  # Titre de la fenêtre en haut à gauche

        # Image de fond
        self.fond = pygame.image.load("images/fond_etoile.png").convert_alpha()
        self.fond = pygame.transform.scale(self.fond, (430, 670))
        # Positions initiales des deux fonds
        self.fond_x1 = 0
        self.fond_x2 = self.width
        self.fond_speed = 2

        self.clock = pygame.time.Clock() # Objet Clock pour limiter le nombre d'images par seconde
        self.running = True # Booléen qui indique si la boucle principale doit continuer
        
        self.state = "menu"  # Etat du jeu : "menu" pour l'instant, plus tard "play"
       
        self.ground_y = 670  # Position verticale du sol (Taille de l'écran)
       
        self.title_img = pygame.image.load("images/title.png").convert_alpha() # Titre du jeux
        self.title_img = pygame.transform.scale(self.title_img, (450, 150))

        self.start_img = pygame.image.load("images/start.gif").convert_alpha() # Image press start
        self.start_img = pygame.transform.scale(self.start_img, (250, 90))

        # Alpha pour faire clignoter le press start 
        self.start_alpha = 255 # Règle l'opacité (ici au max)
        self.alpha_direction = -5 # Variable qui va diminuer l'opacité progressivement 

        # Joueur et ennemis
        self.player = None
        self.enemies = []

        self.start_x = 100  # Position du joueur au départ
        self.start_y = 300
        self.menu_player = Player(self.start_x, self.start_y, "images/soucoupe.png") # Création d'une soucoupe pour le menu 

        # Difficulté du spawn des meteorites
        self.spawn_difficulty = 1.0      # Commence doucement
        self.spawn_timer = 0             # Compteur interne

        self.explosion_time = None

        self.score = 0 # Score
        self.frame_count = 0 # Compte le nombre de frame pour mieux gérer le score
        self.font_score = pygame.font.SysFont(None, 50) # Taille du score

        # Meilleur score 
        self.best_score = self.donnees['score'] # Meilleur score stocké dans le json
        self.best_font = pygame.font.Font("arcade.ttf", 30) # Police et taille du meilleur score 

        self.reset_level() # On initialise le niveau (joueur, etc.)
        
        self.score_img = pygame.image.load("images/score.png").convert_alpha() # Image du score
        self.score_img = pygame.transform.scale(self.score_img, (110, 45))

        self.best_img = pygame.image.load("images/high_score.png").convert_alpha() # Image du meilleur score
        self.best_img = pygame.transform.scale(self.best_img, (160, 100))
        self.pixel_font = pygame.font.Font("arcade.ttf", 25) # Police du nombre score

        self.game_over = False
        self.game_over_img = pygame.image.load("images/game_over.png").convert_alpha() # Image du game over
        self.game_over_img = pygame.transform.scale(self.game_over_img, (450, 150))

        # Son game over
        self.sound_game_over = pygame.mixer.Sound("Sons/explosion.mp3")
        self.sound_game_over.set_volume(0.7)
        self.game_over_sound_played = False
        # Musique de fond 
        pygame.mixer.music.load("Sons/musique_de_fond.mp3")
        pygame.mixer.music.set_volume(0.4)
        self.menu_music_playing = False  # Sera lancé automatiquement
        
    def update_background(self):
        """Permet de faire défiler le fond à l'infini en faisant défilé 2 fonds l'un après l'autre"""
        self.fond_x1 -= self.fond_speed
        self.fond_x2 -= self.fond_speed
        # Boucle infinie
        if self.fond_x1 <= -self.width: # Si le fond arrive à la fin de l'écran à gauche alors changer de position 
            self.fond_x1 = self.fond_x2 + self.width
        if self.fond_x2 <= -self.width:
            self.fond_x2 = self.fond_x1 + self.width

    def reset_level(self):
        """Réinitialise le jeu"""
        self.player = Player(self.start_x, self.start_y, "images/soucoupe.png") # Crée un joueur au début 
        self.enemies = [] # Supprime tous les ennemis
        self.explosion_time = None
        self.score = 0
        self.frame_count = 0
        self.spawn_difficulty = 1.0
        self.spawn_timer = 0
        self.game_over_sound_played = False

    def prepare_menu_player(self): # Prépare le joueur pour l’affichage dans le menu ou le game over
        self.player.rect.center = (self.width // 2, self.height // 2) # Place le joueur au milieu 
        self.player.vy = 0
        self.player.exploding = False # Désactive l'état d'explosion
        self.player.explosion_index = 0
        self.player.image = self.player.original_image.copy() # Restaure l’image normale de la soucoupe (sans explosion)
       
    def run(self):
        # Lancer la musique de fond une seule fois au démarrage
        if not self.menu_music_playing:
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
            self.menu_music_playing = True

        while self.running: # Tant que running est True, la boucle continue
            for event in pygame.event.get(): # On parcourt tous les événements envoyés par Pygame

                if event.type == pygame.QUIT: # Si l'utilisateur ferme la fenêtre
                    self.donnees['score'] = self.best_score # On enregistre le meilleur score dans le json  
                    with open("score.json", "w", encoding="utf-8") as f:
                        json.dump(self.donnees, f, indent=2, ensure_ascii=False)
                    self.running = False # On arrête la boucle en mettant running à False

                if self.state == "menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Si on est dans le menu et qu'on appuie sur ENTREE
                    self.prepare_menu_player()
                    self.state = "transition" # On passe en mode transition pour faire bouger la soucoupe 
                    
                if self.state == "end" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Si on est dans le end et qu'on appuie sur ENTREE
                    self.reset_level()
                    self.prepare_menu_player()
                    self.state = "transition" # On passe en mode transition pour faire bouger la soucoupe 

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Si on appuie sur espace 
                    self.player.jump() # La soucoupe saute 

            if self.state == "menu": # Si on est dans l'écran de menu
                self.draw_menu() # On dessine le menu

            elif self.state == "transition": # Si on est dans l'état de transition
                self.window.blit(self.fond, (0, 0))
                self.player.draw(self.window)
                self.update_transition() # On applique l'animation de transition de la soucoupe 

            elif self.state == "play": # Si on est dans l'état de jeu
                self.update_game() # On met à jour la logique du jeu
                self.draw_game() # On dessine le jeu
    
            elif self.state == 'end': # Si on est dans l'état de fin
                self.game_over = True
                self.draw_menu() # On dessine le menu

            pygame.display.flip() # On met à jour l'affichage (affiche ce qui a été dessiné)
            self.clock.tick(60) # On limite la boucle à 60 images par seconde
        pygame.quit() # Quand la boucle est terminée, on ferme Pygame 

    def draw_menu(self):
        """Dessine l'écran de menu"""
        self.window.blit(self.fond, (0,0))
        if self.game_over:
            # Titre game over
            game_over_x = self.width // 2 - self.game_over_img.get_width() // 2
            self.window.blit(self.game_over_img, (game_over_x, 40))
        else:
            # Titre du jeu  
            title_x = self.width // 2 - self.title_img.get_width() // 2
            self.window.blit(self.title_img, (title_x, 40))

        self.window.blit(self.score_img, (120, 400)) # Image du score affichée
        score_text = self.pixel_font.render(str(self.score), True, (255, 255, 255))
        # Position du nombre juste à droite de l'image
        number_x = 120 + self.score_img.get_width() + 10
        number_y = 410  # Position verticale pour le score
        self.window.blit(score_text, (number_x, number_y))

        # Image du meilleur score 
        decalage_gauche = 50  # Ajuste la position horizontale
        best_x = (self.width // 2 - self.best_img.get_width() // 2) - decalage_gauche
        best_y = 200
        self.window.blit(self.best_img, (best_x, best_y))
        # Valeur du meilleur score
        best_value = self.best_font.render(str(self.best_score), True, (255, 255, 255))
        value_x = best_x + self.best_img.get_width() + 10
        value_y = best_y + self.best_img.get_height() // 2 - best_value.get_height() // 2
        self.window.blit(best_value, (value_x, value_y))

        # Utilise des valeurs par défaut si Player n'a pas encore float_angle, float_speed, float_amplitude
        angle = getattr(self.menu_player, "float_angle", 0.0) # Angle utilisé pour calculer le mouvement sinusoïdal
        speed = getattr(self.menu_player, "float_speed", 0.05) # Vitesse du flottement
        amp = getattr(self.menu_player, "float_amplitude", 8) # Amplitude du flottement
        angle += speed
        setattr(self.menu_player, "float_angle", angle)  # Stocke pour la frame suivante
        offset = int(math.sin(angle) * amp) # Calcule le décalage vertical à l’aide d’une fonction sinusoïdale
        self.menu_player.rect.center = (self.width // 2, self.height // 2 + offset) # Centre le joueur à l’écran avec un léger mouvement vertical
        self.menu_player.draw(self.window) # Dessine la soucoupe à sa nouvelle position

        # Press start clignotant
        self.start_alpha += self.alpha_direction # On réduit/augmente l'opacité
        if self.start_alpha <= 0 or self.start_alpha >= 255:
            self.alpha_direction *= -1 # On change le signe de la variable pour que l'opacité augmente/diminue

        start_img = self.start_img.copy() # On copie l'image du press start pour éviter de modifier l'originale
        start_img.set_alpha(self.start_alpha) # On applique l'opacité à la copie 

        # Centrer horizontalement le press start en gardant la taille originale de l'image
        x = self.width // 2 - start_img.get_width() // 2
        y = 500
        self.window.blit(start_img, (x, y))

    def draw_game(self):
        self.player.draw_hitbox(self.window) # On dessine d'abord la hitbox de la soucoupe pour pas la voir
        self.window.fill((0, 0, 0)) # Puis on dessine l'écran en noir     
        # Dessiner les deux fonds qui défilent
        self.window.blit(self.fond, (self.fond_x1, 0))
        self.window.blit(self.fond, (self.fond_x2, 0))
        self.player.draw(self.window) # On dessine le joueur
        for enemy in self.enemies: # On dessine les météorites
            enemy.draw_hitbox(self.window)
            enemy.draw(self.window)
        # Affichage image score
        score_x = 10
        score_y = 10
        self.window.blit(self.score_img, (score_x, score_y))
        # Texte score
        score_text = self.pixel_font.render(str(self.score), True, (255, 255, 255))
        # Position du nombre juste à droite de l'image
        number_x = score_x + self.score_img.get_width() + 10
        score_value_y = 20  # Nouvelle position verticale pour le score
        self.window.blit(score_text, (number_x, score_value_y))
  
        def update_transition(self):
            """Fait bouger la soucoupe à la position de départ"""
            speed = 5 # Vitesse de déplacement 
            dx = self.start_x - self.player.rect.x # Distance horizontale entre la position actuel et celle pour jouer
            dy = self.start_y - self.player.rect.y # Distance verticale entre la position actuel et celle pour jouer

            if abs(dx) > 2: # Si la valeur absolue de dx > 2
                self.player.rect.x += dx / speed # Alors on déplace la soucoupe progressivement
            if abs(dy) > 2: # Si la valeur absolue de dy > 2
                self.player.rect.y += dy / speed

            if abs(dx) <= 2 and abs(dy) <= 2: # Quand on est assez proche de la position cible 
                self.player.rect.x = self.start_x # Alors on met la soucoupe à sa position de jeu
                self.player.rect.y = self.start_y
                self.state = "play" # On change l'état du jeu 

    def update_game(self):
        self.update_background()  
        # Met à jour la logique du jeu
        keys = pygame.key.get_pressed() # On relit le clavier pour le saut
        if keys[pygame.K_SPACE]: # Si la barre d'espace est enfoncée
            self.player.jump() # On fait sauter la soucoupe
        self.player.apply_gravity(self.height) # On applique la gravité et on gère le sol
        self.player.update_explosion()   # Explosion se met à jour ici
        # Lancer le timer de fin si explosion démarre
        if self.player.exploding and self.explosion_time is None:
            self.explosion_time = pygame.time.get_ticks()
            if not self.game_over_sound_played:
                self.sound_game_over.play() # On lance la musique d'explosion
                self.game_over_sound_played = True

        # Augmentation progressive de la difficulté (≈ toutes les 1 secondes)
        self.spawn_timer += 1 # Compte le nombre de frame pour mesurer le temps
        if self.spawn_timer >= 60:  # Toutes les secondes car 60 frames/seconde
            self.spawn_timer = 0
            self.spawn_difficulty += 0.1   # Augmente progressivement la difficulté
            if self.spawn_difficulty > 30: # Limite de difficulté
                self.spawn_difficulty = 30

        spawn_rate = max(20, int(300 / self.spawn_difficulty))
        '''Calcule la probabilité d'apparition des ennemis : 
        plus la difficulté augmente, plus les ennemis apparaissent souvent,
        avec une limite minimale pour garder le jeu jouable'''

        # Choisir un emplacement vertical sûr
        def can_spawn(y_new, enemies):
            for e in enemies:
                if abs(e.rect.y - y_new) < 80: # Espace minimum entre 2 météorites pour la soucoupe
                    return False
            return True
        
        y_enemy = randint(0, self.height - 50) # Position verticale aléatoire d'une météorite
        if randint(1, spawn_rate) == 1 and can_spawn(y_enemy, self.enemies): # Détermine aléatoirement l'apparition d'une météorite
            enemy = Enemy(self.width + 50, y_enemy, "images/meteorite.png") # On crée une météorite
            self.enemies.append(enemy) # Et on l'ajoute à la liste des ennemis

        # Si explosion en cours attendre un petit peu avant la fin
        if self.explosion_time is not None:
            if pygame.time.get_ticks() - self.explosion_time >= 500: # Attend 500 millisecondes (0,5 seconde) après l’explosion
                self.meilleur_score() # On met à jour le meilleur score s'il faut
                self.state = "end" # On passe à l'état game over
                return

        # Mise à jour des météorites
        for enemy in self.enemies[:]:
            enemy.move(self.spawn_difficulty) # On bouge la météorite en fonction de la difficulté 
            if enemy.rect.right < 0: # Si elle sort de l'écran à gauche 
                self.enemies.remove(enemy) # Alors suppression de la météorite
            if self.player.hitbox.colliderect(enemy.hitbox): # Si il y a une collision avec une météorite
                self.player.exploding = True # Déclenche l'animation d'explosion
                if self.explosion_time is None:
                    self.explosion_time = pygame.time.get_ticks()
                if not self.game_over_sound_played:
                    self.sound_game_over.play()
                    self.game_over_sound_played = True

        self.frame_count += 1 # On augmente de 1 à chaque frame
        if self.frame_count % 60 == 0:  # Augmente le score de 1 toutes les secondes (60 images par seconde)
            self.score += 1

    def meilleur_score(self):
        """Compare le score et le meilleur score pour potentiellement le remplacer"""
        if self.best_score < self.score:
            self.best_score = self.score
            
