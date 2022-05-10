import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
import time

def add_coordinates_with_speed(a, b, s):
	return [a[0] + (b[0] * s), a[1] + (b[1] * s)]

class Colors:
	def __init__(this):
		this.white = [255, 255, 255]
		this.red = [255, 0, 0]
		this.green = [0, 255, 0]
		this.black = [0, 0, 0]
		this.blue = [0, 0, 255]

class Slab:
	def __init__(this, size, step_size, orientation, display_height, pixel_size, position):
		this.size = size
		this.step_size = step_size
		this.pixel_size = pixel_size
		this.orientation = orientation
		this.display_height = display_height
		this.position = position
		this.pixel_slab_size = this.size * this.pixel_size
		this.buffer_top_size = 0 + this.pixel_slab_size
		this.buffer_bottom_size = this.display_height - this.pixel_slab_size

	def move(this, movement):
		if movement == 1:
			if this.position - this.step_size < this.buffer_top_size:
				this.position = this.buffer_top_size
			else:
				this.position -= this.step_size
		elif movement == 0:
			if this.position + this.step_size > this.buffer_bottom_size:
				this.position = this.buffer_bottom_size
			else:
				this.position += this.step_size

class Ball:
	def __init__(this, speed, display_width, display_height, pixel_size, position, direction):
		this.direction = direction
		this.pixel_size = pixel_size
		this.speed = speed
		this.display_width = display_width
		this.display_height = display_height
		this.radius = this.pixel_size / 2
		this.position = position
		this.buffer_top_size = 0 + (this.radius)
		this.buffer_bottom_size = this.display_height - (this.radius)
		this.buffer_left_size = 0 + (this.radius)
		this.buffer_right_size = this.display_width - (this.radius)
		this.buffer_left_slab_size = 0 + (this.radius) + this.pixel_size
		this.buffer_right_slab_size = this.display_width - (this.radius) - this.pixel_size

	def step(this, left_slab, right_slab):
		if this.position[0] < this.buffer_left_size:
			return 'Left'
		if this.position[0] > this.buffer_right_size:
			return 'Right'
		temp = 0
		if this.position[1] <= this.buffer_top_size:
			this.direction[1] = 1
		if this.position[1] >= this.buffer_bottom_size:
			this.direction[1] = -1
		if this.position[0] <= this.buffer_left_slab_size and this.position[1] >= left_slab.position - left_slab.pixel_slab_size and this.position[1] <= left_slab.position + left_slab.pixel_slab_size:
			this.direction[0] = 1
			temp = ['Left', 1]
		if this.position[0] >= this.buffer_right_slab_size and this.position[1] >= right_slab.position - right_slab.pixel_slab_size and this.position[1] <= right_slab.position + right_slab.pixel_slab_size:
			this.direction[0] = -1
			temp = ['Right', 1]
		this.position = add_coordinates_with_speed(this.position, this.direction, this.speed)
		return temp

class Display():
	def __init__(this, display_width, display_height):
		this.display_width = display_width
		this.display_height = display_height
		this.screen = pygame.display.set_mode([this.display_width, this.display_height])
		pygame.display.set_caption("Ping-Pong Tron")

	def fill(this, color):
		this.screen.fill(color)

	def update(this):
		pygame.display.update()

	def circle(this, coordinates, radius, color):
		pygame.draw.circle(this.screen, color, coordinates, radius)

	def rect(this, coordinates, color):
		pygame.draw.rect(this.screen, color, coordinates)

	def quit(this):
		pygame.display.quit()
		pygame.quit()

class Environment:
	def __init__(this, time_delay = 0.01, ball_speed = 10, slab_step_size = 10, pixel_size = 30, slab_size = 2, display_width = 1500, display_height = 900, headless = False, automatic = False, left_slab_position = 900 / 2, right_slab_position = 900 / 2, ball_position = [1500 / 2, random.randint(100, 800)], ball_direction = [random.choice([1, -1]), random.choice([1, -1])]):
		this.headless = headless
		this.score = 0
		this.time_delay = time_delay
		this.automatic = automatic
		this.ball_speed = ball_speed
		this.colors = Colors()
		this.slab_step_size = slab_step_size
		this.pixel_size = pixel_size
		this.slab_size = slab_size
		this.display_width = display_width
		this.display_height = display_height
		this.left_slab = Slab(this.slab_size, this.slab_step_size, 1, this.display_height, this.pixel_size, left_slab_position)
		this.right_slab = Slab(this.slab_size, this.slab_step_size, 2, this.display_height, this.pixel_size, right_slab_position)
		this.ball = Ball(this.ball_speed, this.display_width, this.display_height, this.pixel_size, ball_position, ball_direction)
		if not this.headless:
			this.display = Display(this.display_width, this.display_height)

	def play(this):
		if not this.headless:
			this.render()
			time.sleep(3)
			boolean = True
			while boolean:
				time.sleep(this.time_delay)
				temp = this.step()
				if temp == 'Left' or temp == 'Right':
					boolean = False
					this.game_over(temp)
					break
				this.render()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						boolean = False
				if not this.automatic:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_UP]:
						this.right_slab.move(1)
					if keys[pygame.K_DOWN]:
						this.right_slab.move(0)
					if keys[pygame.K_w]:
						this.left_slab.move(1)
					if keys[pygame.K_s]:
						this.left_slab.move(0)
					if keys[pygame.K_q]:
						boolean = False
				else:
					keys = pygame.key.get_pressed()
					if keys[pygame.K_q]:
						boolean = False
					if keys[pygame.K_UP]:
						this.right_slab.move(1)
					if keys[pygame.K_DOWN]:
						this.right_slab.move(0)
# 					if this.right_slab.position > this.ball.position[1]:
# 						this.right_slab.move(1)
# 					else:
# 						this.right_slab.move(0)
					if this.left_slab.position > this.ball.position[1]:
						this.left_slab.move(1)
					else:
						this.left_slab.move(0)

	def step(this):
		temp = this.ball.step(this.left_slab, this.right_slab)
		if type(temp) == list:
			print(temp[0], 'has continued the streak of', str(this.score))
			this.score += temp[1]
		return temp

	def game_over(this, orientation):
		print(orientation, 'lost with a streak of', str(this.score))
		return this.score

	def render(this):
		if not this.headless:
			this.display.fill(this.colors.black)
			this.display.rect([0, this.left_slab.position - this.left_slab.pixel_slab_size, this.pixel_size, 2 * this.left_slab.pixel_slab_size], this.colors.red)
			this.display.rect([this.display_width - this.pixel_size, this.right_slab.position - this.right_slab.pixel_slab_size, this.pixel_size, 2 * this.right_slab.pixel_slab_size], this.colors.red)
			this.display.circle([this.ball.position[0], this.ball.position[1]], this.ball.radius, this.colors.green)
			this.display.update()

if __name__ == "__main__":
	environment = Environment(headless = False, automatic = False, time_delay = 0.009)
	environment.play()
