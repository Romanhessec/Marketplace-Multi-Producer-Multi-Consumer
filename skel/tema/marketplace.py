"""Thread/unittest/logging modules"""
from threading import Lock, currentThread
from logging.handlers import RotatingFileHandler
import unittest
import logging

class Marketplace:
    """
    Class that represents the Marketplace in the MPMC program, a mediator between
    producers and consumers.
    """
    def __init__(self, queue_size_per_producer):
        """
        Initialize variables + logger information.
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_id_count = -1 # will add to it in the future
        self.carts_id_count = -1 # will add to it in the future
        self.producers = {} # (producer_id, product list for the producer_id)
        self.carts = {} # (cart_id, list of products of the cart)
        self.lock = Lock()
        self.logger = logging.getLogger('Logger Marketplace')
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler('marketplace.log', maxBytes=25000, backupCount=3)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def register_producer(self):
        """
        Register a producer in the database with its own id.
        """
        with self.lock:
            self.producer_id_count += 1
            self.producers[self.producer_id_count] = [] # initialize
            self.logger.info('Registered new producer with id %s', str(self.producer_id_count))
            return self.producer_id_count

    def publish(self, producer_id, product):
        """
        Publish a producer's item on the market if the number of item's produced
        isn't bigger than the queue size.
        """
        if len(self.producers[int(producer_id)]) == self.queue_size_per_producer:
            self.logger.error('Producer %s couldnt place %s on the market - max queue size', producer_id, product)
            return False
        self.producers[int(producer_id)].append(product)
        self.logger.info('Producer %s placed on the market %s', producer_id, product)
        return True

    def new_cart(self):
        """
        Regiser a new cart in the database with its own id.
        """
        with self.lock:
            self.carts_id_count += 1
            self.carts[self.carts_id_count] = [] # initialize
            self.logger.info('Registered new cart with id %s', str(self.carts_id_count))
            return self.carts_id_count

    def add_to_cart(self, cart_id, product):
        """
        Add an item to a cart if the item is produced already (it is on a queue
        of one of the producers).
        """
        with self.lock:
            for producer in self.producers:
                if product in self.producers[producer]:
                    self.carts[int(cart_id)].append((product, producer))
                    self.producers[producer].remove(product)
                    self.logger.info('Added product %s to the cart %s', product, cart_id)
                    return True
            self.logger.error('Couldnt add product %s to the cart %s - didnt find product', product, cart_id)
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes an item from a cart (if the item exists in the cart)
        """
        with self.lock:
            for pair in self.carts[int(cart_id)]:
                if pair[0] == product:
                    self.carts[int(cart_id)].remove(pair)
                    self.producers[pair[1]].append(product)
                    self.logger.info('Removed product %s from the cart %s', product, cart_id)
                    return
            self.logger.error('Couldnt remove item %s from cart %s - didnt find item', product, cart_id)

    def place_order(self, cart_id):
        """
        Places an order from a cart with a specific id.
        """
        order = []
        for pair in self.carts[int(cart_id)]:
            with self.lock:
                print("{} bought {}".format(currentThread().getName(), pair[0]))
            order.append(pair[0])
        self.logger.info('Placed order from the cart %s', cart_id)
        return order

class TestMarketplace(unittest.TestCase):
    """
    Class that represents the Marketplace test class, made for unittesting
    the marketplace class.
    """
    def setUp(self):
        self.marketplace = Marketplace(3) # queue size 3 for easier testing

    def test_register_producer(self):
        """
        First producer should have id 0
        """
        self.assertEqual(self.marketplace.register_producer(), 0)

    def test_publish_true(self):
        """
        The producer should be able to register a product.
        """
        producer_id = self.marketplace.register_producer()
        self.assertTrue(self.marketplace.publish(producer_id, "tea"))

    def test_publish_false(self):
        """
        The producer should be able to register only 3 products, not 4
        because the queue size for the marketplace is 3.
        """
        producer_id = self.marketplace.register_producer()
        self.assertTrue(self.marketplace.publish(producer_id, "tea1"))
        self.assertTrue(self.marketplace.publish(producer_id, "tea2"))
        self.assertTrue(self.marketplace.publish(producer_id, "coffee1"))
        self.assertFalse(self.marketplace.publish(producer_id, "coffee2"))

    def test_new_cart(self):
        """
        First cart id should be 0
        """
        self.assertEqual(self.marketplace.new_cart(), 0)

    def test_add_to_cart_true(self):
        """
        The cart should be able to register the 'tea' product.
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, "tea")
        self.assertTrue(self.marketplace.add_to_cart(self.marketplace.new_cart(), "tea"))

    def test_add_to_cart_fail(self):
        """
        The cart shouldn't be able to register a product that wasn't produced
        beforehand.
        """
        self.assertFalse(self.marketplace.add_to_cart(self.marketplace.new_cart(), "tea"))

    def test_remove_from_cart(self):
        """
        Tests successively remove_from_cart function with 2 items, tea and coffee.
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, "tea")
        self.marketplace.publish(producer_id, "coffee")
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, "tea")
        self.assertEqual(self.marketplace.carts[cart_id], [("tea", 0)])
        self.marketplace.remove_from_cart(cart_id, "tea")
        self.assertEqual(self.marketplace.carts[cart_id], [])

    def test_place_order(self):
        """
        Tests place_order function with 2 items, tea and coffee.
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, "tea")
        self.marketplace.publish(producer_id, "coffee")
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, "tea")
        self.marketplace.add_to_cart(cart_id, "coffee")
        order = self.marketplace.place_order(cart_id)
        self.assertEqual(order, ["tea", "coffee"])
    