"""Thread/time modules"""
from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents the Consumer in the MPMC program.
    """
    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            for request in cart:
                if request["type"] == "add":
                    for _ in range(request["quantity"]):
                        while not self.marketplace.add_to_cart(cart_id, request["product"]):
                            time.sleep(self.retry_wait_time)
                elif request["type"] == "remove":
                    for _ in range(request["quantity"]):
                        self.marketplace.remove_from_cart(cart_id, request["product"])

            self.marketplace.place_order(cart_id)
