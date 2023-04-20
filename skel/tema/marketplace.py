from threading import Lock, currentThread

class Marketplace:
	def __init__(self, queue_size_per_producer):
		self.queue_size_per_producer = queue_size_per_producer
		self.producer_id_count = -1 # will add to it in the future
		self.carts_id_count = -1 # will add to it in the future
		self.producers = {} # dictionary, key = producer_id, value = list of products for the producer_id
		self.carts = {} # key: cart_id, value: list of products of the cart
		self.lock = Lock()

	def register_producer(self):
		with self.lock:
			self.producer_id_count += 1
			self.producers[self.producer_id_count] = [] # initialize
			return self.producer_id_count

	def publish(self, producer_id, product):
		prod_id = int(producer_id)
		if len(self.producers[prod_id]) == self.queue_size_per_producer :
			return False
		
		self.producers[prod_id].append(product)
		return True

	def new_cart(self):
		with self.lock:
			self.carts_id_count += 1
			self.carts[self.carts_id_count] = [] # initialize
			return self.carts_id_count

	def add_to_cart(self, cart_id, product):
		carts_id = int(cart_id)

		with self.lock:
			for producer in self.producers:
				if product in self.producers[producer]:
					self.carts[carts_id].append((product, producer))
					self.producers[producer].remove(product)
					return True
			return False

	def remove_from_cart(self, cart_id, product):
		with self.lock:
			for pair in self.carts[int(cart_id)]:
				if pair[0] == product:
					self.carts[int(cart_id)].remove(pair)
					self.producers[pair[1]].append(product)
					return

	def place_order(self, cart_id):
		order = []
		for pair in self.carts[int(cart_id)]:
			with self.lock:
				print("{} bought {}".format(currentThread().getName(), pair[0]))
			order.append(pair[0])
		return order
