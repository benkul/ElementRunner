
class Ship(object):
	def __init__(self, name, velocity, weight, hauling_capacity, 
			cargo_space=None, current_cargo=None, fuel=100, cost_to_buy=None, value=None):
		self.name = name
		self.velocity = velocity
		self.weight = weight
		self.hauling_capacity = hauling_capacity # total hauling capacity
		self.cargo_space = self.cargo_load_calculator # how much space is left in hold.
		self.current_cargo = []
		self.cost_to_buy = None
		self.value = None
	
	def ship_cleaner(self):
		self.current_cargo = []
		self.fuel = 100

	def add_cargo(self, product, cost): # add defined product to hold
		if len(self.current_cargo) == 0:
			self.current_cargo.append([product, cost, 1])
			return True
		elif self.cargo_load_calculator() == 0:
			return False	
		else:
			for item in self.current_cargo:
				if item[0].find(product) != -1:
					item[2] += 1
					return True
				else:
					pass
		self.current_cargo.append([product, cost, 1])
		return True	

	def cargo_load_calculator(self): # calculate space in hold
		x = 0 
		for item in self.current_cargo:
			x += int(item[2])
		self.cargo_space = self.hauling_capacity - x
		return self.cargo_space

	def remove_cargo(self, product): # need ability to not remove more than amount available.
		for item in self.current_cargo:
			if item[0].find(product) != -1:
				if item[2] == 0:
					self.current_cargo.remove(item)
					return False
				elif item[2] == 1:
					item[2] -= 1
					self.current_cargo.remove(item)
					return True
				else:
					item[2]	-= 1
					return True



	def __str__(self):
		return self.name, self.fuel, self.current_cargo
	




#need function for removing fuel and refueling



