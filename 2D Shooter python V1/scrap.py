import pygame,sys,time
WHITE = 255,255,255
fontList = pygame.font.get_fonts()
WIN_SIZE = 800,600
screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)
i = 0
pygame.init()
font = pygame.font.SysFont("freesansbold.ttf",13)
clock = pygame.time.Clock()
BLACK = 0,0,0
reloadTime = 0
def draw_text(text, font, color, surface,x,y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textobj, textrect)
drawText = False
while True:
	screen.fill(BLACK)
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and drawText == False:
				drawText=True
				print(fontList[i] + "			"	+ str(reloadTime))
				i += 1
	if drawText == True:
		draw_text("Hello World !    1 2 3 4 5 6 7 8 9 0    !@#$%^&*()-_;:><?|[}{]",pygame.font.SysFont(str(i)+".ttf",20),WHITE,screen,300,300)
		reloadTime += 1
		if reloadTime >= 150:
			reloadTime = 0
			drawText = False
	pygame.display.update()