import bacon
import copy
bacon.window.title = 'Elemental'
bacon.window.width = 640
bacon.window.height = 540
bacon.window.fullscreen = False

background = bacon.Image('Galaxy.jpg')
ship = bacon.Image('ship3.png')
accship = bacon.Image('ship3mov.png')
enemy1 = bacon.Image('redship2.png')
enemy2 = bacon.Image('ship2.png') 
titlefont = bacon.Font('moonhouse.ttf', 40)
text = bacon.Font('FINALOLD.ttf', 15)
playerproj = bacon.Image('shot3.png')

location = (bacon.window.width / 2 - 31)
ylocation =(bacon.window.width / 2 + 100)
stamp = 0





class Menu(bacon.Game):


	def on_tick(self):

		bacon.draw_image(background, 0, 0)
		bacon.draw_string(titlefont, "Elemental", 175, bacon.window.height / 2)
		bacon.push_color()
		bacon.set_color(0, 0, 0, 1)
		bacon.draw_rect(
			bacon.window.width / 2 - 80, bacon.window.height / 2 + 10, 
			bacon.window.width / 2 + 80, bacon.window.height / 2 + 45)
		bacon.pop_color()
		bacon.push_color()
		bacon.set_color(0, 0, 0, .5)
		bacon.fill_rect(
			bacon.window.width / 2 - 80, bacon.window.height / 2 + 10, 
			bacon.window.width / 2 + 80, bacon.window.height / 2 + 45)
		bacon.pop_color()
		bacon.push_color()
		bacon.set_color(1, 1, 1, .2)
		bacon.draw_string(text, "press enter to begin", 
			bacon.window.width/2 - 70, bacon.window.height / 2 + 35)		
		bacon.pop_color()
		if bacon.Keys.enter in bacon.keys:
			bacon.run(Game())

xvelocity = 0

v = .5 #global velocity effect 
v2 = 1 #global displacement 




class Game(bacon.Game):
	def on_tick(self):
		bacon.draw_image(background, 0, 0)
		global stamp
		stamp += 1
		global xvelocity
		global location
		global loationy
		# enforce game window boundaries
		if location > bacon.window.width - ship.width:
			location = bacon.window.width - ship.width
			xvelocity -= v #slow ship when it hits boundary
		elif location < 0:
			xvelocity += v
			location = 0

		bacon.draw_image(accship, location, ylocation)
		location += xvelocity




		x, y = bacon.mouse.x, bacon.mouse.y

		if bacon.Keys.right in bacon.keys or bacon.Keys.d in bacon.keys:
			location += v2
			xvelocity += v


		if bacon.Keys.left in bacon.keys or bacon.Keys.a in bacon.keys:
			location -= v2
			xvelocity -= v			


		#if bacon.Keys.up in bacon.keys or bacon.Keys.w in bacon.keys:

		

		
		bacon.push_color()
		bacon.set_color(0,0,0,.2)
		bacon.fill_rect(0, 0, 640, 40) #HUD top bar
		bacon.pop_color()

		bacon.push_color()
		bacon.set_color(1,1,1,1)
		bacon.draw_string(text, "Score: ", 20, 26) # enter player score variable here
		bacon.draw_string(text, "Health", 350, 26) 
		bacon.pop_color()

		bacon.push_color()
		bacon.set_color(0, 0, 0, 1)
		bacon.fill_rect(400, 10, 620, 30)
		bacon.pop_color()

		bacon.push_color()
		bacon.set_color(.2, .6, .05, 1) # green health bar
		bacon.fill_rect(401, 11, 619, 29) # needs percentage change for HP damage end bar need variable coordinate
		bacon.pop_color()

		bacon.push_color()
		bacon.set_color(.7, .07, .07, 1) # red for damage drop 
		#bacon.fill_rect( )coordinates based on variables for damage done
		bacon.pop_color()


bacon.run(Menu())
