class Player(object):
	def __init__(self, name, ship, money_in_pocket, money_in_bank, location_x, location_y, 
		from_where=None, fuel_used=None, distance=None, turn=0, 
		destination=None, destination_x=None, destination_y=None):
		self.name = name
		self.ship = ship
		self.money_in_pocket = money_in_pocket
		self.money_in_bank = money_in_bank
		self.location_x = location_x
		self.location_y = location_y
		self.from_where = None
		self.fuel_used = None
		self.distance = None
		self.turn = 0
		self.destination = None
		self.destination_x = None
		self.destination_y = None
	
	def remove_money_from_pocket(self, amount):
		self.money_in_pocket -= amount

	def remove_money_from_bank(self, amount):
		self.money_in_bank -= amount 
	
	def character_cleaner(self):
		self.ship = None
		self.money_in_pocket = 10000
		self.money_in_bank = 0
		self.location_x = 213
		self.location_y = 196
		self.turn = 0








