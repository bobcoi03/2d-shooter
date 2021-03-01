import sys, pygame, time, random, math
from math import sqrt
from pygame.locals import *
import draw
from map1 import grass_img_scale, dirt_img_scale
pygame.init()

clock = pygame.time.Clock()
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 600
screen = pygame.display.set_mode((WIN_SIZE), pygame.RESIZABLE)
font = pygame.font.Font("freesansbold.ttf",13)
running = True
#
bullets = []
#	TIME
time = 0
FPS = 60

WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,128,0
BLUE = 0,255,255
def load_map(path):
	with open(path + '.txt', 'r') as map:
		data = map.read()
		data = data.split('\n')
		game_map = []
		for row in data:
			game_map.append(list(row))
		return game_map

game_map = load_map('map')

def display_map(game_map, x, y, scroll):
	tile_rects = []
	y = 0
	for layer in game_map:
		x = 0
		for tile in layer:
			WIDTH = 50
			if tile == '1':
				screen.blit(dirt_img_scale,(x*WIDTH-scroll[0],y*WIDTH - scroll[1]))
			if tile == '2':
				screen.blit(grass_img_scale,(x*WIDTH-scroll[0],y*WIDTH - scroll[1]))
			if tile != '0':
				tile_rects.append(pygame.Rect(x*WIDTH,y*WIDTH,WIDTH,WIDTH))
			x += 1
		y += 1
class character:
	# character image
	characterImg = pygame.image.load("thief1.png").convert_alpha()
	characterImg.set_colorkey(BLUE)
	characterImgScale = pygame.transform.scale(characterImg,(100,100))
	characterImgCopy = characterImgScale.copy()
	#	ANIMATION SPRITE
	walkRightLoad = [pygame.image.load("thief1_running.png"),pygame.image.load("thief1_running2.png"),pygame.image.load("thief1_running3.png"),pygame.image.load("thief1_running4.png"),pygame.image.load("thief1_running5.png"),]
	walkRight = [pygame.transform.scale(walkRightLoad[0],(100,100)),pygame.transform.scale(walkRightLoad[1],(100,100)),pygame.transform.scale(walkRightLoad[2],(100,100)),pygame.transform.scale(walkRightLoad[3],(100,100)),pygame.transform.scale(walkRightLoad[4],(100,100))]
	walkLeft = [pygame.transform.flip(walkRight[0],True,False),pygame.transform.flip(walkRight[1],True,False),pygame.transform.flip(walkRight[2],True,False),pygame.transform.flip(walkRight[3],True,False),pygame.transform.flip(walkRight[4],True,False)]

	runReloadfunction = False

	def __init__(self,x,y,leftWalk,rightWalk,walkCount,XMOVE,YMOVE, scroll):
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
		self.scroll0 = scroll[0]
		self.scroll1 = scroll[1]
	
	def draw_bulletMagazine(self):
		draw.draw_text("Ammo:    " + str(self.bulletMagazine),font, GREEN,screen,950,775)

	def draw(self,mx,my):
		self.mx = mx
		self.my = my

		if self.walkCount + 1 >= FPS:
			self.walkCount = 0
		#	LEFTWALK ANIMATION
		frames = 12
		if self.leftWalk:
			if self.mx > self.x + 50:
				screen.blit(self.walkRight[self.walkCount//frames], (self.x - self.scroll0,self.y - self.scroll1))
				self.walkCount += 1
			else:

				screen.blit(self.walkLeft[self.walkCount//frames], (self.x - self.scroll0,self.y - self.scroll1))
				self.walkCount += 1
		#	RIGHTWALK ANIMATION
		if self.rightWalk:
			if self.mx < self.x + 50:
				screen.blit(self.walkLeft[self.walkCount//frames], (self.x - self.scroll0,self.y - self.scroll1))
				self.walkCount += 1
				
			else:
				screen.blit(self.walkRight[self.walkCount//frames], (self.x - self.scroll0,self.y - self.scroll1))
				self.walkCount += 1
		#	BLIT LEFT OR RIGHT FACING CHARACTER STANDING STILL
		if not self.leftWalk and not self.rightWalk:

			if self.mx > self.x - self.scroll0:
				screen.blit(self.characterImgScale, (self.x - self.scroll0,self.y - self.scroll1))
			else:
				screen.blit(pygame.transform.flip(self.characterImgScale,True,False),(self.x - self.scroll0,self.y - self.scroll1))

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
		self.reloadTime += 1
		if self.reloadTime >= 150:
			self.bulletMagazine = 10
			self.reloadTime = 0
			self.runReloadfunction = False
		draw.draw_text("Reloading....", font, RED,screen, ((1920-600)/2) + 85,((1080-300)/2) -100)

	def move(self,nozzleX,nozzleY):
		self.nozzleX = nozzleX
		self.nozzleY = nozzleY
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
					print("space is pressed")
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
						'''						COORDINATES OF BULLET IN TIME            		       '''
						bullets.append([math.atan2((position[1])-(centerY - self.scroll1),(position[0])-(centerX - self.scroll1)),(centerX),(centerY)])
						self.bulletMagazine -= 1
					#centerX = self.x + 70
					#centerY = self.y + 70
					#position = pygame.mouse.get_pos()
					#if self.bulletMagazine > 0:
					#	bullets.append([math.atan2(position[1]-(centerY),position[0]-(centerX)),(centerX),(centerY)])
					#	self.bulletMagazine -= 1
		if self.runReloadfunction == True:
			self.reload()
		self.x += self.XMOVE
		self.y += self.YMOVE
	def __repr__(self):
		pass
	def __str__(self):
		pass
class weapon(character):
	# image of pistol gun
	gunImg = pygame.image.load("pistol.png")
	gunImgScale = pygame.transform.scale(gunImg, (50,25))
	gunImgCopy = gunImgScale.copy()
	# image of paintball gun
	gunImg1 = pygame.image.load("gun.png")
	gunImgScale1 = pygame.transform.scale(gunImg1, (50,25))
	gunImgCopy1 = gunImgScale1.copy()
	# paintball bullet image
	paintBallBullet = pygame.image.load("circle.png")
	paintBallBulletScale = pygame.transform.scale(paintBallBullet,(8,8))
	paintBallBulletCopy = paintBallBulletScale.copy()

	paintBallGunCopy_rect = gunImgCopy.get_rect()

	def __init__(self, class_character, mx, my):
		self.scroll0 = class_character.scroll0
		self.scroll1 = class_character.scroll1
		self.x = class_character.x
		self.y = class_character.y
		self.mx = mx
		self.my = my
		centerX = self.x + 60
		centerY = self.y + 60

		self.angle = math.atan2(self.my - (centerY - self.scroll1), self.mx - (centerX - self.scroll0))

		left = -1.6741997891848224 
		leftFlip = pygame.transform.flip(self.gunImgCopy1,False,True)
		
		#	WHEN LOOKING LEFT
		self.paintBallGunRotLeft = pygame.transform.rotate(leftFlip,360-self.angle*57.29)
		self.paintBallGunPosLeft = ((centerX - self.scroll0) - self.paintBallGunRotLeft.get_rect().width/2-25,(centerY - self.scroll1) - self.paintBallGunRotLeft.get_rect().height/2)
		self.paintBallGunRot = pygame.transform.rotate(self.gunImgCopy1,360-self.angle*57.29)
		self.paintBallGunPos = ((centerX - self.scroll0) - self.paintBallGunRot.get_rect().width/2-8,(centerY - self.scroll1) - self.paintBallGunRot.get_rect().height/2)

	def draw_paintball_gun(self):
		if self.mx <= self.x + 60:
			screen.blit(self.paintBallGunRotLeft,(self.paintBallGunPosLeft[0], self.paintBallGunPosLeft[1]))
		# 	WHEN LOOKING RIGHT
		else:
			screen.blit(self.paintBallGunRot,(self.paintBallGunPos[0], self.paintBallGunPos[1]))

		for bullet in bullets:
			bulletspeed = 25
			index = 0
			velx = math.cos(bullet[0])*bulletspeed
			vely = math.sin(bullet[0])*bulletspeed
			bullet[1] += velx
			bullet[2] += vely
			if bullet[1]<-64 or bullet[1]>2000 or bullet[2]<-64 or bullet[2]>2000:
				bullets.pop(index)
			index+= 1
			for projectile in bullets:
				bullets1 = pygame.transform.rotate(self.paintBallBulletCopy, 360-projectile[0]*57.29)
				screen.blit(bullets1, (projectile[1],projectile[2]))

	#for bullet in bullets:
	#	bulletspeed = 25
	#	index = 0
	#	vely = math.sin(bullet[0])*bulletspeed
	#	bullet[1] += velx
	#	bullet[2] += vely
	#	if bullet[1]<-64 or bullet[1]>2000 or bullet[2]<-64 or bullet[2]>2000:
	#		bullets.pop(index)
	#	index+= 1
	#	for projectile in bullets:
	#		bullets1 = pygame.transform.rotate(self.paintBallBulletCopy, 360-projectile[0]*57.29)
	#		screen.blit(bullets1, (projectile[1],projectile[2]))

		#else:
			#reloadTime += 1
			#if reloadTime == 150:	# 5 seconds * 60frames per second
			#	reloadTime = 0
			#	bulletMagazine = 10

		cos = math.cos
		sin = math.cos
		a = self.angle
		xm = self.paintBallGunPos[0]
		ym = self.paintBallGunPos[1]
		xpos = xm + 50
		ypos = ym + 12.5
		xr = (xpos - xm) * cos(a) - (ypos - ym) * sin(a) + xm
		yr = (xpos - xm) * sin(a) + (ypos - ym) * cos(a) + ym
		pygame.draw.line(screen, (RED),(xr,yr),(self.mx,self.my))


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

	x = 1920//2
	y = 1080//2
	leftWalk = False
	rightWalk = False
	walkCount = 0
	scroll = [0,0]

	character1 = character(x,y,leftWalk,rightWalk,walkCount,0,0, scroll)
	while running:
		screen.fill(BLUE)
		
		scroll[0] += ((character1.x-scroll[0])-(WIN_WIDTH/2))
		scroll[1] += ((character1.y-scroll[1])-(WIN_HEIGHT/2))
		display_map(game_map, character1.x, character1.y, scroll)

		mx,my = pygame.mouse.get_pos()
		paintball1 = weapon(character1, mx, my)
		character1.draw(mx,my)
		character1.draw_bulletMagazine()

		paintball1.draw_paintball_gun()
		if mx >= character1.x + 60:
			character1.move(paintball1.paintBallGunPos[0],paintball1.paintBallGunPos[1])
		if mx <= character1.x + 60:
			character1.move(paintball1.paintBallGunPosLeft[0],paintball1.paintBallGunPosLeft[1])
		character1.jump() 
		'''		TEST YOUR STUFF HERE		'''
		time += 1
		draw.draw_text('TIME:          ' + str(time), font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 12.5)
		draw.draw_text('RELOADTIME:        ' + str(character1.reloadTime), font, (0,0,0), screen, ((1920-600)/2) + 85,((1080-300)/2) + 50)
		healthpoints = draw.draw_rectangle(((1920-600)/2) + 85,((1080-300)/2) + 380,200,25,GREEN,True,3)
		manapoints = draw.draw_rectangle(((1920-600)/2) + 85,((1080-300)/2) + 410,200,25,BLUE,True,3)
		platform = draw.draw_rectangle(((1920-600)/2) - scroll[0],((1080-300)/2)+150 - scroll[1],200,25,GREEN,True,3)
		clock.tick(FPS)
		pygame.display.update()

if __name__ == "__main__":
	main()