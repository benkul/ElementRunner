import bacon
import copy
from random import randrange
from random import choice
from ship import Ship
from player import Player
from planets import planet_list, Planet # contains list of planets for game
from elements import element_list # contains list of element commodities for game


high_score = [] # create list to put high scores in
element_pricelist = [] # create list that is refreshed when player arrives on planet

def rarity(quantity, base_price): # determines price adjustment based on quantity on hand
	price = float(base_price * (1.0 - ((quantity/200.0))))
	if price <= 0:
		price = 1
	return price
 


def price_refresh(): # 
	for item in range(len(element_pricelist)):
		element_pricelist.pop(0)

	for item in element_list:
		element_pricelist.append([item[0], 0, randrange(1, 100), item[1]])

	for item in element_pricelist:	
		item[1] = rarity(item[2], item[3])


price_refresh() # initalizes element prices and populates list

class game_function(object): # create class that contains On/Off variables for game windows
	def __init__(self, refuel = False, bank = False, cargo = False, merchant = False, destination = False):
		self.refuel = refuel
		self.bank = bank
		self.cargo = cargo
		self.merchant = merchant
		self.destination = destination

window = game_function() # create instance of window class


fuel_cost = 21 # sets cost per unit of fuel for vehicle
#game images
title = bacon.Image('Galaxy.jpg')
background = bacon.Image('backdrop3.jpg')
star = bacon.Image('star3.png')
target = bacon.Image('pin72.png')
battery = bacon.Image('greenbattery.png')
market = bacon.Image('greenmarket.png')
depart = bacon.Image('greenrocket.png')
money = bacon.Image('greenbank.png')
cargo = bacon.Image('greencargo.png')
triangle = bacon.Image('triangle.png')
robot = bacon.Image('cargorobot.png')
redrocket = bacon.Image('redrocket.png')
ship1 = bacon.Image('dauntless.png')
ship2 = bacon.Image('firefly.png')
ship3 = bacon.Image('excelsior.png')
ship4 = bacon.Image('defiant.png')
tutorial = bacon.Image('tutorial.png')
merch1 = bacon.Image('merch1.png')
merch2 = bacon.Image('merch2.png')
merch3 = bacon.Image('merch3.png')
merch4 = bacon.Image('merch4.png')
merch5 = bacon.Image('merch5.png')
merch6 = bacon.Image('merch6.png')
merch7 = bacon.Image('merch7.png')
merch8 = bacon.Image('merch8.png')
merch9 = bacon.Image('merch9.png')
merch10 = bacon.Image('merch10.png')
# create list of merchant names
merch_list = [merch1, merch2, merch3, merch4, merch5, merch6, merch7, merch8, merch9, merch10] 



# set up game fonts
titlefont = bacon.Font('moonhouse.ttf', 40)
byline = bacon.Font('moonhouse.ttf', 20)
planet = bacon.Font('FINALOLD.ttf', 20)
robot_speak = bacon.Font('LCD_Solid.ttf', 14)

# music 
music = bacon.Sound('farewell.ogg', stream=True)

# sets ranges for the main game icons at the bottom of the screen
battery_range = {'x1': 183, 'x2': 233, 'y1': 486, 'y2': 540}
cargo_range = {'x1': 267, 'x2': 339, 'y1': 486, 'y2': 540}
market_range = {'x1': 363, 'x2': 486, 'y1': 486, 'y2': 540}
money_range = {'x1': 460, 'x2': 540, 'y1': 486, 'y2': 540}
depart_range = {'x1': 555, 'x2': 630, 'y1': 486, 'y2': 540}

planet_master = [] 
planet_locator = [] 
for item in planet_list: #create master planet list 
	planet_master.append(Planet(item[0], item[1], item[2], merch_list.pop(0)))
	planet_locator.append((item[1], item[2]))


myplayer = Player("Hobart Killjoy", "defiant", 10000, 0, 213, 196) # initialize player class
myship = Ship("Defiant", 10, 10000, 50) #initialize ship class
myship.fuel = 100 # set fuel to 100 for start
line_height = 25 # for planet font

#initalize music
music_voice = bacon.Voice(music, loop=True)
# star music at start of game
music_voice.play()

x = 360 #initialize player start position
y = 300

# create game parameters class that includes dimensions, player start position, 
bacon.window.title = 'Element Runner'
bacon.window.width = 640
bacon.window.height = 540
bacon.window.fullscreen = False

def transfer_element_to_market(product): # add product to market, return amount paid for it
		for item in element_pricelist:
			if item[0].find(product) != -1:
				item[2] += 1
				return item[1]

def depart_view(): # set view for player to travel from one planet to another
	bacon.draw_image(redrocket, 561, 485) 
	if myplayer.destination:
		bacon.draw_image(depart, 561, 485)
		bacon.push_color()
		bacon.set_color(1,1,1,1) # white
		bacon.draw_string(planet, "destination set: %s" % myplayer.destination, 400, 470)	
		bacon.pop_color
		
		bacon.push_color() # place pin
		bacon.set_color(.74, .07, .07, 1) # red
		bacon.draw_image(target, myplayer.destination_x - 7, myplayer.destination_y - 20)
		bacon.pop_color()
		
		bacon.push_color() # set fuel usage in red on gauge
		gauge_level = (179 * (myplayer.fuel_used/100.0))
		if gauge_level == 0:
			gauge_level = 14

		bacon.set_color(.74, .07, .07, 1) # red
		bacon.fill_rect(14, 496, (gauge_level), 530) 
		bacon.pop_color()

		bacon.push_color()
		bacon.set_color(0, 0, 0, 1)

		if myplayer.fuel_used > myship.fuel:
			bacon.draw_string(planet, "need more fuel", 16, 522)
		else:	
			bacon.draw_string(planet, "fuel used: %r " % myplayer.fuel_used, 16, 522)
		bacon.pop_color()


def cargo_view():
	bacon.push_color()
	bacon.set_color(1, 1, 1, 0) # white 
	bacon.draw_image(triangle, 268, 450) #point triangle at icon
	bacon.fill_rect(150, 40, 425, 450) # create white background box
	bacon.pop_color()

	bacon.push_color() # draw cargo robot
	bacon.draw_image(robot, 175, 65)
	bacon.pop_color()

	bacon.push_color()
	bacon.set_color(0, 0, 0, 1) #black
	bacon.draw_string(robot_speak, "Here is the ", (175 + robot.width + 5), 82)
	bacon.draw_string(robot_speak, "cargo manifest ", (175 + robot.width + 5), 97)
	bacon.draw_string(robot_speak, "you requested,", (175 + robot.width + 5), 112)
	bacon.draw_string(robot_speak, "Captian.", (175 + robot.width + 5), 127)
	bacon.draw_string(planet, "Name", 175, 175)
	bacon.draw_string(planet, "Cost", 295, 175)
	bacon.draw_string(planet, "Quantity", 350, 175)
	bacon.draw_string(planet, "(%d)" % myship.cargo_load_calculator(), 360, 150)
	n = 0
	for item in myship.current_cargo:
		n += 1
		bacon.draw_string(planet, "%s" % item[0], 175, (180 + (line_height * n)))
		bacon.draw_string(planet, "%d" % item[1], 295, (180 + (line_height * n)))
		bacon.draw_string(planet, "%d" % item[2], 350, (180 + (line_height * n)))
	bacon.pop_color()

def merchant_view():
	x, y = bacon.mouse.x, bacon.mouse.y
	bacon.push_color()
	bacon.set_color(1, 1, 1, 0) # white 
	bacon.draw_image(triangle, 367, 450) #point triangle at icon
	bacon.fill_rect(0, 40, 640, 450) # create white background box
	bacon.pop_color()

	bacon.push_color() 
	bacon.draw_image(robot, 20, 65) # draw cargo robot
	n = planet_locator.index((myplayer.location_x, myplayer.location_y))
	bacon.draw_image(planet_master[n].merchant_photo, 350, 65) #draw planet merchant
	bacon.pop_color()

	bacon.push_color()
	bacon.set_color(0, 0, 0, 1) #black
	bacon.draw_string(robot_speak, "Here is the ", (20 + robot.width + 5), 82) # cargo robot speech
	bacon.draw_string(robot_speak, "cargo manifest ", (20 + robot.width + 5), 97)
	bacon.draw_string(robot_speak, "you requested,", (20 + robot.width + 5), 112)
	bacon.draw_string(robot_speak, "Captian.", (20 + robot.width + 5), 127)

	bacon.draw_string(robot_speak, "Buy something,", (350 + merch1.width + 5), 82) # planet merchent speach
	bacon.draw_string(robot_speak, "will ya!?", (350 + merch1.width + 5), 97)	
	bacon.draw_string(planet, "Name", 20, 175) # current cargo labels
	bacon.draw_string(planet, "Cost", 140, 175)
	bacon.draw_string(planet, "Quantity", 195, 175)
	bacon.draw_string(planet, "(%d)" % myship.cargo_load_calculator(), 205, 150)
	n = 0
	for item in myship.current_cargo: # draw current cargo
		n += 1
		bacon.draw_string(planet, "%s" % item[0], 20, (180 + (line_height * n)))
		bacon.draw_string(planet, "%d" % item[1], 140, (180 + (line_height * n)))
		bacon.draw_string(planet, "%d" % item[2], 195, (180 + (line_height * n)))

			
	bacon.draw_string(planet, "Name", 350, 175) # merchant labels
	bacon.draw_string(planet, "Cost", 490, 175)
	bacon.draw_string(planet, "Quantity", 545, 175)

	n = 0

	for item in element_pricelist: # draw merchant quantities on hand
		n += 1
		bacon.draw_string(planet, "%s" % item[0], 350, (180 + (line_height * n)))
		bacon.draw_string(planet, "%d" % item[1], 490, (180 + (line_height * n)))
		bacon.draw_string(planet, "%d" % item[2], 545, (180 + (line_height * n)))
		bacon.push_color() # draw rectange

	
	for i, item in enumerate(myship.current_cargo, 1): # draw sell buttons for cargo
		bacon.draw_rect(
		220, (160 + (line_height * i)),
		265, (160 + line_height + line_height * i)) # draw rectange

		if x in range(220, 265) and y in range((160 + (line_height * i)), (160 + line_height + line_height * i)):
			bacon.push_color # fill rectangle on hover
			bacon.set_color(.20, .58, .03, 1) # green
			bacon.fill_rect(		
			221, (161 + (line_height * i)), 
			264, (159 + line_height + line_height * i)) 
			bacon.pop_color()
		bacon.draw_string(planet, "sell", 226, (180 + (line_height * i)))# sell text for rectangle	
	
	for i, item in enumerate(element_pricelist, 1): # draw buy buttons for merchant
		bacon.draw_rect(
		300, (160 + (line_height * i)), 
		345, (160 + line_height + line_height * i)) # draw rectange

		if x in range(300, 345) and y in range((160 + (line_height * i)), (160 + line_height + line_height * i)):
			bacon.push_color # fill rectangle on hover
			bacon.set_color(.20, .58, .03, 1)  # red
			bacon.fill_rect(		
			301, (161 + (line_height * i)), 
			344, (159 + line_height + line_height * i)) 
			bacon.pop_color()
		bacon.draw_string(planet, "buy", 308, (180 + (line_height * i)))# buy text for rectangle	
	bacon.pop_color()

def distance_and_fuel(x1, y1, x2, y2):
	myplayer.distance = int((
	(x1 - x2) ** 2 + 
	(y1 - y2) ** 2 ) **(.5)) # calculate distance to destination(x2,y2) from current point
	myplayer.fuel_used = int(((myplayer.distance/myship.velocity)/100.0) * myship.weight) # calculate fuel usage
	myplayer.distance /= 85 # modify distance to scale to screen
	if myplayer.fuel_used > 100:
		myplayer.fuel_used = 100
	return myplayer.distance, myplayer.fuel_used

def refill_tank():
	if myplayer.money_in_pocket < ((100 - myship.fuel)* fuel_cost):
		while myplayer.money_in_pocket > 0 + fuel_cost :
			myplayer.money_in_pocket -= fuel_cost
			myship.fuel += 1
	else:
		myplayer.money_in_pocket -= ((100 - myship.fuel)* fuel_cost)
		myship.fuel = 100

def banking():
	x, y = bacon.mouse.x, bacon.mouse.y

	bacon.draw_image(money, 458, 485)
	
	bacon.draw_image(triangle, 463, 450) #point triangle at icon
	bacon.fill_rect(350, 375, 620, 450) # create white background box
	
	bacon.push_color
	bacon.set_color(0, 0, 0, 1)
	bacon.draw_rect(515, 378, 617, 406) # for deposit
	bacon.draw_string(planet, "Cash: %d" % myplayer.money_in_pocket, 355, 400)
	bacon.draw_rect(515, 412, 617, 442) # for withdrawal
	bacon.draw_string(planet, "Bank: %d" % myplayer.money_in_bank, 355, 435)
	bacon.pop_color()


	bacon.push_color()		
	bacon.set_color(.20, .58, .03, 1) # green
	if x in range(515, 617) and y in range(412, 442): # withdrawal
		bacon.fill_rect(516, 413, 616, 441)

	elif x in range(515, 617) and y in range(378, 406): # deposit
		bacon.fill_rect(516, 379, 616, 405)
	bacon.pop_color()


	bacon.draw_string(planet, "Deposit", 518, 400)					
	bacon.draw_string(planet, "Withdrawal", 518, 435)


def main_view(): # call from on_tick to draw main game elements
	bacon.draw_image(background, 0, 0) # place backdrop

	for item in planet_list: # place planet names
		bacon.draw_string(planet, item[0], item[1] + 13, item[2] + 8)

	bacon.push_color() # set fuel gauge
	bacon.set_color(.2, .58, .03, 1) #green
	bacon.fill_rect(14, 496, (179 * (myship.fuel/100.0)), 530) 
	bacon.pop_color()

	bacon.push_color() # place star for current location
	bacon.draw_image(star, myplayer.location_x - 8, myplayer.location_y - 6)
	bacon.pop_color()	

	bacon.push_color()
	bacon.set_color(0,0,0,.2)
	bacon.fill_rect(0, 0, 640, 40) #HUD top bar
	bacon.set_color(1,1,1,1)
	bacon.draw_string(planet, "%s    cash: %d    bank: %d    turn: %d" % (
		myplayer.name, myplayer.money_in_pocket, myplayer.money_in_bank, myplayer.turn), 20, 30)
	bacon.pop_color()


def core_action(): # set mouse roll-over behaviour for icons on bottom of screen
	x, y = bacon.mouse.x, bacon.mouse.y	

	if x in range(
		battery_range['x1'], battery_range['x2']) and y in range(
		battery_range['y1'], battery_range['y2']):
		bacon.draw_image(battery, 189, 485)
		if bacon.mouse.left:
			window.bank = False
			window.cargo = False
			window.merchant = False
			window.destination = False
			window.refuel = True

	if x in range(
		cargo_range['x1'], cargo_range['x2']) and y in range(
		cargo_range['y1'], cargo_range['y2']):
		bacon.draw_image(cargo, 261, 485)
		if bacon.mouse.left:
			window.bank = False
			window.cargo = True
			window.merchant = False
			window.destination = False
			window.refuel = False

	if x in range(
		market_range['x1'], market_range['x2']) and y in range(
		market_range['y1'], market_range['y2']):
		bacon.draw_image(market, 359, 485)
		if bacon.mouse.left:
			window.bank = False
			window.cargo = False
			window.merchant = True
			window.destination = False
			window.refuel = False

	if x in range(
		money_range['x1'], money_range['x2']) and y in range(
		money_range['y1'], money_range['y2']):
		bacon.draw_image(money, 458, 485)	
		if bacon.mouse.left:
			window.bank = True
			window.cargo = False
			window.merchant = False
			window.destination = False
			window.refuel = False

	if x in range( 
		depart_range['x1'], depart_range['x2']) and y in range(
		depart_range['y1'], depart_range['y2']):
		bacon.draw_image(depart, 561, 485)	
		if bacon.mouse.left:
			window.bank = False
			window.cargo = False
			window.merchant = False
			window.destination = True
			window.refuel = False



myplayer.name = []

class Menu(bacon.Game):

	def on_tick(self):
		bacon.draw_image(title, 0, 0)
		bacon.push_color()

		bacon.set_color(0, 0, 0, 1 - round((abs(bacon.mouse.y-270.0)/540.0), 2))		
		bacon.draw_string(titlefont, 'ELEMENT', 70, 100)
		bacon.draw_string(titlefont, 'RUNNER', 250, 140)
		bacon.draw_string(byline, "a game by ben kulp", 150, 180)	
		bacon.draw_string(planet, "[ press space to begin ]", 130, bacon.window.height/2)	
		bacon.draw_string(planet, "[ hold 'h' for tutorial ]", 130, (bacon.window.height/2 - 30))
		bacon.pop_color()	
		if bacon.Keys.space in bacon.keys:
			bacon.run(Enter_name())
		if bacon.Keys.h in bacon.keys:
			bacon.draw_image(tutorial, 0, 0)	


class Enter_name(bacon.Game):
	def on_tick(self):
		bacon.draw_image(title, 0, 0)
		bacon.draw_string(planet, "[ Type your Name ]", 100, 430) 
		bacon.draw_string(planet, "[ press 'Enter' when done ]", 100, 450)
		n = 0
		for item in myplayer.name:
			bacon.draw_string(robot_speak, "%s" % myplayer.name[n], (240 + (10 * n)), 475)
			n += 1
		if bacon.Keys.enter in bacon.keys:
			myplayer.name = "".join(myplayer.name)
			bacon.run(Character_Builder())
	
	def	on_key(self, key, pressed):
		for keys in bacon.keys:
			if keys in range(96, 123):
				myplayer.name.append(bacon.Keys.tostring(keys))
			elif keys == 32:
				myplayer.name.append(" ")
			elif keys == 268:
				myplayer.name.pop(len(myplayer.name)-1)









class Character_Builder(bacon.Game):

	def on_tick(self):
		x, y = bacon.mouse.x, bacon.mouse.y
		oberon = [5000, 75, 40, 5] # set ship attributes
		intrepid = [6000, 225, 80, 2]
		excelsior = [4000, 100, 60, 2]
		firefly = [7000, 125, 80, 3]
		
		bacon.draw_image(title, 0, 0)
		bacon.draw_string(planet, "Select your starship", 240, 450)
		if x in range(
			(bacon.window.width * 0/4 + 20), 
			(bacon.window.width * 0/4 + 20 + ship1.width)) and y in range(
			300, (300 + ship1.height)):
			bacon.draw_image(triangle, (bacon.window.width * 0/4 + 42), 265)
			bacon.fill_rect(0, 125, 200, 265)
			bacon.push_color()
			bacon.set_color(0,0,0,1) #black
			bacon.draw_string(planet, "Class: Oberon", 10, 153)
			bacon.draw_string(planet, "Price: %d credits" % oberon[0], 10, 153 + line_height * 4)
			bacon.draw_string(planet, "Cargo Space: %d" % oberon[1], 10, 153 + line_height)
			bacon.draw_string(planet, "Weight: %d tons" % oberon[2], 10, 153 + line_height * 2)	
			bacon.draw_string(planet, "Max Velocity: %d" % oberon[3], 10, 153 + line_height * 3)		
			bacon.pop_color()
			if bacon.mouse.left:
				myplayer.ship = "Oberon"
				myplayer.money_in_pocket -= oberon[0]									
				myship.cost_to_buy = oberon[0]
				myship.hauling_capacity = oberon[1]
				myship.weight = oberon[2]
				myship.velocity = oberon[3]
				bacon.run(Game())
		bacon.draw_image(ship1, (bacon.window.width * 0/4 + 40), 300)

		if x in range(
			(bacon.window.width * 1/4 + 20), 
			(bacon.window.width * 1/4 + 20 + ship1.width)) and y in range(
			300, (300 + ship1.height)):
			bacon.draw_image(triangle, (bacon.window.width * 1/4 + 45), 265)
			bacon.fill_rect(135, 125, 335, 265)
			bacon.push_color()
			bacon.set_color(0,0,0,1) #black
			bacon.draw_string(planet, "Class: Intrepid", 145, 153)
			bacon.draw_string(planet, "Price: %d credits" % intrepid[0], 145, 153 + line_height * 4)
			bacon.draw_string(planet, "Cargo Space: %d" % intrepid[1], 145, 153 + line_height)
			bacon.draw_string(planet, "Weight: %d tons" % intrepid[2], 145, 153 + line_height * 2)	
			bacon.draw_string(planet, "Max Velocity: %d" % intrepid[3], 145, 153 + line_height * 3)		
			bacon.pop_color()			
			if bacon.mouse.left:
				myplayer.ship = "Intrepid"
				myplayer.money_in_pocket -= intrepid[0]								
				myship.cost_to_buy = intrepid[0]
				myship.hauling_capacity = intrepid[1]
				myship.weight = intrepid[2]
				myship.velocity = intrepid[3]
				bacon.run(Game())
		bacon.draw_image(ship2, (bacon.window.width * 1/4 + 40), 300)

		if x in range(
			(bacon.window.width * 2/4 + 20), 
			(bacon.window.width * 2/4 + 20 + ship1.width)) and y in range(
			300, (300 + ship1.height)):
			bacon.draw_image(triangle, (bacon.window.width * 2/4 + 29), 265)
			bacon.fill_rect(290, 125, 490, 265)
			bacon.push_color()
			bacon.set_color(0,0,0,1) #black
			bacon.draw_string(planet, "Class: Excelsior", 300, 153)
			bacon.draw_string(planet, "Price: %d credits" % excelsior[0], 300, 153 + line_height * 4)
			bacon.draw_string(planet, "Cargo Space: %d" % excelsior[1], 300, 153 + line_height)
			bacon.draw_string(planet, "Weight: %d tons" % excelsior[2], 300, 153 + line_height * 2)	
			bacon.draw_string(planet, "Max Velocity: %d" % excelsior[3], 300, 153 + line_height * 3)		
			bacon.pop_color()				
			if bacon.mouse.left:
				myplayer.ship = "Excelsior"
				myplayer.money_in_pocket -= excelsior[0]
				myship.cost_to_buy = excelsior[0]
				myship.hauling_capacity = excelsior[1]
				myship.weight = excelsior[2]
				myship.velocity = excelsior[3]
				bacon.run(Game())
		bacon.draw_image(ship3, (bacon.window.width * 2/4 + 30), 300)	

		if x in range(
			(bacon.window.width * 3/4 + 20), 
			(bacon.window.width * 3/4 + 20 + ship1.width)) and y in range(
			300, (300 + ship1.height)):
			bacon.draw_image(triangle, (bacon.window.width * 3/4 + 22), 265)
			bacon.fill_rect(440, 125, 640, 265)
			bacon.push_color()
			bacon.set_color(0,0,0,1) #black
			bacon.draw_string(planet, "Class: Firefly", 450, 153)
			bacon.draw_string(planet, "Price: %d credits" % firefly[0], 450, 153 + line_height * 4)
			bacon.draw_string(planet, "Cargo Space: %d" % firefly[1], 450, 153 + line_height)
			bacon.draw_string(planet, "Weight: %d tons" % firefly[2], 450, 153 + line_height * 2)	
			bacon.draw_string(planet, "Max Velocity: %d" % firefly[3], 450, 153 + line_height * 3)		
			bacon.pop_color()	
			if bacon.mouse.left:
				myplayer.ship = "Firefly"
				myplayer.money_in_pocket -= firefly[0]				
				myship.cost_to_buy = firefly[0]
				myship.hauling_capacity = firefly[1]
				myship.weight = firefly[2]
				myship.velocity = firefly[3]
				bacon.run(Game())
		bacon.draw_image(ship4, (bacon.window.width * 3/4 + 20), 300)


def refuel():
	x, y = bacon.mouse.x, bacon.mouse.y
	main_view()
	bacon.draw_image(battery, 189, 485)
	
	bacon.draw_image(triangle, 173, 450) #point triangle at icon
	bacon.fill_rect(95, 375, 268, 450) # create white dialogue box
	bacon.push_color()
	bacon.set_color(0, 0, 0, 1)
	bacon.draw_string(planet, "Refuel cost: %d " % abs((100 - myship.fuel) * fuel_cost), 105, 402)

	bacon.draw_rect(102, 408, 140, 444) #yes rectangle
	if x in range(102, 140) and y in range(408, 444): #yes box hover color
		bacon.push_color()
		bacon.set_color(.2, .58, .03, 1) #green
		bacon.fill_rect(103, 409, 139, 443)
		bacon.pop_color()

	bacon.draw_rect(230, 408, 260, 444) #no box
	if x in range(230, 260) and y in range(408, 444): #no box hover color
		bacon.push_color()
		bacon.set_color(.74, .07, .07, 1) # red
		bacon.fill_rect(231, 409, 259, 443)
		bacon.pop_color()

	bacon.draw_string(planet, "Yes              No", 106, 438)
	bacon.pop_color()
	core_action()	







class Game(bacon.Game):
	def on_tick(self):
		#global banking_window
		x, y = bacon.mouse.x, bacon.mouse.y
		main_view() # build the main page elements 
		core_action() # build the hover colors for screen icons
		
		# if window is active, run function to display it
		if window.bank:
			banking() 
		if window.cargo:
			cargo_view()
		if window.merchant:
			merchant_view()
		if window.destination:
			depart_view()
		if window.refuel:
			refuel()

		if window.bank == True or window.cargo == True or window.merchant ==True:
			pass
		else:	
			for item in planet_list: # on mouse hover over planet  usage
				if x in range(item[1], item[1] + 12) and y in range(item[2], item[2] + 12):
					distance_and_fuel(myplayer.location_x, myplayer.location_y, item[1], item[2])
					
					bacon.push_color() # place pin
					bacon.set_color(.74, .07, .07, 1) # red
					bacon.draw_image(target, item[1] - 7, item[2] - 20)
					bacon.pop_color()
					
					bacon.push_color() # set fuel usage in red on gauge
					gauge_level = (179 * (myplayer.fuel_used/100.0))
					if gauge_level == 0:
						gauge_level = 14
					bacon.set_color(.74, .07, .07, 1) # red
					bacon.fill_rect(14, 496, (gauge_level), 530) 
					bacon.pop_color()

					bacon.push_color()
					bacon.set_color(0, 0, 0, 1)
					gauge_level = (179 * (myplayer.fuel_used/100.0))
					if gauge_level == 0:
						gauge_level = 14
					if myplayer.fuel_used > myship.fuel:
						bacon.draw_string(planet, "need more fuel", 16, 522)
					else:	
						bacon.draw_string(planet, "fuel used: %r " % myplayer.fuel_used, 16, 522)
					bacon.pop_color()
		if bacon.Keys.space in bacon.keys or bacon.mouse.left:

			if window.merchant:
				for i, item in enumerate(myship.current_cargo, 1): # process selling element
					if x in range(220, 265) and y in range(
						(160 + (line_height * i)), (160 + line_height + line_height * i)):
						if item[2] == 0:
							self.current_cargo.remove(item)
							pass
						elif myship.remove_cargo(item[0]):
							
							myplayer.money_in_pocket += transfer_element_to_market(item[0])

	
				for i, item in enumerate(element_pricelist, 1): # process buying element
					if x in range(300, 345) and y in range(
						(160 + (line_height * i)), (160 + line_height + line_height * i)):
						if item[2] == 0:
							pass 
						elif myship.add_cargo(item[0], item[1]):
							myplayer.remove_money_from_pocket(item[1])
							item[2] -= 1
							if myplayer.money_in_pocket < 0:
								myplayer.money_in_bank += myplayer.money_in_pocket
								myplayer.money_in_pocket = 0

			if window.bank: 		
				if x in range(515, 617) and y in range(412, 442) and myplayer.money_in_bank > 1000: 
					myplayer.money_in_bank -= 1000
					myplayer.money_in_pocket += 1000
				elif x in range(515, 617) and y in range(378, 406) and myplayer.money_in_pocket > 1000:
					myplayer.money_in_bank += 1000
					myplayer.money_in_pocket -= 1000


	def on_mouse_button(self, button, pressed):
		x, y = bacon.mouse.x, bacon.mouse.y 

		if window.bank: #money goest into/out of bank in 1000 increments for speed/simplicity		
			if x in range(515, 617) and y in range(412, 442) and myplayer.money_in_bank > 1000: 
				myplayer.money_in_bank -= 1000 
				myplayer.money_in_pocket += 1000
			elif x in range(515, 617) and y in range(378, 406) and myplayer.money_in_pocket > 1000:
				myplayer.money_in_bank += 1000
				myplayer.money_in_pocket -= 1000
		if window.destination:
			for item in planet_list: # on mouse hover over planet
				if x in range(item[1], item[1] + 12) and y in range(item[2], item[2] + 12):
					distance_and_fuel(myplayer.location_x, myplayer.location_y, item[1], item[2])
					
					bacon.push_color() # place pin
					bacon.set_color(.74, .07, .07, 1) # red
					bacon.draw_image(target, item[1] - 7, item[2] - 20)
					bacon.pop_color()
					
					bacon.push_color() # set fuel usage in red on gauge
					gauge_level = (179 * (myplayer.fuel_used/100.0))
					if gauge_level == 0:
						gauge_level = 14
					bacon.set_color(.74, .07, .07, 1) # red
					bacon.fill_rect(14, 496, (gauge_level), 530) 
					bacon.pop_color()

					bacon.push_color()
					bacon.set_color(0, 0, 0, 1)

					if myplayer.fuel_used > myship.fuel:
						bacon.draw_string(planet, "need more fuel", 16, 522)
					else:	
						bacon.draw_string(planet, "fuel used: %r " % myplayer.fuel_used, 16, 522)
					bacon.pop_color()

					myplayer.destination = copy.copy(item[0])
					myplayer.destination_x = copy.copy(item[1])
					myplayer.destination_y = copy.copy(item[2])
					bacon.draw_image(depart, 561, 485)	

		if myplayer.destination: # set up next turn properties			
			if myplayer.destination_x == myplayer.location_x and myplayer.destination_y == myplayer.location_y:
				return False
			elif x in range( 
			depart_range['x1'], depart_range['x2']) and y in range(
			depart_range['y1'], depart_range['y2']):
				myplayer.location_x = copy.copy(myplayer.destination_x) # move player to destination
				myplayer.location_y = copy.copy(myplayer.destination_y)
				myplayer.turn += 1 # advance turn
				myship.fuel -= myplayer.fuel_used # remove fuel from flight
				myplayer.destination_x = None # return destination variables to none
				myplayer.destination_y = None
				myplayer.destination = None
				if myplayer.money_in_bank < 0:
					myplayer.money_in_bank += (myplayer.money_in_bank * .15) # calc bank loan interest
				else:		 
					myplayer.money_in_bank += (myplayer.money_in_bank * .05) # calc bank interest
				price_refresh()# recalculate price index and quantities
				if myplayer.turn > 10:
					bacon.run(Game_Over())


				
		if window.refuel:
			if x in range(230, 260) and y in range(408, 444): # no refill
				window.refuel = False
			if x in range(102, 140) and y in range(408, 444): # yes refill
				refill_tank()
				window.refuel = False


class Game_Over(bacon.Game):
	def on_tick(self):
		bacon.draw_image(title, 0, 0)
		bacon.push_color()
		bacon.set_color(0, 0, 0, 1 - round((abs(bacon.mouse.y-270.0)/540.0), 2))		
		bacon.draw_string(titlefont, 'ELEMENT', 70, 100)
		bacon.draw_string(titlefont, 'RUNNER', 250, 140)
		bacon.draw_string(byline, "Game Over", 150, 180)
		bacon.draw_string(planet, "Final Score: %d" % myplayer.money_in_bank, 150, 210)
		bacon.draw_string(planet, "[ press 'space' to start a new game ]", 150, 235)
		bacon.draw_string(planet, "[ High Scores ]", 150, 280)
		if myplayer.turn > 10:
			high_score.append([int(myplayer.money_in_bank + myplayer.money_in_pocket), myplayer.name])
			high_score.sort(key=None, reverse=True)
			myplayer.turn = 10
		for i, item in enumerate(high_score):
			bacon.draw_string(planet, "%s   " % high_score[i][1], 150, (315 + line_height * i))
			bacon.draw_string(planet, "      ........       ", 150 + len(high_score[i][1]), (315 + line_height * i))
			bacon.draw_string(planet, "%d" %  high_score[i][0], 300, (315 + line_height * i))

		bacon.pop_color()	
		if bacon.Keys.space in bacon.keys:
			myplayer.character_cleaner()
			myship.ship_cleaner()
			bacon.run(Enter_name())


		

	




bacon.run(Menu())

