"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock

class Marketplace:
	"""
	Class that represents the Marketplace. It's the central part of the implementation.
	The producers and consumers use its methods concurrently.
	"""
	def __init__(self, queue_size_per_producer):
		"""
		Constructor

		:type queue_size_per_producer: Int
		:param queue_size_per_producer: the maximum size of a queue associated with each producer
		"""
		self.queue_size_per_producer = queue_size_per_producer
		self.producer_id_count = -1 # will add to it in the future
		self.carts_id_count = -1 # will add to it in the future
		self.producers = {} # dictionary, key = producer_id, value = list of products for the producer_id
		self.carts = {} # key: cart_id, value: list of products of the cart
		self.lock = Lock()

	def register_producer(self):
		"""
		Returns an id for the producer that calls this.
		"""
		with self.lock:
			self.producer_id_count += 1
			self.producers[self.producer_id_count] = [] # initialize
			return self.producer_id_count

	def publish(self, producer_id, product):
		"""
		Adds the product provided by the producer to the marketplace

		:type producer_id: String
		:param producer_id: producer id

		:type product: Product
		:param product: the Product that will be published in the Marketplace

		:returns True or False. If the caller receives False, it should wait and then try again.
		"""
		prod_id = int(producer_id)
		if len(self.producers[prod_id]) == self.queue_size_per_producer :
			return False
		
		self.producers[prod_id].append(product)
		return True

	def new_cart(self):
		"""
		Creates a new cart for the consumer

		:returns an int representing the cart_id
		"""
		with self.lock:
			self.carts_id_count += 1
			self.carts[self.carts_id_count] = [] # initialize
			return self.carts_id_count

	def add_to_cart(self, cart_id, product):
		"""
		Adds a product to the given cart. The method returns

		:type cart_id: Int
		:param cart_id: id cart

		:type product: Product
		:param product: the product to add to cart

		:returns True or False. If the caller receives False, it should wait and then try again
		"""
		carts_id = int(cart_id)

		with self.lock:
			for producer in self.producers:
				if product in self.producers[producer]:
					self.carts[carts_id].append((product, producer))
					self.producers[producer].remove(product)
					return True
			return False

	def remove_from_cart(self, cart_id, product):
		"""
		Removes a product from cart.

		:type cart_id: Int
		:param cart_id: id cart

		:type product: Product
		:param product: the product to remove from cart
		"""		
		for pair in self.carts[int(cart_id)]:
			if pair[0] == product:
				self.carts[int(cart_id)].remove(pair)
				self.producers[pair[1]].append(product)
				return

	def place_order(self, cart_id):
		"""
		Return a list with all the products in the cart.

		:type cart_id: Int
		:param cart_id: id cart
		"""
		order = []
		for pair in self.carts[int(cart_id)]:
			order.append(pair[0])
		return order
