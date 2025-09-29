import pygame

SHADOW = (0, 0, 0, 90)

def draw_image_button(screen, idle_img, hover_img, rect, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    screen.blit(hover_img if hovered else idle_img, rect)
    return hovered
