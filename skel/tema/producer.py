"""Thread/time modules"""
import time
from threading import Thread

class Producer(Thread):
    """
    Class that represents the Producer in the MPMC program.
    """
    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.this_producer_id = self.marketplace.register_producer()

    def run(self):
        while True:
            for tuple in self.products: # tuple = (product, nr_product, wait_time)
                for i in range(0, tuple[1]):
                    if self.marketplace.publish(str(self.this_producer_id), tuple[0]):
                        # marketplace is available
                        time.sleep(tuple[2])
                    else:
                        # marketplace is not available, stay on the same loop iteration
                        time.sleep(self.republish_wait_time)
                        i -= 1
