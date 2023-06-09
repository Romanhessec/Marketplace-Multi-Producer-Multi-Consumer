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
            cart_id = int(self.marketplace.new_cart())

            for tuple in cart:
                if tuple["type"] == "add":
                    for i in range(tuple["quantity"]):
                        # check if we can add to cart or not (check marketplace)
                        while True:
                            added_or_not = self.marketplace.add_to_cart(str(cart_id), tuple["product"])
                            if added_or_not:
                                break
                            time.sleep(self.retry_wait_time)
                else:
                    for i in range(tuple["quantity"]):
                        # no need to check if it worked or not, the result will be logged
                        self.marketplace.remove_from_cart(str(cart_id), tuple["product"])

            self.marketplace.place_order(str(cart_id))
