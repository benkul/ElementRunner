import bacon
import copy
from random import randrange
from random import choice
from math import atan
from math import pi
from ship import Ship
from player import Player
from planets import planet_list, Planet # contains list of planets for game
from elements import element_list # contains list of element commodities for game

element_pricelist = []
for item in element_list:
	element_pricelist.append([item, randrange(100, 200), randrange(10, 50)])




class game_function(object):
	def __init__(self, refuel = False, bank = False, cargo = False, merchant = False, destination = False):
		self.refuel = refuel
		self.bank = bank
		self.cargo = cargo
		self.merchant = merchant
		self.destination = destination

window = game_function()

title = bacon.Image('Galaxy.jpg')
fuel_cost = 21
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
merch_list = [merch1, merch2, merch3, merch4, merch5, merch6, merch7, merch8, merch9, merch10]



titlefont = bacon.Font('moonhouse.ttf', 40)
byline = bacon.Font('moonhouse.ttf', 20)
planet = bacon.Font('FINALOLD.ttf', 20)
robot_speak = bacon.Font('LCD_Solid.ttf', 14)
ship = bacon.Image('ship3.png')
music = bacon.Sound('farewell.ogg', stream=True)

battery_range = {'x1': 183, 'x2': 233, 'y1': 486, 'y2': 540}
cargo_range = {'x1': 267, 'x2': 339, 'y1': 486, 'y2': 540}
market_range = {'x1': 363, 'x2': 486, 'y1': 486, 'y2': 540}
money_range = {'x1': 460, 'x2': 540, 'y1': 486, 'y2': 540}
depart_range = {'x1': 555, 'x2': 630, 'y1': 486, 'y2': 540}

planet_master = []

for item in planet_list: #create master planet list 
	planet_master.append(Planet(item[0], item[1], item[2], merch_list.pop(0)))

myplayer = Player("Hobart Killjoy", "defiant", 100003298, 0, 213, 196)
myship = Ship("Defiant", 10, 10000, 400)
myship.fuel = 90
line_height = 25 # for planet font


music_voice = bacon.Voice(music, loop=True)
#music_voice.play()

x = 360 #inital player start position
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
	bacon.draw_image(planet_master[0].merchant_photo, 350, 65) #draw planet merchant
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
		# fill rectangle on hover
		# but text for rectangle
	n = 0
	for item in myship.current_cargo: # draw sell buttons for cargo
		n += 1
		bacon.draw_rect(
		220, (160 + (line_height * n)), 
		265, (160 + line_height + line_height * n)) # draw rectange

		if x in range(220, 265) and y in range((160 + (line_height * n)), (160 + line_height + line_height * n)):
			bacon.push_color # fill rectangle on hover
			bacon.set_color(.20, .58, .03, 1) # green
			bacon.fill_rect(		
			221, (161 + (line_height * n)), 
			264, (159 + line_height + line_height * n)) 
			bacon.pop_color()
		bacon.draw_string(planet, "sell", 226, (180 + (line_height * n)))# sell text for rectangle	
	
	n = 0
	for item in element_pricelist: # draw buy buttons for merchant
		n += 1
		bacon.draw_rect(
		300, (160 + (line_height * n)), 
		345, (160 + line_height + line_height * n)) # draw rectange

		if x in range(300, 345) and y in range((160 + (line_height * n)), (160 + line_height + line_height * n)):
			bacon.push_color # fill rectangle on hover
			bacon.set_color(.20, .58, .03, 1)  # red
			bacon.fill_rect(		
			301, (161 + (line_height * n)), 
			344, (159 + line_height + line_height * n)) 
			bacon.pop_color()
		bacon.draw_string(planet, "buy", 308, (180 + (line_height * n)))# buy text for rectangle	
	bacon.pop_color()

def distance_and_fuel(x1, y1, x2, y2):
	myplayer.distance = int((
	(x1 - x2) ** 2 + 
	(y1 - y2) ** 2 ) **(.5))
	myplayer.fuel_used = int((myplayer.distance/525.0) * 100)
	myplayer.distance /= 85
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
	bacon.draw_image(star, planet_list[0][1] - 8, planet_list[0][2] - 6)
	bacon.pop_color()	

	bacon.push_color()
	bacon.set_color(0,0,0,.2)
	bacon.fill_rect(0, 0, 640, 40) #HUD top bar
	bacon.set_color(1,1,1,1)
	bacon.draw_string(planet, "%s    cash: %d    bank: %d    turn: %d" % (
		myplayer.name, myplayer.money_in_pocket, myplayer.money_in_bank, myplayer.turn), 20, 30)
	bacon.pop_color()


def core_action():
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




class Menu(bacon.Game):

	def on_tick(self):
		bacon.draw_image(title, 0, 0)
		bacon.push_color()

		bacon.set_color(0, 0, 0, 1 - round((abs(bacon.mouse.y-270.0)/540.0), 2))		
		bacon.draw_string(titlefont, 'ELEMENT', 70, 100)
		bacon.draw_string(titlefont, 'RUNNER', 250, 140)
		bacon.draw_string(byline, "a game by ben kulp", 150, 180)	
		bacon.draw_string(planet, '[ press enter to begin ]', 130, bacon.window.height/2)	
		bacon.draw_string(planet, '[ press h for tutorial ]', 130, (bacon.window.height/2 - 30))
		bacon.pop_color()	
		if bacon.Keys.enter in bacon.keys:
			bacon.run(Game())	

	def on_key(self, key, pressed):
		print bacon.Keys.tostring(key)




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
		global banking_window
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
			print "destination"
		if window.refuel:
			refuel()

		if window.bank == True or window.cargo == True or window.merchant ==True:
			pass
		else:	
			for item in planet_list: # on mouse hover over planet  usage
				if x in range(item[1], item[1] + 12) and y in range(item[2], item[2] + 12):
					distance_and_fuel(planet_list[1][1], planet_list[1][2], item[1], item[2])
					
					bacon.push_color() # place pin
					bacon.set_color(.74, .07, .07, 1) # red
					bacon.draw_image(target, item[1] - 7, item[2] - 20)
					bacon.pop_color()
					
					bacon.push_color() # set fuel usage in red on gauge
					bacon.set_color(.74, .07, .07, 1) # red
					bacon.fill_rect(14, 496, (179 * (myplayer.fuel_used/100.0)), 530) 
					bacon.pop_color()

					bacon.push_color()
					bacon.set_color(0, 0, 0, 1)

					if myplayer.fuel_used > myship.fuel:
						bacon.draw_string(planet, "need more fuel", 16, 522)
					else:	
						bacon.draw_string(planet, "fuel used: %r " % myplayer.fuel_used, 16, 522)
					bacon.pop_color()

	def on_mouse_button(self, button, pressed):
		x, y = bacon.mouse.x, bacon.mouse.y

		if window.bank: 		
			if x in range(515, 617) and y in range(412, 442) and myplayer.money_in_bank > 100: 
				myplayer.money_in_bank -= 100
				myplayer.money_in_pocket += 100
			elif x in range(515, 617) and y in range(378, 406) and myplayer.money_in_pocket > 100:
				myplayer.money_in_bank += 100
				myplayer.money_in_pocket -= 100
		if window.refuel:
			if x in range(230, 260) and y in range(408, 444): # no refill
				window.refuel = False
			if x in range(102, 140) and y in range(408, 444): # yes refill
				refill_tank()
				window.refuel = False
		if window.merchant:
			n = 0
			for item in myship.current_cargo: # process selling element
				n += 1
				if x in range(220, 265) and y in range(
					(160 + (line_height * n)), (160 + line_height + line_height * n)):
					if item[2] == 0:
						self.current_cargo.remove(item)
						pass
					elif myship.remove_cargo(item[0]):
						
						myplayer.money_in_pocket += transfer_element_to_market(item[0])

			n = 0		
			for item in element_pricelist: # process buying element
				n += 1
				if x in range(300, 345) and y in range(
					(160 + (line_height * n)), (160 + line_height + line_height * n)):
					if item[2] == 0:
						pass 
					elif myship.add_cargo(item[0], item[1]):
						myplayer.remove_money_from_pocket(item[1])
						item[2] -= 1


		bacon.run(Game())

	




bacon.run(Menu())

