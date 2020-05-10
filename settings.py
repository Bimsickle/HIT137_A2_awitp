# Settings file
# Created by Angie Hollingworth
# HIT137 2019

import pygame
pygame

window_width = 1200# Set window size
window_height = 750
FPS = 60# Set frames
speed = -1.2 # Set game speed

def textload (text, x, y, heightdiv,r,g,b,size, font, game):
    '''Function for blitting text to the screen\
    hegight is caluclated with a devisor'''
    pygame.font.init()
    font = pygame.font.SysFont(font, size) #select a font
    text = font.render(text,1 ,(r,g,b)) #Assemble Write the text
    text_rect = text.get_rect(center=(window_width/x, window_height/y+heightdiv))# calculate text size and position
    game.window.blit(text, text_rect) # Blit text to window
