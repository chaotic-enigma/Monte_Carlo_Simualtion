import dash
import random
import time
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

def category_guess(num, category):
	roulette = {
		'b' : [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35],
		'r' : [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
	}

	whole = []
	for i,j in roulette.items():
		for k in j:
			rb = {}
			rb.update({i : k})
			whole.append(rb)

	for table in whole:
		for k, v in table.items():
			if num == v and category == k:
				return True

def even_property(num):
	if num % 2 == 0:
		return True 

spin_wheel = range(0, 37)
table_guess = range(1 ,37)

category = ['even', 'odd']

def exact_guessing():
	color = ['b', 'r']
	dozen1_even = range(1, 13)
	dozen2_r_b = range(13, 25)
	dozen3_odd = range(25, 37)

	guess_num = random.choice(table_guess)

	if guess_num in dozen1_even:
		if category_guess(guess_num, color[0]):
			if even_property(guess_num):
				#print('guessed number is {} (even) belongs to {}'.format(guess_num, color[0]))
				return guess_num
			else:
				#print('guessed number is {} (odd) belongs to {}'.format(guess_num, color[0]))
				return guess_num
		if category_guess(guess_num, color[1]):
			if even_property(guess_num):
				#print('guessed number is {} (even) belongs to {}'.format(guess_num, color[1]))
				return guess_num				
			else:
				#print('guessed number is {} (odd) belongs to {}'.format(guess_num, color[1]))
				return guess_num

	elif guess_num in dozen2_r_b:
		if category_guess(guess_num, color[0]):
			if even_property(guess_num):
				#print('guessed number is {} (even) belongs to {}'.format(guess_num, color[0]))
				return guess_num
			else:
				#print('guessed number is {} (odd) belongs to {}'.format(guess_num, color[0]))
				return guess_num
		if category_guess(guess_num, color[1]):
			if even_property(guess_num):
				#print('guessed number is {} (even) belongs to {}'.format(guess_num, color[1]))
				return guess_num
			else:
				#print('guessed number is {} (odd) belongs to {}'.format(guess_num, color[1]))
				return guess_num

	elif guess_num in dozen3_odd:
		if category_guess(guess_num, color[0]):
			if not even_property(guess_num):
				#print('guessed number is {} (odd) belongs to {}'.format(guess_num, color[0]))
				return guess_num
			else:
				#print('guessed number is {} (even) belongs to {}'.format(guess_num, color[0]))
				return guess_num
		if category_guess(guess_num, color[1]):
			if not even_property(guess_num):
				#print('guessed number is {} (odd) belongs to {}'.format(guess_num, color[1]))
				return guess_num
			else:
				#print('guessed number is {} (even) belongs to {}'.format(guess_num, color[1]))
				return guess_num

	else:
		print('guessed number is 0')
		return 0

def gambling_roulette(total_betting, initial_betting, chances):
	outcome_amt = total_betting
	wager_betting = initial_betting

	wx = []
	vy = []

	turns = 1
	while turns <= chances:
		ball = random.choice(spin_wheel)
		#print('turned out number {}'.format(ball))
		if ball == exact_guessing():
			outcome_amt += wager_betting
			wx.append(turns)
			vy.append(outcome_amt)
		else:
			outcome_amt -= wager_betting
			wx.append(turns)
			vy.append(outcome_amt)

		turns += 1

	if outcome_amt < 0:
		outcome_amt = 'broke'

	#print('Amount Left: {}'.format(outcome_amt))

	return wx, vy

# for i in range(100):
# 	gambling_roulette(10000, 100, 100)

def martingale_strategy(total_betting, initial_betting, chances):
	outcome_amt = total_betting
	wager_betting = initial_betting
	strategy = wager_betting * 2

	previous_turn = 'win'

	wx = []
	vy = []

	turns = 1
	while turns <= chances:
		ball = random.choice(spin_wheel)
		if previous_turn == 'win':
			if ball == exact_guessing():
				outcome_amt += wager_betting
				#print('betting {}'.format(wager_betting))
				wx.append(turns)
				vy.append(outcome_amt)
			else:
				outcome_amt -= strategy
				previous_turn = 'lose'
				wx.append(turns)
				vy.append(outcome_amt)
				if outcome_amt < 0:
					break

		elif previous_turn == 'lose':
			if ball == exact_guessing():
				outcome_amt += wager_betting
				#print('betting {}'.format(strategy))
				previous_turn = 'win'
				wx.append(turns)
				vy.append(outcome_amt)
			else:
				outcome_amt -= strategy
				if outcome_amt < 0:
					break
				previous_turn = 'lose'
				wx.append(turns)
				vy.append(outcome_amt)

		turns += 1

	#print('Amount Left: {}'.format(outcome_amt))
	return wx, vy

wx1, vy1 = gambling_roulette(10000, 10, 100)
wx2, vy2 = martingale_strategy(10000, 10, 100)

app.layout = html.Div([
	dcc.Graph(
		id='example_graph',
		figure={
			'data' : [
				{'x' : wx1, 'y' : vy1, 'type' : 'line', 'name' : 'gambling_roulette'},
				{'x' : wx2, 'y' : vy2, 'type' : 'line', 'name' : 'martingale_strategy'}
			],
			'layout' : {'title' : 'Monte Carlo Simulation (roulette guess game)'}
		}
	)
])

if __name__ == '__main__':
	app.run_server(debug=True)