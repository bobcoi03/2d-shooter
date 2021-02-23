import pygame,sys
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 600
screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)

def draw_text(text, font, color, surface,x,y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textobj, textrect)

def draw_rectangle(leftX,leftY,width,height,color,fill,thickness):
	rectangle = pygame.Rect(leftX,leftY,width,height)

	if fill == True:
		draw_rect = pygame.draw.rect(screen, color, rectangle)
	if fill == False:
		draw_rect = pygame.draw.rect(screen, color, rectangle,width=thickness)

def camera_scroll(x,y):
	pass
