import string
import random

class GeneratorCodes():
    def __init__(self, _size):
        self.size = _size

    def generator(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(self.size))

