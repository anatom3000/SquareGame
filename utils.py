import pygame


def pilImageToSurface(pilImage):
    return pygame.image.frombytes(
        pilImage.tobytes(), pilImage.size, pilImage.mode
    ).convert_alpha()

