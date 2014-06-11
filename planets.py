
planet_list = [
["Gestea", 213, 196],
["Skenus", 70, 210],
["Pregantu", 237, 119],
["Ocraco", 370, 132],
["Bleutis", 181, 286],
["Ofthara", 286, 221],
["Sworia", 286, 369],
["Ostbomia", 440, 347],
["Hulara", 551, 292],
["Mulia", 551, 419]
]


class Planet(object):
	def __init__(self, name, locx, locy, merchant_photo):
		self.name = name
		self.locx = locx
		self.locy = locy
		self.merchant_photo = merchant_photo



	"""def transfer_element_to_market(self, product): # add product to market, return amount paid for it
		for item in element_pricelist:
			if item[0].find(product) != -1:
				item[2] += 1
				return item[1]"""






