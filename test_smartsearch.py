
from modules.chatbot.chatbot import get_data_from_es

teks = [
    'cari rumah di jual di bandung',
    # 'cari rumah di bandung',
    # 'cari rumah di jual',
    # 'cari apartement',
    # 'cari ruko',
    # 'bandung',
    # 'sukajadi',
    # 'rumah di jual di sukajadi 100jt',
    # '100 - 500jt',
    # '500 - 750jt',
    # '750 - 1mily',
    # '1mily - 5mily'
]

if __name__ == '__main__':
    for text in teks:
        print("-------------------------------------------------------------------------------------------------------")
        print("Text : {}".format(text))
        get_data_from_es(text)
        print("-------------------------------------------------------------------------------------------------------")
