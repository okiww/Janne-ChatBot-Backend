import random


class GeneralHelper(object):
    @staticmethod
    def random_image():
        images = [line.rstrip('\n') for line in open('files/images_property.txt')]
        return random.choice(images)

    @staticmethod
    def get_mortgage(price):
        mortagage = round(price / 180)
        if mortagage > 999999999:
            return '{0:.2f}m / bulan'.format(float(mortagage / 1000000000))

        if mortagage > 999999:
            return '{0:.2f}jt / bulan'.format(float(mortagage / 1000000))

        if mortagage > 999:
            return '{0:.2f}rb / bulan'.format(float(mortagage / 1000))

    @staticmethod
    def get_link_by_id_random():
        ids = [line.rstrip('\n') for line in open('files/property_ids.txt')]
        return "https://99.co/id/properti/{}".format(random.choice(ids))
