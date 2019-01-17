from helper import GeneralHelper

if __name__ == '__main__':
    prices = [
        100000000,
        500000000,
        750000000,
        1000000000
    ]

    gh = GeneralHelper()
    for price in prices:
        print("------------------------------------------------------------------------------------------------------")
        print("Harga: {}".format(price))
        print("Cicilan: {}".format(gh.get_installment(price)))
        print("------------------------------------------------------------------------------------------------------")
