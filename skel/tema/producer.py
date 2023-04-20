
import time
from threading import Thread

class Producer(Thread):
    
    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.id = self.marketplace.register_producer()

    def run(self):
        while True:
            for (product, num_product, wait_time_product) in self.products:
                for i in range(0, num_product):
                    if self.marketplace.publish(str(self.id), product):
                        # marketplace is available
                        time.sleep(wait_time_product)
                    else:
                        # marketplace is not available, stay on the same loop iteration
                        time.sleep(self.republish_wait_time)
                        i-=1
