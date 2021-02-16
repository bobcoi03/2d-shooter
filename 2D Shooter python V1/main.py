import sys, pygame, time, random, math
from math import sqrt

pygame.init()

clock = pygame.time.Clock()

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

# ANIMATIONS SPRITE

walkRightLoad = [pygame.image.load("thief1_running.png"),pygame.image.load("thief1_running2.png"),pygame.image.load("thief1_running3.png"),pygame.image.load("thief1_running4.png"),pygame.image.load("thief1_running5.png"),]
walkRight = [pygame.transform.scale(walkRightLoad[0],(100,100)),pygame.transform.scale(walkRightLoad[1],(100,100)),pygame.transform.scale(walkRightLoad[2],(100,100)),pygame.transform.scale(walkRightLoad[3],(100,100)),pygame.transform.scale(walkRightLoad[4],(100,100))]
walkLeft = [pygame.transform.flip(walkRight[0],True,False),pygame.transform.flip(walkRight[1],True,False),pygame.transform.flip(walkRight[2],True,False),pygame.transform.flip(walkRight[3],True,False),pygame.transform.flip(walkRight[4],True,False)]
walkRightBackwards = walkRight = [pygame.transform.scale(walkRightLoad[4],(100,100)),pygame.transform.scale(walkRightLoad[3],(100,100)),pygame.transform.scale(walkRightLoad[2],(100,100)),pygame.transform.scale(walkRightLoad[1],(100,100)),pygame.transform.scale(walkRightLoad[0],(100,100))]
leftWalk = False
rightWalk = False
walkCount = 0
#x,y of character
x = 400
xmove = 0
y = 300
ymove = 0
running = True
velocity = 10
#
fire = 0
bulletX = x + 60
bulletY = y + 60
bulletXMove = 1
bulletYMove = 0

bullets = []

class character:
	
	def __init__(self,mx,my):
		self.mx = mx
		self.my = my

	def draw(self):

		global walkCount

		if walkCount + 1 >= 60:
			walkCount = 0

		if leftWalk:
			if self.mx > x + 50:
				screen.blit(walkRight[walkCount//12], (x,y))
				walkCount += 1
			else:
				screen.blit(walkLeft[walkCount//12], (x,y))
				walkCount += 1
		if rightWalk:
			if self.mx < x + 50:
				screen.blit(walkLeft[walkCount//12], (x,y))
				walkCount += 1
			else:
				screen.blit(walkRight[walkCount//12], (x,y))
				walkCount += 1

		if not leftWalk and not rightWalk:

			if self.mx > x + 50:
				screen.blit(characterImgCopy, (x,y))
			else:
				screen.blit(pygame.transform.flip(characterImgCopy,True,False),(x,y))


	def move(self):

		global x,y,xmove,ymove,running, leftWalk,rightWalk

		LEFT = 1
		RIGHT = 3
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.RESIZABLE:
				screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN:
				#	MOVE LEFT
				if event.key == pygame.K_a:
					xmove = 0 - velocity
					x -= xmove
					leftWalk = True
					rightWalk = False
				# MOVE RIGHT
				if event.key == pygame.K_d:
					xmove = + velocity
					x -= xmove
					leftWalk = False
					rightWalk = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					xmove = 0
					leftWalk = False
					rightWalk = False
			if event.type == pygame.KEYDOWN:
				# MOVE UP
				if event.key == pygame.K_w:
					ymove = - velocity
					y -= ymove
					if self.mx > x:
						rightWalk = True
						leftWalk = False
					else:
						rightWalk = False
						leftWalk = True
				# MOVE DOWN
				if event.key == pygame.K_s:
					ymove = + velocity
					y -= ymove
					if self.mx > x:
						rightWalk = True
						leftWalk = False
					else:
						rightWalk = False
						leftWalk = True
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w or event.key == pygame.K_s:
					ymove = 0
					leftWalk = False
					rightWalk = False
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
			bulletspeed = 20
			index=0
			velx = math.cos(bullet[0])*bulletspeed
			vely = math.sin(bullet[0])*bulletspeed
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
		clock.tick(60)

		mx,my = pygame.mouse.get_pos()

		screen.fill(white)

		character1 = character(mx,my)
		character1.draw()
		character1.move()
		
		#paintball = weapon(mx,my)
		#paintball.draw_paintball_gun()

		x += xmove
		y += ymove

		'''		TEST YOUR STUFF HERE		'''
		
		pygame.display.update()

if __name__ == "__main__":
	main()