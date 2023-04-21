"""Thread/unittest modules"""
from threading import Lock, currentThread
import unittest

class Marketplace:
    """
    Class that represents the Marketplace in the MPMC program, a mediator between
    producers and consumers.
    """
    def __init__(self, queue_size_per_producer):
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_id_count = -1 # will add to it in the future
        self.carts_id_count = -1 # will add to it in the future
        self.producers = {} # key = producer_id, value = product list for the producer_id
        self.carts = {} # key: cart_id, value: list of products of the cart
        self.lock = Lock()

    def register_producer(self):
        with self.lock:
            self.producer_id_count += 1
            self.producers[self.producer_id_count] = [] # initialize
            return self.producer_id_count

    def publish(self, producer_id, product):
        prod_id = int(producer_id)
        if len(self.producers[prod_id]) == self.queue_size_per_producer:
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
    