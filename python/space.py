import pygame  # necessaire pour charger les images et les sons
import random


class Joueur():  # classe pour créer le vaisseau du joueur
    def __init__(self):
        self.image = pygame.image.load("img/vaisseau.png")
        self.sens = 0
        self.position = 400 - self.image.get_width()/2
        self.vitesse = 0.2

    def deplacer(self):
        if not (self.position <= 0 or self.position >= 800 - self.image.get_width()):
            match self.sens:
                case "droite":
                    self.position += self.vitesse
                case "gauche":
                    self.position -= self.vitesse
                case _:
                    pass

        else:
            if self.position <= 0 and self.sens == "droite":
                self.position += self.vitesse
            elif self.position >= 800 - self.image.get_width() and self.sens == "gauche":
                self.position -= self.vitesse

    def tirer(self):
        pass


class Balle():
    def __init__(self, tireur: Joueur):
        self.tireur = tireur
        self.depart = self.tireur.position
        self.hauteur = 500
        self.image = pygame.image.load("img/balle.png")
        self.etat = "chargee"

    def bouger(self):
        if self.etat == "tiree":
            self.hauteur -= 0.3
            if self.hauteur < -self.image.get_height():
                self.etat = "chargee"
                self.hauteur = 500
        else:
            self.depart = self.tireur.position


class Ennemi():

    NbEnnemis = random.randint(10, 20)

    def __init__(self):
        self.depart = random.randint(0, 800)
        self.hauteur = 0
        self.type = random.randint(1, 2)
        self.image = pygame.image.load("img/invader1")
        if self.type == 1:
            self.vitesse = 0.1
        else:
            self.vitesse = 0.3

    def avancer(self):
        self.hauteur -= self.vitesse
