import random


class GeneralHelper(object):
    @staticmethod
    def random_image():
        images = [line.rstrip('\n') for line in open('files/images_property.txt')]
        return random.choice(images)

    @staticmethod
    def get_mortgage(price):
        return round(price / 180)
