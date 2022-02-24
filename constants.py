"""
This file contains the constant variable of the application and chess game,
its purpose is to maintain code clear and readable
"""
import pygame

author = "Baptiste Fraboul"

name = "Chess"

FPS = 60

# Constant UI-related

board_offset = (64, 128)

board_position= (576, 640 )

#Pygame related stuff

Arial_font = pygame.font.Font('fonts/ARIALN.TTF',16)

default_color = pygame.Color((61,61,61))

error_color = pygame.Color((136,0,21))