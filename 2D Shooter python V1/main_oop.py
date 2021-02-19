import sys, pygame, time, random, math
from math import sqrt
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

white = 255,255,255
red = 255,0,0

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 600

screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)

font = pygame.font.Font("freesansbold.ttf",13)

running = True
#
bullets = []
bulletMagazine = 10
#	TIME
time = 0
reloadTime = 0

class character:
	# character image
	characterImg = pygame.image.load("thief1.png")
	characterImgScale = pygame.transform.scale(characterImg,(100,100))
	characterImgCopy = characterImgScale.copy()
	#	ANIMATION SPRITE
	walkRightLoad = [pygame.image.load("thief1_running.png"),pygame.image.load("thief1_running2.png"),pygame.image.load("thief1_running3.png"),pygame.image.load("thief1_running4.png"),pygame.image.load("thief1_running5.png"),]
	walkRight = [pygame.transform.scale(walkRightLoad[0],(100,100)),pygame.transform.scale(walkRightLoad[1],(100,100)),pygame.transform.scale(walkRightLoad[2],(100,100)),pygame.transform.scale(walkRightLoad[3],(100,100)),pygame.transform.scale(walkRightLoad[4],(100,100))]
	walkLeft = [pygame.transform.flip(walkRight[0],True,False),pygame.transform.flip(walkRight[1],True,False),pygame.transform.flip(walkRight[2],True,False),pygame.transform.flip(walkRight[3],True,False),pygame.transform.flip(walkRight[4],True,False)]
	def __init__(self,x,y,leftWalk,rightWalk,walkCount,xmove,ymove):
		self.x = x
		self.y = y
		self.leftWalk = leftWalk
		self.rightWalk = rightWalk
		self.walkCount = walkCount
		self.xmove = xmove
		self.ymove = ymove
	def draw(self,mx,my):
		self.mx = mx
		self.my = my

		if self.walkCount + 1 >= 60:
			self.walkCount = 0

		#	LEFTWALK ANIMATION
		frames = 12
		if self.leftWalk:
			if self.mx > self.x + 50:
				screen.blit(self.walkRight[self.walkCount//frames], (self.x,self.y))
				self.walkCount += 1

			else:
				screen.blit(self.walkLeft[self.walkCount//frames], (self.x,self.y))
				self.walkCount += 1
		#	RIGHTWALK ANIMATION
		if self.rightWalk:
			if self.mx < self.x + 50:
				screen.blit(self.walkLeft[self.walkCount//frames], (self.x,self.y))
				self.walkCount += 1
				
			else:
				screen.blit(self.walkRight[self.walkCount//frames], (self.x,self.y))
				self.walkCount += 1
		#	BLIT LEFT OR RIGHT FACING CHARACTER STANDING STILL
		if not self.leftWalk and not self.rightWalk:

			if self.mx > self.x + 50:
				screen.blit(self.characterImgCopy, (self.x,self.y))
			else:
				screen.blit(pygame.transform.flip(self.characterImgCopy,True,False),(self.x,self.y))

	def move(self):

		global running,bulletMagazine

		LEFT = 1
		RIGHT = 3
		velocity = 10
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.RESIZABLE:
				screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN:
				#	MOVE LEFT
				if event.key == pygame.K_a:
					self.xmove = 0 - velocity
					self.x -= self.xmove
					self.leftWalk = True
					self.rightWalk = False
				# MOVE RIGHT
				if event.key == pygame.K_d:
					self.xmove = + velocity
					self.x -= self.xmove
					self.leftWalk = False
					self.rightWalk = True
				if event.key == pygame.K_ESCAPE:
					menu()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					self.xmove = 0
					self.leftWalk = False
					self.rightWalk = False
			if event.type == pygame.KEYDOWN:
				# MOVE UP
				if event.key == pygame.K_w:
					self.ymove = - velocity
					self.y -= self.ymove
					if self.mx > self.x:
						self.rightWalk = True
						self.leftWalk = False
					else:
						self.rightWalk = False
						self.leftWalk = True
				# MOVE DOWN
				if event.key == pygame.K_s:
					self.ymove = + velocity
					self.y -= self.ymove
					if self.mx > self.x:
						self.rightWalk = True
						self.leftWalk = False
					else:
						self.rightWalk = False
						self.leftWalk = True
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w or event.key == pygame.K_s:
					self.ymove = 0
					self.leftWalk = False
					self.rightWalk = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == LEFT:
					if bulletMagazine > 0:
						position = pygame.mouse.get_pos()
						bullets.append([math.atan2(position[1]-(self.y + 60),position[0]-(self.x + 60)),(self.x + 60),(self.y + 60)])
						bulletMagazine -= 1
			if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
				pass
		self.x += self.xmove
		self.y += self.ymove

	def __repr__(self):
		pass
	def __str__(self):
		pass
class weapon(character):
	# image of paintball gun
	gunImg = pygame.image.load("paintball.png")
	gunImgScale = pygame.transform.scale(gunImg, (100,50))
	gunImgCopy = gunImgScale.copy()
	# paintball bullet image
	paintBallBullet = pygame.image.load("circle.png")
	paintBallBulletScale = pygame.transform.scale(paintBallBullet,(12,12))
	paintBallBulletCopy = paintBallBulletScale.copy()

	paintBallGunCopy_rect = gunImgCopy.get_rect()

	def __init__(self, class_character):
		self.x = class_character.x
		self.y = class_character.y

	def draw_paintball_gun(self,mx,my):
		self.mx = mx
		self.my = my

		angle = math.atan2(self.my - (self.y + 60), self.mx - (self.x + 60))

		left = -1.6741997891848224 
		leftFlip = pygame.transform.flip(self.gunImgCopy,False,True)

		#	GUN ROTATE IMG
		if self.mx <= self.x + 60:
			paintBallGunRotLeft = pygame.transform.rotate(leftFlip,360-angle*57.29)
			paintBallGunPosLeft = ((self.x + 60) - paintBallGunRotLeft.get_rect().width/2,(self.y + 60) - paintBallGunRotLeft.get_rect().height/2)
			screen.blit(paintBallGunRotLeft,paintBallGunPosLeft)
		else:
			paintBallGunRot = pygame.transform.rotate(self.gunImgCopy,360-angle*57.29)
			paintBallGunPos = ((self.x + 60) - paintBallGunRot.get_rect().width/2,(self.y + 60) - paintBallGunRot.get_rect().height/2)
			screen.blit(paintBallGunRot,paintBallGunPos)

	def bullet(self):
		global bulletMagazine,reloadTime

		if bulletMagazine in range(1,11):
			for bullet in bullets:
				bulletspeed = 25
				index=0
				velx = math.cos(bullet[0])*bulletspeed
				vely = math.sin(bullet[0])*bulletspeed
				bullet[1] += velx
				bullet[2] += vely 
				if bullet[1]<-64 or bullet[1]>2000 or bullet[2]<-64 or bullet[2]>2000:
					bullets.pop(index)
				index += 1
				for projectile in bullets:
					bullets1 = pygame.transform.rotate(self.paintBallBulletCopy, 360-projectile[0]*57.29)
					screen.blit(bullets1, (projectile[1],projectile[2]))
		else:

			reloadTime += 1
			if reloadTime == 150:	# 5 seconds * 60frames per second
				reloadTime = 0
				bulletMagazine = 10

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

		# FIRE BULLET MECHANIC

def draw_text(text, font, color, surface,x,y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textobj, textrect)

def menu():
	while True:

		mx,my = pygame.mouse.get_pos()
		clock.tick(FPS)

		screen.fill(white)

		LEFTCLICK = 1
		click = False
		button_1 = pygame.Rect((1920-600)/2,(1080-300)/2,200,50)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == LEFTCLICK:
					click = True

		if button_1.collidepoint((mx, my)):
			if click:
				main()
		pygame.draw.rect(screen, (255,0,0), button_1)
		draw_text('PLAY', font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 12.5)
		pygame.display.update()

def main():

	global white, screen, running,bulletMagazine, time

	x = 300
	y = 400
	leftWalk = False
	rightWalk = False
	walkCount = 0
	xmove = 0
	ymove = 0

	character1 = character(x,y,leftWalk,rightWalk,walkCount,xmove,ymove)
	while running:

		mx,my = pygame.mouse.get_pos()

		screen.fill(white)
		character1.move()
		character1.draw(mx,my)

		
		paintball1 = weapon(character1)
		paintball1.draw_paintball_gun(mx,my)
		paintball1.bullet()

		'''		TEST YOUR STUFF HERE		'''
		time += 1
		draw_text('TIME:' + str(time), font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 12.5)
		clock.tick(FPS)
		pygame.display.update()

if __name__ == "__main__":
	try:
		menu()
	except pygame.error:
		print("\n\n\n					video system not initialized")