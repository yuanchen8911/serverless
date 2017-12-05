'''
Here is our 

'''
from __future__ import print_function

import os
import sys
import json
import apiai

CLIENT_ACCESS_TOKEN = 'c7329636abe648c9ad117c83c0f3bb1f'


class ShoppingBot:
    itemsInfo = {}
    shoppingCart = None

    def __init__(self, data_file):
        self.shoppingCart = None

    def displayGreeting(self):
        print('Hi! Welcome to our grocery store! You can always type Help to get more information about our system!')

    def displayHelp(self):
        print('Buy something -- Say "add something to my cart"')

        print('Remove something -- Say "remove something"')

        print('List items in your shopping cart -- Type list-items')

        print('Check out -- Type checkout')

        print('Type exit to stop shopping')

    def displayItemsInCart(self):
        print(self.shoppingCart.toString)

    def displayBye(self):
        print('Thanks for shopping with us!')
        print('Bye')

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
                print("echo " + userInput)


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.event_request(apiai.events.Event("my_custom_event"))

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "my-session"

    response = request.getresponse()

    print(response.read())

    shoppingBot = ShoppingBot("items.txt")

    shoppingBot.run()


if __name__ == '__main__':
    main()
