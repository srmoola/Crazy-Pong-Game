import pygame
import time

pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()	
FPS = 60



class Striker:
		
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		self.geekRect = pygame.Rect(posx, posy, width, height)
		self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

	def display(self):
		self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		if self.posy <= 0:
			self.posy = 0
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		self.geekRect = (self.posx, self.posy, self.width, self.height)
	
	def updateX(self, xFac):
		self.posx = self.posx + self.speed*xFac

		if self.posx <= 0:
			self.posx = 0
		if self.posx >= 890:
			self.posx = 890
	
		self.geekRect = (self.posx, self.posy, self.width, self.height)

	def resetPos(self):
		self.posx = 10
		self.posy = 250
	
	def resetPos2(self):
		self.posx = 880
		self.posy = 250
	
	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):
		return self.geekRect



class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 0.75
		self.yFac = -0.75
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		
		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		time.sleep(1)
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1
		

	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball



def main():
	running = True

	


	geek1 = Striker(20, 0, 10, 100, 10, GREEN)
	geek2 = Striker(WIDTH-30, 0, 10, 100, 10, RED)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

	listOfGeeks = [geek1, geek2]

	geek1Score, geek2Score = 0, 0
	geek1YFac, geek2YFac = 0, 0
	geek1XFac, geek2XFac = 0,0

	while running:
		screen.fill(BLACK)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					geek2YFac = -1
				if event.key == pygame.K_DOWN:
					geek2YFac = 1
				if event.key == pygame.K_LEFT:
					geek2XFac = -1
				if event.key == pygame.K_RIGHT:
					geek2XFac = 1
				if event.key == pygame.K_w:
					geek1YFac = -1
				if event.key == pygame.K_s:
					geek1YFac = 1
				if event.key == pygame.K_a:
					geek1XFac = -1
				if event.key == pygame.K_d:
					geek1XFac = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					geek2YFac = 0
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					geek2XFac = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					geek1YFac = 0
				if event.key == pygame.K_a or event.key == pygame.K_d:
					geek1XFac = 0

		for geek in listOfGeeks:
			if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
				ball.hit()

		geek1.update(geek1YFac)
		geek2.update(geek2YFac)
		geek2.updateX(geek2XFac)
		geek1.updateX(geek1XFac)
		point = ball.update()

		
		if point == -1:
			geek1Score += 1
		elif point == 1:
			geek2Score += 1

		
		if point:
			ball.reset()
			geek1.resetPos()
			geek2.resetPos2()
			

		geek1.display()
		geek2.display()
		ball.display()

		geek1.displayScore("Player 1: ",
						geek1Score, 100, 20, WHITE)
		geek2.displayScore("Player 2: ",
						geek2Score, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)	


if __name__ == "__main__":
	main()
	pygame.quit()
