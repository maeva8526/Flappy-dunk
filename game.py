import pygame
# On importe la bibliothèque pygame pour gérer la fenêtre et le jeu

from ball import Player

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
        pygame.display.set_caption("Flappy dunk")
        # Définition du titre de la fenêtre
        self.clock = pygame.time.Clock()
        # Objet Clock pour limiter le nombre d'images par seconde
        self.running = True
        # Booléen qui indique si la boucle principale doit continuer
        self.state = "menu"
        # Etat du jeu : "menu" pour l'instant, plus tard "play"
        self.ground_y = 750
        # Position verticale du sol
        self.font_title = pygame.font.SysFont(None, 80)
        # Police pour le titre dans le menu
        self.font_text = pygame.font.SysFont(None, 40)
        # Police pour les textes dans le menu
        self.reset_level()
        # On initialise le niveau (joueur, etc.)

    def reset_level(self):
        # Réinitialise la position du joueur (plus tard ennemi, goal...)
        self.player = Player(100, 300, "soucoupe.png")
        # Crée un joueur au début du niveau, posé sur le sol
       
    def run(self):
        while self.running:
            # Tant que running est True, la boucle continue
            for event in pygame.event.get():
            # On parcourt tous les événements envoyés par Pygame
                if event.type == pygame.QUIT:
                    # Si l'utilisateur ferme la fenêtre
                    self.running = False
                    # On arrête la boucle en mettant running à False
                if self.state == "menu":
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
        title = self.font_title.render("Flappy Dunk", True, (255, 255, 255))
        # Crée le texte du titre en blanc
        text = self.font_text.render("Appuyez sur ENTREE", True, (255, 255, 255))
        # Crée le texte d'instruction
        self.window.blit(title,( 50, 100))
        # Dessine le titre
        self.window.blit(text, (60, 400)) #(x,y) du coin supérieur gauche du texte 
        # Dessine le texte d'instruction
    def draw_game(self):
        # Dessine la scène de jeu
        self.window.fill((0, 0, 20))
        # On remplit l'écran de bleu foncé
        self.player.draw(self.window)
        # On dessine le joueur
    def update_game(self):
        # Met à jour la logique du jeu
        keys = pygame.key.get_pressed()
        # On relit le clavier pour le saut
        if keys[pygame.K_SPACE]:
            # Si la barre d'espace est enfoncée
            self.player.jump()
            # On demande au joueur de sauter
        self.player.apply_gravity(self.ground_y)
        # On applique la gravité et on gère le sol
     


