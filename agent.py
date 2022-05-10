import json
import os
from environment import *
import math

class Agent:
	def __init__(this, alpha, gamma, orientation):
		this.alpha = alpha
		this.orientation = orientation
		this.gamma = gamma
		this.dataset = None
		if not os.path.exists('dataset.json'):
			file = open('dataset.json', 'w')
			file_data = {
				"information": {
					"games": 0,
					"highest_streak": 0
				},
				"q_table": {}
			}
			json.dump(file_data, file, indent = 4)
			file.close()
		this.env = None

	def dump_dataset(this):
		file = open('dataset.json', 'w')
		json.dump(this.dataset, file, indent = 4)
		file.close()

	def load_dataset(this):
		file = open('dataset.json', 'r')
		this.dataset = json.load(file)
		file.close()

	def state_string_generator(this):
		if this.orientation == 'Left':
			return '|' + str(this.env.left_slab.position) + '|' + str(this.env.ball.position) + '|' + str(this.env.ball.direction) + '|'
		elif this.orientation == 'Right':
			return '|' + str(this.env.right_slab.position) + '|' + str(this.env.ball.position) + '|' + str(this.env.ball.direction) + '|'

	def reward_generator(this):
		if this.orientation == 'Left':
			up = math.dist((this.env.ball.position[0], this.env.ball.position[1]), (0 + (this.env.pixel_size / 2), this.env.left_slab.position - this.env.left_slab.step_size))
			down = math.dist((this.env.ball.position[0], this.env.ball.position[1]), (0 + (this.env.pixel_size / 2), this.env.left_slab.position + this.env.left_slab.step_size))
		elif this.orientation == 'Right':
			up = math.dist((this.env.ball.position[0], this.env.ball.position[1]), (this.env.display_height - (this.env.pixel_size / 2), this.env.left_slab.position - this.env.left_slab.step_size))
			down = math.dist((this.env.ball.position[0], this.env.ball.position[1]),  (this.env.display_height - (this.env.pixel_size / 2), this.env.left_slab.position + this.env.left_slab.step_size))
		return [down, up]

	def train(this, games_count):
		this.load_dataset()
		this.dataset['information']['games'] += games_count
		for i in range(games_count):
			this.env = Environment(headless = False)
			boolean = True
			score = 0
			if not this.env.headless:
				this.env.render()
			while boolean:
				temp = this.env.step()
				if temp == 'Left' or temp == 'Right':
					boolean = False
					score = this.env.game_over(temp)
					if this.dataset['information']['highest_streak'] < score:
						this.dataset['information']['highest_streak'] = score
					break
				if not this.env.headless:
					this.env.render()
				state = this.state_string_generator()
				reward = this.reward_generator()
				temp_action = -1
				if (reward[0] > reward[1]):
					temp_action = 1
				else:
					temp_action = 0
				this.env.right_slab.move(temp_action)
				if this.orientation == 'Left':
					if this.env.right_slab.position > this.env.ball.position[1]:
						this.env.right_slab.move(1)
					else:
						this.env.right_slab.move(0)
				elif this.orientation == 'Right':
					if this.env.left_slab.position > this.env.ball.position[1]:
						this.env.left_slab.move(1)
					else:
						this.env.left_slab.move(0)
				if state not in this.dataset['q_table']:
					this.dataset['q_table'][state] = {
						"up": 0,
						"down": 0
					}
				temp1 = this.dataset['q_table'][state]
				if temp_action == 1:
					this.dataset['q_table'][state]['up'] = round(temp1['up'] + (this.alpha * (reward[temp_action] + (this.gamma * max(temp1['up'], temp1['down'])) - temp1['up'])), 5)
				else:
					this.dataset['q_table'][state]['down'] = round(temp1['down'] + (this.alpha * (reward[temp_action] + (this.gamma * max(temp1['up'], temp1['down'])) - temp1['down'])), 5)
		this.dump_dataset()

#
# 	def evaluate(this):
# 		this.load_dataset()
# 		this.env = Environment(headless = False)
# 		this.env.render()
# 		boolean = TRue
# 		while boolean:
# 			time.sleep(this.env.time_delay)
# 			temp = this.env.step()
# 			if temp == 'Left' or temp == 'Right':
# 				boolean = False
# 				this.game_over(temp)
# 				break
# 			this.render()

if __name__ == "__main__":
	agent = Agent(0.1, 0.1, 'Right')
	agent.train(10)
