from __future__ import print_function

import sys
import json
import apiai
import os
from termcolor import colored




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

        if debug:
            print('Start initializing shopping bot...')
        with open(data_file, 'r') as f:
            for line in f.readlines():
                s = line.split(',')
                if debug:
                    print(line)
                self.itemsInfo[s[0]] = Item(s[0], 0, float(s[1]))
            if debug:
                print('Finished initializing shopping bot')

    def displayGreeting(self):
        colored('hello', 'red'), colored('world', 'green')
        print (colored(
            'Hi! Welcome to our grocery store! You can always type Help to get more information about our system!', 'blue'))

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
        print(colored('We only sell by pounds. How many ' + item.unit + " of " + item.itemName + " do you want?",'blue'))
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
            print(colored('Sorry, I don\'t understand.', 'red'))
            self.displayHelp()
            return
        if metadata['intentName'] != 'itemCount':
            print(colored('Sorry, I don\'t understand.', 'red'))
            self.displayHelp()
            return
        count = response['result']['parameters']['number']
        status = self.shoppingCart.addToCart(Item(item.itemName, int(count), item.price))
        if status:
            print(colored("Successfully add " + str(count) + " " + item.unit + " " + item.itemName + " to cart!", 'green'))
        self.displayItemsInCart()

    def run(self):
        self.displayGreeting()
        self.displayHelp()

        while True:

            print(u"> ", end=u"")

            userInput = raw_input()
            os.system('clear')
            if userInput == None or len(userInput) <= 0:
                continue
            # normal flow
            # If the user wants to exit
            if userInput.lower() == 'exit':
                self.displayBye()
                break
            # If the user wants to check shopping cart
            elif userInput.lower() == 'list-items':
                self.displayItemsInCart()
            elif userInput.lower() == 'help':
                self.displayHelp()
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

                # If the query cannot be understood
                if len(metadata) == 0:
                    print('Sorry, I don\'t understand.')
                    self.displayHelp()
                    continue

                # If the user wants to add
                if metadata['intentName'] == 'addToCart':
                    result = response['result']
                    number = result['parameters']['number']
                    items = result['parameters']['Item']

                    # If no item can be detected
                    if len(items) == 0:
                        print(colored('Sorry, I can\'t recognize the item you want to add/remove.', 'red'))
                        self.displayHelp()
                        continue

                    # TO DO: If the item cannot be found in our grocery


                    # If number of items are not specified
                    if len(number) < len(items):
                        for itemName in items:
                            item = self.itemsInfo[itemName]
                            self.askForQuantity(item)
                    # If all items and numbers are specified
                    else:
                        for i in range(len(items)):
                            item = self.itemsInfo[items[i]]
                            self.shoppingCart.addToCart(Item(item.itemName, int(number[i])))
                            print(colored("Successfully add " + str(
                                number[i]) + " " + item.unit + " " + item.itemName + " to cart!", 'green'))
                        self.shoppingCart.printCart()
                # If the user want to remove
                elif metadata['intentName'] == 'removeFromCart':
                    result = response['result']
                    items = result['parameters']['Item']

                    # If no item can be detected
                    if len(items) == 0:
                        print(colored('Sorry, I can\'t recognize the item you want to add/remove.', 'red'))
                        self.displayHelp()
                        continue

                    for itemName in items:
                        self.shoppingCart.removeItem(itemName)
                        print(colored("Successfully remove " + itemName + " from cart!", 'green'))
                    self.shoppingCart.printCart()
                # If the user wants to check out
                elif metadata['intentName'] == 'checkOut':
                    self.shoppingCart.printCart()
                    print(colored("Do you want to checkout (yes/no)?", 'blue'))
                    confirm = raw_input()
                    if confirm.lower() == 'yes':
                        print(colored("Thanks for shopping with us!", 'green'))
                        self.shoppingCart.printCart()
                        self.shoppingCart.getTotal()

                # If the user wants to ask for help or just say greetings
                elif metadata['intentName'] == 'greeting':
                    self.displayGreeting()

                else:
                    print(colored('Sorry, I don\'t understand.', 'red'))

            if debug:
                print("echo " + userInput)


def main():
    global debug
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True
    shoppingBot = ShoppingBot("items.txt")
    shoppingBot.run()


if __name__ == '__main__':
    main()
