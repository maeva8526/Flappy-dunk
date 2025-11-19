import pygame

background_layers = [
    pygame.image.load("fond-_ecran.png").convert(),
    pygame.image.load().convert()
]

class Game:
    def __init__(self):
        self.width = 430 #largeur de la fenêtre
        self.height = 670 #hauteur de la fenêtre
        self.window = pygame.display.set_mode((self.width, self.height))
        #crée la fenêtre 
        pygame.display.set_caption("Flappy dunk de Maéva et Raphaël")
        self.clock = pygame.time.Clock() #limite le nombre d'images/secondes
        self.running = True #indique si la boucle principale doit continuer
        self.state = "menu"
        # Etat du jeu : "menu" pour l'instant, plus tard "play"

    def run(self):
        # Méthode principale qui contient la boucle de jeu
        while self.running:
            for event in pygame.event.get(): #on parcours tous les événements envoyés par pygame
                if event.type == pygame.QUIT: #si l'utilisateur ferme la fenêtre
                    self.running = False #arrête la boucle 
            self.window.fill((0, 0, 0)) # couleur des images de la fenêtre
            pygame.display.flip() #met à jour l'affichage
            self.clock.tick(60) #limite la boucle à 60 img/sec
        pygame.quit() #ferme pygame quand la boucle est terminée

