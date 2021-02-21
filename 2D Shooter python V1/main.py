import sys, pygame, time, random, math
from math import sqrt
from pygame.locals import *
import draw
pygame.init()

clock = pygame.time.Clock()
FPS = 60

WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,128,0
BLUE = 0,0,255

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 600

screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)
font = pygame.font.Font("freesansbold.ttf",13)
running = True
#
bullets = []
#	TIME
time = 0
class character:
	# character image
	characterImg = pygame.image.load("thief1.png")
	characterImgScale = pygame.transform.scale(characterImg,(100,100))
	characterImgCopy = characterImgScale.copy()
	#	ANIMATION SPRITE
	walkRightLoad = [pygame.image.load("thief1_running.png"),pygame.image.load("thief1_running2.png"),pygame.image.load("thief1_running3.png"),pygame.image.load("thief1_running4.png"),pygame.image.load("thief1_running5.png"),]
	walkRight = [pygame.transform.scale(walkRightLoad[0],(100,100)),pygame.transform.scale(walkRightLoad[1],(100,100)),pygame.transform.scale(walkRightLoad[2],(100,100)),pygame.transform.scale(walkRightLoad[3],(100,100)),pygame.transform.scale(walkRightLoad[4],(100,100))]
	walkLeft = [pygame.transform.flip(walkRight[0],True,False),pygame.transform.flip(walkRight[1],True,False),pygame.transform.flip(walkRight[2],True,False),pygame.transform.flip(walkRight[3],True,False),pygame.transform.flip(walkRight[4],True,False)]

	runReloadfunction = False

	def __init__(self,x,y,leftWalk,rightWalk,walkCount,XMOVE,YMOVE):
		self.x = x
		self.y = y
		self.leftWalk = leftWalk
		self.rightWalk = rightWalk
		self.walkCount = walkCount
		self.XMOVE = XMOVE
		self.YMOVE = YMOVE
		self.isJump = False
		self.jumpCount = 10
		self.bulletMagazine = 10
		self.reloadTime = 0
		self.runReloadfunction = False
	
	def draw(self,mx,my,scroll):
		self.scroll0 = scroll[0]
		self.scroll1 = scroll[1]
		self.mx = mx
		self.my = my

		if self.walkCount + 1 >= FPS:
			self.walkCount = 0
		#	LEFTWALK ANIMATION
		frames = 12
		if self.leftWalk:
			if self.mx > self.x + 50:
				screen.blit(self.walkRight[self.walkCount//frames], (self.x-self.scroll0,self.y-self.scroll1))
				self.walkCount += 1
			else:

				screen.blit(self.walkLeft[self.walkCount//frames], (self.x-self.scroll0,self.y-self.scroll1))
				self.walkCount += 1
		#	RIGHTWALK ANIMATION
		if self.rightWalk:
			if self.mx < self.x + 50:
				screen.blit(self.walkLeft[self.walkCount//frames], (self.x-self.scroll0,self.y-self.scroll1))
				self.walkCount += 1
				
			else:
				screen.blit(self.walkRight[self.walkCount//frames], (self.x-self.scroll0,self.y-self.scroll1))
				self.walkCount += 1
		#	BLIT LEFT OR RIGHT FACING CHARACTER STANDING STILL
		if not self.leftWalk and not self.rightWalk:

			if self.mx > self.x + 50:
				screen.blit(self.characterImgScale, (self.x-self.scroll0,self.y-self.scroll1))
			else:
				screen.blit(pygame.transform.flip(self.characterImgScale,True,False),(self.x-self.scroll0,self.y-self.scroll1))

	def jump(self):
		if self.isJump:
			if self.jumpCount >= -10:
				neg = 1
				if self.jumpCount < 0:
					neg = - 1
				self.y -= self.jumpCount**2 * 0.5 * neg
				self.jumpCount -= 1
			else:
				self.isJump = False
				self.jumpCount = 10

	def reload(self):
		if self.bulletMagazine == 0:
			self.reloadTime += 1
			if self.reloadTime >= 150:
				self.bulletMagazine = 10
				self.reloadTime = 0
				self.runReloadfunction = False
		draw.draw_text("Reloading....", font, RED,screen, ((1920-600)/2) + 85,((1080-300)/2) -100)


	def move(self):
		global running

		LEFT = 1
		RIGHT = 3
		velocity = 10
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				break
			if event.type == pygame.RESIZABLE:
				screen
			if event.type == pygame.KEYDOWN:
				#	MOVE LEFT
				if event.key == pygame.K_a:
					self.XMOVE = 0 - velocity 
					self.x -= self.XMOVE
					self.leftWalk = True
					self.rightWalk = False
				# MOVE RIGHT
				elif event.key == pygame.K_d:
					self.XMOVE = 0 + velocity
					self.x += self.XMOVE
					self.leftWalk = False
					self.rightWalk = True
				elif event.key == pygame.K_ESCAPE:
					menu()
				elif event.key == pygame.K_SPACE:
					self.isJump = True
					self.jump()
				elif event.key == pygame.K_r:
					self.runReloadfunction = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					self.XMOVE = 0
					self.leftWalk = False
					self.rightWalk = False
			if event.type == pygame.KEYDOWN:
				# MOVE UP
				if event.key == pygame.K_w and self.isJump == False:
					self.YMOVE = 0 - velocity
					self.y -= self.YMOVE
					if self.mx > self.x:
						self.rightWalk = True
						self.leftWalk = False
					else:
						self.rightWalk = False
						self.leftWalk = True
				# MOVE DOWN
				elif event.key == pygame.K_s and self.isJump == False:
					self.YMOVE = 0 + velocity
					self.y += self.YMOVE
					if self.mx > self.x:
						self.rightWalk = True
						self.leftWalk = False
					else:
						self.rightWalk = False
						self.leftWalk = True
					
			if event.type == pygame.KEYUP and self.isJump == False:
				if event.key == pygame.K_w or event.key == pygame.K_s and self.isJump == False:
					self.YMOVE = 0
					self.leftWalk = False
					self.rightWalk = False
			#	FIRE BULLET
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == LEFT:
					centerX = self.x + 70
					centerY = self.y + 70
					position = pygame.mouse.get_pos()
					if self.bulletMagazine > 0:
						bullets.append([math.atan2(position[1]-(centerY),position[0]-(centerX)),(centerX),(centerY)])
						self.bulletMagazine -= 1
		if self.runReloadfunction == True:
			self.reload()
		self.x += self.XMOVE
		self.y += self.YMOVE
	def __repr__(self):
		pass
	def __str__(self):
		pass
class weapon(character):
	# image of paintball gun
	gunImg = pygame.image.load("pistol.png")
	gunImgScale = pygame.transform.scale(gunImg, (50,25))
	gunImgCopy = gunImgScale.copy()
	# paintball bullet image
	paintBallBullet = pygame.image.load("circle.png")
	paintBallBulletScale = pygame.transform.scale(paintBallBullet,(8,8))
	paintBallBulletCopy = paintBallBulletScale.copy()

	paintBallGunCopy_rect = gunImgCopy.get_rect()

	def __init__(self, class_character):
		self.x = class_character.x
		self.y = class_character.y

	def draw_paintball_gun(self,mx,my):
		self.mx = mx
		self.my = my

		centerX = self.x + 70
		centerY = self.y + 70

		angle = math.atan2(self.my - (centerY), self.mx - (centerX))

		left = -1.6741997891848224 
		leftFlip = pygame.transform.flip(self.gunImgCopy,False,True)

		#	GUN ROTATE IMG
		if self.mx <= self.x + 60:
			paintBallGunRotLeft = pygame.transform.rotate(leftFlip,360-angle*57.29)
			paintBallGunPosLeft = ((centerX) - paintBallGunRotLeft.get_rect().width/2,(centerY) - paintBallGunRotLeft.get_rect().height/2)
			screen.blit(paintBallGunRotLeft,paintBallGunPosLeft)
		else:
			paintBallGunRot = pygame.transform.rotate(self.gunImgCopy,360-angle*57.29)
			paintBallGunPos = ((centerX) - paintBallGunRot.get_rect().width/2,(centerY) - paintBallGunRot.get_rect().height/2)
			screen.blit(paintBallGunRot,paintBallGunPos)
	def bullet(self):

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


		#else:
			#reloadTime += 1
			#if reloadTime == 150:	# 5 seconds * 60frames per second
			#	reloadTime = 0
			#	bulletMagazine = 10

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
def menu():
	while True:

		mx,my = pygame.mouse.get_pos()
		clock.tick(FPS)

		screen.fill(WHITE)

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
		a = pygame.draw.rect(screen, RED, button_1,width=0,)
		draw.draw_text('PLAY', font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 12.5)
		pygame.display.update()

def main():

	global screen, running, time

	x = 300
	y = 400
	leftWalk = False
	rightWalk = False
	walkCount = 0
	XMOVE = 0
	YMOVE = 0

	scroll = [0,0]

	character1 = character(x,y,leftWalk,rightWalk,walkCount,XMOVE,YMOVE)
	while running:

		mx,my = pygame.mouse.get_pos()

		screen.fill(WHITE)

		character1.move()
		scroll[0] += (character1.x-scroll[0]-(WIN_WIDTH/2))/20
		scroll[1] += (character1.y-scroll[1]-(WIN_HEIGHT/2))/20
		character1.draw(mx,my,scroll)
		character1.jump()

		#paintball1 = weapon(character1)
		#paintball1.draw_paintball_gun(mx,my)
		#paintball1.bullet()
		'''		TEST YOUR STUFF HERE		'''
		time += 1
		draw.draw_text('TIME:          ' + str(time), font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 12.5)
		draw.draw_text('RELOADTIME:        ' + str(character1.reloadTime), font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 50)
		healthpoints = draw.draw_rectangle(((1920-600)/2) + 85,((1080-300)/2) + 380,200,25,GREEN,True,3)
		manapoints = draw.draw_rectangle(((1920-600)/2) + 85,((1080-300)/2) + 410,200,25,BLUE,True,3)
		clock.tick(FPS)
		pygame.display.update()

if __name__ == "__main__":
	menu()