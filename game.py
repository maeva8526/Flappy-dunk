import pygame
# On importe la bibliothèque pygame pour gérer la fenêtre et le jeu

from ball import Player
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
        self.font_title = pygame.font.SysFont(None, 80)
        # Police pour le titre dans le menu
        self.font_text = pygame.font.SysFont(None, 40)
        # Police pour les textes dans le menu
        self.reset_level()
        # On initialise le niveau (joueur, etc.)
        self.enemies = []
        self.explosion_time = None

    def update_background(self):
        self.fond_x1 -= self.fond_speed
        self.fond_x2 -= self.fond_speed

        # boucle infinie
        if self.fond_x1 <= -self.width:
            self.fond_x1 = self.fond_x2 + self.width
        if self.fond_x2 <= -self.width:
            self.fond_x2 = self.fond_x1 + self.width

    def reset_level(self):
        # Réinitialise la position du joueur (plus tard ennemi, goal...)
        self.player = Player(100, 300, "soucoupe.png")
        # Crée un joueur au début du niveau, posé sur le sol
        self.enemies = []
        self.explosion_time = None
       
    def run(self):
        while self.running:
            # Tant que running est True, la boucle continue
            for event in pygame.event.get():
            # On parcourt tous les événements envoyés par Pygame
                if event.type == pygame.QUIT:
                    # Si l'utilisateur ferme la fenêtre
                    self.running = False
                    # On arrête la boucle en mettant running à False
                if self.state == "menu" or self.state == "end":
                    # Si on est dans le menu
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        # Si on appuie sur ENTREE
                        self.reset_level()
                        # On réinitialise le niveau
                        self.state = "play"
                        # On passe en mode jeu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.jump()
            if self.state == "menu":
                # Si on est dans l'écran de menu
                self.draw_menu()
                # On dessine le menu
            elif self.state == "play":
                # Si on est dans l'état de jeu
                self.update_game()
                # On met à jour la logique du jeu
                self.draw_game()
                # On dessine le jeu
            elif self.state == 'end':
                self.draw_end()
                self.reset_level()
            pygame.display.flip()
            # On met à jour l'affichage (affiche ce qui a été dessiné)
            self.clock.tick(60)
            # On limite la boucle à 60 images par seconde
        pygame.quit()
        # Quand la boucle est terminée, on ferme Pygame proprement

    def draw_menu(self):
        # Dessine l'écran de menu
        self.window.fill((0, 0, 0))
        # Remplit l'écran de noir
        title = self.font_title.render("Flappy Space", True, (255, 255, 255))
        # Crée le texte du titre en blanc
        text = self.font_text.render("Appuyez sur ENTREE", True, (255, 255, 255))
        # Crée le texte d'instruction
        self.window.blit(title,(40, 100))
        # Dessine le titre
        self.window.blit(text, (60, 400)) #(x,y) du coin supérieur gauche du texte 
        # Dessine le texte d'instruction
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
    def draw_end(self):
        # Dessine l'écran de fin
        self.window.fill((0, 0, 0))
        # Remplit l'écran de noir
        title = self.font_title.render("Game Over", True, (255, 255, 255))
        # Crée le texte du titre en blanc
        text = self.font_text.render("Appuyez sur ENTREE", True, (255, 255, 255))
        # Crée le texte d'instruction
        self.window.blit(title,(60, 100))
        # Dessine le titre
        self.window.blit(text, (60, 400)) #(x,y) du coin supérieur gauche du texte 
        # Dessine le texte d'instruction
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

        # Apparition d'une météorite (1 chance sur 120 = environ 0.5 seconde)
        if randint(1, 120) == 1:
            enemy = Enemy(self.width + 50, randint(0, 670), "meteorite.png")
            self.enemies.append(enemy)
        # Si explosion en cours → attendre 1 seconde avant fin
        if self.explosion_time is not None:
            if pygame.time.get_ticks() - self.explosion_time >= 500:
                self.state = "end"
                return

        # Mise à jour des météorites
        for enemy in self.enemies[:]:
            enemy.move()
            # Si elle sort de l'écran à gauche → suppression
            if enemy.rect.right < 0:
                self.enemies.remove(enemy)
            if self.player.hitbox.colliderect(enemy.hitbox):
                self.player.exploding = True
                if self.explosion_time is None:
                    self.explosion_time = pygame.time.get_ticks()