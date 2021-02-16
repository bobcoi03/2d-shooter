import sys, pygame, time, random, math
from math import sqrt

pygame.init()

white = 255,255,255
red = 255,0,0

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 600

screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)

font = pygame.font.Font("freesansbold.ttf",13)
# image of paintball gun
gunImg = pygame.image.load("paintball.png")
gunImgScale = pygame.transform.scale(gunImg, (100,50))
gunImgCopy = gunImgScale.copy()
# character image
characterImg = pygame.image.load("thief1.png")
characterImgScale = pygame.transform.scale(characterImg,(100,100))
characterImgCopy = characterImgScale.copy()
# paintball bullet image
paintBallBullet = pygame.image.load("circle.png")
paintBallBulletScale = pygame.transform.scale(paintBallBullet,(12,12))
paintBallBulletCopy = paintBallBulletScale.copy()
#x,y of character
x = 400
xmove = 0
y = 300
ymove = 0
running = True
#
fire = 0
bulletX = x + 60
bulletY = y + 60
bulletXMove = 1
bulletYMove = 0

bullets = []

class character:
	imageCopy = characterImgCopy
	
	def __init__(self,mx,my):
		self.mx = mx
		self.my = my

	def draw(self):

		if self.mx <= x + 50:
			leftFlip = pygame.transform.flip(self.imageCopy,True,False)
			screen.blit(leftFlip, (x,y))
		else:
			screen.blit(self.imageCopy, (x,y))

	def move(self):

		global x,y,xmove,ymove,running

		sensitivity = 2

		LEFT = 1
		RIGHT = 3
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.RESIZABLE:
				screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					xmove = 0 - sensitivity
					x -= xmove
				if event.key == pygame.K_d:
					xmove = + sensitivity
					x -= xmove
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					xmove = 0
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					ymove = - sensitivity
					y -= ymove
				if event.key == pygame.K_s:
					ymove = + sensitivity
					y -= ymove
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w or event.key == pygame.K_s:
					ymove = 0
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == LEFT:
					position = pygame.mouse.get_pos()
					bullets.append([math.atan2(position[1]-(y + 60),position[0]-(x + 60)),(x + 60),(y + 60)])
			if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
				pass

class weapon:
	paintBallGunCopy_rect = gunImgCopy.get_rect()
	characterImgRect = characterImgCopy.get_rect()

	global x,y

	def __init__(self,mx,my):
		self.mx = mx
		self.my = my

	def draw_paintball_gun(self):

		angle = math.atan2(self.my - (y + 60), self.mx - (x + 60))

		left = -1.6741997891848224 
		leftFlip = pygame.transform.flip(gunImgCopy,False,True)

		if self.mx <= x + 60:
			paintBallGunRotLeft = pygame.transform.rotate(leftFlip,360-angle*57.29)
			paintBallGunPosLeft = ((x + 60) - paintBallGunRotLeft.get_rect().width/2,(y + 60) - paintBallGunRotLeft.get_rect().height/2)
			screen.blit(paintBallGunRotLeft,paintBallGunPosLeft)
		else:
			paintBallGunRot = pygame.transform.rotate(gunImgCopy,360-angle*57.29)
			paintBallGunPos = ((x + 60) - paintBallGunRot.get_rect().width/2,(y + 60) - paintBallGunRot.get_rect().height/2)
			screen.blit(paintBallGunRot,paintBallGunPos)

			'''									GET X,Y COORDINATES OF ROTATED GUN IMAGE
			cos = math.cos
			sin = math.cos
			a = angle
			xm = x + 60
			ym = y + 60
			xpos = xm + 15
			ypos = ym - 15
			xr = (xpos - xm) * cos(a) - (ypos - ym) * sin(a) + xm
			yr = (xpos - xm) * sin(a) + (ypos - ym) * cos(a) + ym
			pygame.draw.line(screen, (red),(xr,yr),(self.mx,self.my))
			'''

		for bullet in bullets:
			index=0
			velx = math.cos(bullet[0])*2
			vely = math.sin(bullet[0])*2
			bullet[1] += velx
			bullet[2] += vely 
			if bullet[1]<-64 or bullet[1]>2000 or bullet[2]<-64 or bullet[2]>2000:
				bullets.pop(index)
			index += 1
			for projectile in bullets:
				bullets1 = pygame.transform.rotate(paintBallBulletCopy, 360-projectile[0]*57.29)
				screen.blit(bullets1, (projectile[1],projectile[2]))

def main():

	global x,y,xmove,ymove,white,screen,running
	
	while running:

		mx,my = pygame.mouse.get_pos()

		screen.fill(white)

		character1 = character(mx,my)
		character1.draw()

		character1.move()
		paintball = weapon(mx,my)
		paintball.draw_paintball_gun()

		x += xmove
		y += ymove
		
		pygame.display.update()

if __name__ == "__main__":
	main()