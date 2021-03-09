import sys,pygame, time, random, math
from math import sqrt
from pygame.locals import *
import draw
from images import *
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
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,128,0
BLUE = 0,255,255
img = pygame.image.load('nightSky.jpg').convert_alpha(screen)
def background_img(image):
	screen.blit(image,(0,0))

background_objects = [[0.25,[1000,50,200,800]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
def background_blocks(scroll):
	pygame.draw.rect(screen,(7,80,75),pygame.Rect(0,120,300,80))
	for background_object in background_objects:
		obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
		#if background_object[0] == 0.5:
		#	pygame.draw.rect(screen,(14,222,150),obj_rect)
		#else:
		pygame.draw.rect(screen,(9,91,85),obj_rect)

def load_map(path):
	with open(path + '.txt', 'r') as map:
		data = map.read()
		data = data.split('\n')
		game_map = []
		for row in data:
			game_map.append(list(row))
		return game_map
def display_map(game_map, x, y, scroll):
	display_map.tile_rects = []
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
				display_map.tile_rects.append(pygame.Rect(x*WIDTH,y*WIDTH,WIDTH,WIDTH))
			x += 1
		y += 1

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles,K_s):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
   
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0 and K_s == False:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] > 0 and K_s == True:
        	collision_types['bottom'] = False
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
	
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

	def __init__(self,x,y,leftWalk,rightWalk,walkCount,XMOVE,YMOVE, vertical_momentum, air_timer):
		self.x = x
		self.y = y
		self.leftWalk = leftWalk
		self.rightWalk = rightWalk
		self.walkCount = walkCount
		self.XMOVE = XMOVE
		self.YMOVE = YMOVE
		self.K_s = False
		self.jumpCount = 10
		self.bulletMagazine = 10
		self.reloadTime = 0
		self.runReloadfunction = False
		self.vertical_momentum = vertical_momentum
		self.air_timer = air_timer
		self.player_rect = pygame.Rect(self.x,self.y,100,100)
		self.isJump = False
		self.timer = 0
	
	def draw_bulletMagazine(self):
		draw.draw_text("Ammo:    " + str(self.bulletMagazine),font, GREEN,screen,950,775)

	def draw(self,mx,my, scroll):
		self.mx = mx
		self.my = my
		self.scroll0 = scroll[0]
		self.scroll1 = scroll[1]

		if self.walkCount + 1 >= FPS:
			self.walkCount = 0
		#	LEFTWALK ANIMATION
		frames = 12
		if self.leftWalk:
			if self.mx > self.x + 50:
				screen.blit(self.walkRight[self.walkCount//frames], (self.player_rect.x - self.scroll0,self.player_rect.y - self.scroll1))
				self.walkCount += 1
			else:

				screen.blit(self.walkLeft[self.walkCount//frames], (self.player_rect.x - self.scroll0,self.player_rect.y - self.scroll1))
				self.walkCount += 1
		#	RIGHTWALK ANIMATION
		if self.rightWalk:
			if self.mx < self.x + 50:
				screen.blit(self.walkLeft[self.walkCount//frames], (self.player_rect.x - self.scroll0,self.player_rect.y - self.scroll1))
				self.walkCount += 1
				
			else:
				screen.blit(self.walkRight[self.walkCount//frames], (self.player_rect.x - self.scroll0,self.player_rect.y - self.scroll1))
				self.walkCount += 1
		#	BLIT LEFT OR RIGHT FACING CHARACTER STANDING STILL
		if not self.leftWalk and not self.rightWalk:

			if self.mx > self.x:
				screen.blit(self.characterImgScale, (self.player_rect.x - self.scroll0,self.player_rect.y - self.scroll1))
			else:
				screen.blit(pygame.transform.flip(self.characterImgScale,True,False),(self.player_rect.x - self.scroll0, self.player_rect.y - self.scroll1))

	def jump(self):
		if self.isJump:
			if self.jumpCount >= -10:
				neg = 1
			if self.jumpCount < 0:
				neg = - 1
			self.player_rect.y -= self.jumpCount**2 * 0.5 * neg
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

	def move(self,nozzleX,nozzleY, scroll):
		self.nozzleX = nozzleX
		self.nozzleY = nozzleY
		self.scroll0 = scroll[0]
		self.scroll1 = scroll[1]
		if self.K_s == True:
			self.timer += 1
		if self.timer > 20:
			self.timer = 0
			self.K_s = False
	
		global running

		LEFT = 1
		RIGHT = 3

		VELOCITY = 10
		# speed at which player move 
		player_movement = [0,0]
		if self.rightWalk == True:
			player_movement[0] += VELOCITY
		if self.leftWalk == True:
			player_movement[0] -= VELOCITY
		
		# GRAVITY
		player_movement[1] += self.vertical_momentum
		self.vertical_momentum += 0.9
		# TERMINAL VELOCITY
		if self.vertical_momentum > VELOCITY * 1.5:
			self.vertical_momentum = VELOCITY * 1.5
		#	COLLISION FUNCTION

		self.player_rect, self.collisions = move(self.player_rect, player_movement, display_map.tile_rects,self.K_s)

		#	IF PLAYER BOTTOM.Y == PLATFORM.Y
		if self.collisions['bottom'] == True:
			self.air_timer = 0
			self.vertical_momentum = 0
		else:
			self.air_timer += 1
		# START FALLING IF HIT BOTTOM OF PLATFORM
		if self.collisions['top'] == True:
			self.air_timer = 21
			self.vertical_momentum += 0.9
		
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
					self.leftWalk = True
					self.rightWalk = False
				# MOVE RIGHT
				elif event.key == pygame.K_d:
					#self.XMOVE = 0 + velocity
					#self.x += self.XMOVE
					self.leftWalk = False
					self.rightWalk = True
				elif event.key == pygame.K_ESCAPE:
					menu()
				#	JUMP
				elif event.key == pygame.K_SPACE:
					if self.air_timer < 20:
						self.vertical_momentum = -16.8
						self.air_timer = 21
				elif event.key == pygame.K_s:
					self.K_s = True
					print('DOWN')				

				elif event.key == pygame.K_r:
					self.runReloadfunction = True
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d:
					self.leftWalk = False
					self.rightWalk = False
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w or event.key == pygame.K_s:
					self.leftWalk = False
					self.rightWalk = False
			#	FIRE BULLET
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == LEFT and not self.runReloadfunction == True:
					centerX = self.player_rect.x + 70
					centerY = self.player_rect.y + 70
					position = pygame.mouse.get_pos()
					if self.bulletMagazine > 0:
						'''						COORDINATES OF BULLET IN TIME            		       '''
						bullets.append([math.atan2((position[1])-(centerY - self.scroll1),(position[0])-(centerX - self.scroll0)),(centerX - self.scroll0),(centerY - self.scroll1)])
						self.bulletMagazine -= 1
					#centerX = self.x + 70
					#centerY = self.y + 70
					#position = pygame.mouse.get_pos()
					#if self.bulletMagazine > 0:
					#	bullets.append([math.atan2(position[1]-(centerY),position[0]-(centerX)),(centerX),(centerY)])
					#	self.bulletMagazine -= 1
		print(self.K_s)
		if self.runReloadfunction == True:
			self.reload()
	def __repr__(self):
		pass
	def __str__(self):
		pass
class weapon(character):

	gunImgScale = pygame.transform.scale(gunImg, (50,25))
	gunImgCopy = gunImgScale.copy()

	gunImgScale1 = pygame.transform.scale(gunImg1, (50,25))
	gunImgCopy1 = gunImgScale1.copy()

	paintBallBulletScale = pygame.transform.scale(paintBallBullet,(8,8))
	paintBallBulletCopy = paintBallBulletScale.copy()

	paintBallGunCopy_rect = gunImgCopy.get_rect()

	def __init__(self, class_character, mx, my, scroll):
		self.scroll0 = scroll[0]
		self.scroll1 = scroll[1]
		self.x = class_character.player_rect.x
		self.y = class_character.player_rect.y
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
		if self.mx <= self.x - self.scroll0:
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
		pygame.draw.line(screen, (RED),(xr,yr),(self.mx,self.my))	# FIRE BULLET MECHANIC
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

	x = (1920-600)/2 + 85
	y = (1920-600)/2 + -300
	leftWalk = False
	rightWalk = False
	walkCount = 0
	vertical_momentum = 0
	air_timer = 0
	scroll = [0,0]
	game_map = load_map('map')
	character1 = character(x,y,leftWalk,rightWalk,walkCount,0,0, vertical_momentum, air_timer)
	while running:
		screen.fill(BLACK)
		
		scroll[0] += (character1.player_rect.x-scroll[0]-x)//15
		scroll[1] += (character1.player_rect.y-scroll[1]-y)//15
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])
		background_blocks(scroll)
		display_map(game_map, character1.player_rect.x, character1.player_rect.y, scroll)

		mx,my = pygame.mouse.get_pos()
		paintball1 = weapon(character1, mx, my, scroll)
		character1.move(paintball1.paintBallGunPos[0],paintball1.paintBallGunPos[1], scroll)
		character1.draw(mx,my, scroll)
		character1.draw_bulletMagazine()

		paintball1.draw_paintball_gun()
		# character1.jump() 
		'''		TEST YOUR STUFF HERE		'''
		time += 1
		draw.draw_text('TIME:          ' + str(time), font, (WHITE), screen, ((1920-600)/2) + 85,((1080-300)/2) - 100)
		draw.draw_text('RELOADTIME:        ' + str(character1.reloadTime), font, (WHITE), screen, ((1920-600)/2) + 85,((1080-300)/2) - 50)
		healthpoints = draw.draw_rectangle(((1920-600)/2) + 85,((1080-300)/2) + 380,200,25,GREEN,True,3)
		manapoints = draw.draw_rectangle(((1920-600)/2) + 85,((1080-300)/2) + 410,200,25,BLUE,True,3)
		platform = draw.draw_rectangle(((1920-600)/2) - scroll[0],((1080-300)/2)+150 - scroll[1],200,25,GREEN,True,3)
		clock.tick(FPS)
		pygame.display.update()

if __name__ == "__main__":
	main()