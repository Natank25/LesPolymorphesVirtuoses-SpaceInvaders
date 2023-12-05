import pygame.display

import main_game
import random
import sys
import os
import pygame

class Ennemi:

    NbEnnemis = random.randint(10, 20)

    def __init__(self, speed):
        self.depart = random.randint(0, pygame.display.get_window_size()[0])
        self.hauteur = 0
        self.spee


    def avancer(self):
        self.hauteur -= self.speed

class Invader1(Ennemi):
    def __init__(self):
        super(Invader1, self).__init__(5)

class Invader2(Ennemi):
    def __init__(self):
        pass