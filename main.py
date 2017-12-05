from __future__ import print_function

import os
import sys
import json
import apiai

from shoppingCart import Cart
from items import Item

CLIENT_ACCESS_TOKEN = 'c7329636abe648c9ad117c83c0f3bb1f'
debug = False


class ShoppingBot:
    itemsInfo = {}
    shoppingCart = None
    ai = None

    def __init__(self, data_file):
        self.shoppingCart = Cart()
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        print('Start initializing shopping bot...')
        with open(data_file, 'r') as f:
            for line in f.readlines():
                s = line.split(',')
                if debug:
                    print(line)
                self.itemsInfo[s[0]] = Item(s[0], 0, float(s[1]))
            print('Finished initializing shopping bot')

    def displayGreeting(self):
        print(
            'Hi! Welcome to our grocery store! You can always type Help to get more information about our system!')

    def displayHelp(self):
        print('Buy something -- Say "add something to my cart"')

        print('Remove something -- Say "remove something"')

        print('List items in your shopping cart -- Type list-items')

        print('Check out -- Type checkout')

        print('Type exit to stop shopping')

    def displayItemsInCart(self):
        self.shoppingCart.printCart()

    def displayBye(self):
        print('Thanks for shopping with us!')
        print('Bye')

    def askForQuantity(self, item):
        print('How many ' + item.unit + " of " + item.itemName + " do you want?")
        userInput = raw_input()
        request = self.ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'
        request.session_id = "1"
        request.query = userInput
        response = json.loads(request.getresponse().read())

        if debug:
            print(response)

        metadata = response['result']['metadata']

        if len(metadata) == 0:
            print('Sorry, I don\'t understand.')
            self.displayHelp()
            return
        if metadata['intentName'] != 'itemCount':
            print('Sorry, I don\'t understand.')
            self.displayHelp()
            return
        count = response['result']['parameters']['number']
        self.shoppingCart.addToCart(Item(item.itemName, count, item.price))
        print("Successfully add " + str(count) + " " + item.unit + " " + item.itemName + " to cart!")
        self.displayItemsInCart()

    def run(self):
        self.displayGreeting()
        self.displayHelp()

        while True:
            print(u"> ", end=u"")

            userInput = raw_input()

            # normal flow
            if userInput.lower() == 'exit':
                self.displayBye()
                break
            elif userInput.lower() == 'list-items':
                self.displayItemsInCart()
            elif userInput.lower() == 'checkout':
                self.displayItemsInCart()
                self.displayBye()
            else:
                # send to aiapi
                request = self.ai.text_request()

                request.lang = 'en'  # optional, default value equal 'en'

                request.session_id = "1"

                request.query = userInput

                response = json.loads(request.getresponse().read())

                if debug:
                    print(response)

                metadata = response['result']['metadata']

                if len(metadata) == 0:
                    print('Sorry, I don\'t understand.')
                    self.displayHelp()
                    continue

                result = response['result']
                number = result['parameters']['number']
                items = result['parameters']['Item']

                if len(items) == 0:
                    print('Sorry, I don\'t understand.')
                    self.displayHelp()
                    continue

                if len(number) < len(items):
                    for itemName in items:
                        item = self.itemsInfo[itemName]
                        self.askForQuantity(item)
                else:
                    for i in range(len(items)):
                        item = self.itemsInfo[itemName]

            print("echo " + userInput)


def main():
    global debug
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True
    shoppingBot = ShoppingBot("items.txt")
    shoppingBot.run()


if __name__ == '__main__':
    main()
