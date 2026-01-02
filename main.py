import pygame
from Game import Game

if __name__ == '__main__':
    # Point d'entrée du programme, ce code s'exécute si on lance main.py
    pygame.init() #on initialise pygame
    game = Game() #on instancie un objet Game
    game.run() #on lance la boucle principale du jeu