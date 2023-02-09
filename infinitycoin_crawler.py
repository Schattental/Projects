import requests
from bs4 import BeautifulSoup
import operator
from tkinter import *
import time
while True:
    time.sleep(10)

    class App(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.pack()

    def start(url):
        word_list = []
        source_code = requests.get(url).text
        soup = BeautifulSoup(source_code, "html.parser")
        for post_text in soup.findAll("div", {"class": "col-xs-12 btc-color"}):
            content = post_text.string
            words = content.split()
            for each_word in words:
                word_list.append(each_word)
        clean_up_list(word_list)


    def clean_up_list(word_list):
        clean_word_list = []
        for word in word_list:
            symbols = ""
            for i in range(0, len(symbols)):
                word = word.replace(symbols[i], " ")
            if len(word) > 0:
                clean_word_list.append(word)
        create_dictionary(clean_word_list)


    def create_dictionary(clean_word_list):
        word_count = {}
        for word in clean_word_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        for key, value in sorted(word_count.items(), key=operator.itemgetter(1)):
            "print(key, value)"
        price_check(clean_word_list)


    def price_check(clean_word_list):
        price = "0.002"
        for word in clean_word_list:
            if word == price in clean_word_list:
                app = App()
                app.master.title("Price Checker Infinitycoin")
                app.master.maxsize(500,500)
                app.master.minsize(500,500)

                label = Label(app, text="Price of Infinitycoin has reached requested value of")
                label.pack()
                value = Label(app, text=price)
                desc = Label(app, text="in USD")
                value.pack()
                desc.pack()
                app.mainloop()
                break

    start("https://infinitycoin.exchange/")
