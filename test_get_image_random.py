from helper import GeneralHelper

if __name__ == '__main__':
    gh = GeneralHelper()
    for count in range(0, 10):
        print("------------------------------------------------------------------------------------------------------")
        print("Counter: {}".format(count))
        print("Image Path: {}".format(gh.random_image()))
        print("------------------------------------------------------------------------------------------------------")
