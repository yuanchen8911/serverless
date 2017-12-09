from __future__ import print_function

import json
import os
import sys

import apiai
from termcolor import colored

from ShoppingComponents.items import Item
from ShoppingComponents.shoppingCart import Cart

# This is the client access token for DialogFlow, specific to client
CLIENT_ACCESS_TOKEN = 'c7329636abe648c9ad117c83c0f3bb1f'

# Debug mode to output responses
debug = False


class ShoppingBot:
    itemsInfo = {}
    shoppingCart = None
    ai = None

    '''
    Initialization of server connection and data import
    '''

    def __init__(self, data_file):
        self.shoppingCart = Cart()
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        if debug:
            print('Start initializing shopping bot...')

        # Import grocery as csv format
        with open(data_file, 'r') as f:
            for line in f.readlines():
                s = line.split(',')
                if debug:
                    print(line)
                self.itemsInfo[s[0]] = Item(s[0], 0, float(s[1]))
            if debug:
                print('Finished initializing shopping bot')

    def displayMessage(self, category):

        # The Greeting message to display
        if category == 'Greeting':
            colored('hello', 'red'), colored('world', 'green')
            print(colored(
                'Hi! Welcome to our grocery store! '
                'You can always type "help" to get more information about our system!',
                'blue'))

        # The Help message to display
        elif category == 'Help':

            print(colored(
                'Want to put items in shopping cart? -- Try "add three apples to my cart"\n'
                'Want to remove items from shopping cart? -- Try "remove all apples"\n'
                'Want check what\'s in your shopping cart? -- Try "Show me my cart?"\n'
                'Want to checkout? -- Try "check me out"\n'
                'Want to exit? -- Try "exit"',
                'green'))

        # The End Conversation message to display
        elif category == 'End':
            print(colored(
                'Thanks for shopping with us! Have a nice day!',
                'green'))

        # The Error message to display for not recognizing
        elif category == 'Error':
            print(colored(
                'Sorry, I don\'t understand.',
                'red'))

        # The Error message to display for no such item
        elif category == 'NoItem':
            print(colored(
                'Sorry, I can\'t recognize the item you want to add/remove.', 'red',
                'red'
            ))

    '''
    List items inside the shopping cart
    '''

    def displayItemsInCart(self):
        self.shoppingCart.printCart()

    '''
    Set up connection with Dialog Flow, send query and return with response
    '''

    def sendQuery(self, userInput):
        request = self.ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'
        request.session_id = "1"
        request.query = userInput
        response = json.loads(request.getresponse().read())
        return response

    '''
    Ask for quantity if a user doesn't specify when purchasing or removing items
    '''

    def askForQuantity(self, item, action):
        if action == 'add':
            print(colored('We only sell by pounds. How many ' + item.unit + " of " + item.itemName + " do you want?", 'blue'))
        elif action == 'remove':
            print (colored('How many '+item.itemName +" do you want to remove?",'blue'))
                
        userInput = raw_input()
        while (userInput == None or len(userInput) <= 0):
            userInput = raw_input()

        response = self.sendQuery(userInput)

        if debug:
            print(response)


        metadata = response['result']['metadata']

        # If it can not be understood
        if len(metadata) == 0:
            self.displayMessage('Error')
            self.displayMessage('Help')
            return

        # If user doesn't contain number
        if metadata['intentName'] != 'itemCount':
            self.displayMessage('Error')
            self.displayMessage('Help')
            return

        count = response['result']['parameters']['number']
        if action == 'add':
            self.shoppingCart.addToCart(Item(item.itemName, int(count), item.price))
            print(colored("Successfully add " + str(count) + " " + item.unit + " " + item.itemName + " to cart!",
                          'green'))

        elif action == 'remove':
            ret = self.shoppingCart.editCart(Item(item.itemName), int(count))
            if ret:
                print(colored("Successfully remove " + item.itemName + " from cart!", 'green'))

        self.displayItemsInCart()

    def run(self):
        self.displayMessage('Greeting')
        self.displayMessage('Help')

        while True:

            print(u"> ", end=u"")

            userInput = raw_input()
            os.system('clear')
            if userInput == None or len(userInput) <= 0:
                continue
            # normal flow
            # If the user wants to exit
            if userInput.lower() == 'exit':
                self.displayMessage('End')
                break
            elif userInput.lower() == 'help':
                self.displayMessage('Help')
            else:
                response = self.sendQuery(userInput)

                if debug:
                    print(response)

                metadata = response['result']['metadata']

                # If the query cannot be understood
                if len(metadata) == 0:
                    self.displayMessage("Error")
                    self.displayMessage('Help')
                    continue

                # If the user wants to add
                if metadata['intentName'] == 'addToCart':
                    result = response['result']
                    number = result['parameters']['number']
                    items = result['parameters']['Item']

                    # If no item can be detected
                    if len(items) == 0:
                        self.displayMessage('NoItem')
                        self.displayMessage('Help')
                        continue

                    # If number of items are not specified
                    if len(number) < len(items):
                        for itemName in items:
                            item = self.itemsInfo[itemName]
                            self.askForQuantity(item, 'add')


                    # If all items and numbers are specified
                    else:
                        for i in range(len(items)):
                            item = self.itemsInfo[items[i]]
                            self.shoppingCart.addToCart(Item(item.itemName, number[i], item.price))
                            print(colored("Successfully add " + str(
                                number[i]) + " " + item.unit + " " + item.itemName + " to cart!", 'green'))
                        self.shoppingCart.printCart()

                # If the user want to remove
                elif metadata['intentName'] == 'removeFromCart':
                    result = response['result']
                    items = result['parameters']['Item']
                    number = result['parameters']['number']
                    all = result['parameters']['all']

                    # If no item can be detected
                    if len(items) == 0:
                        self.displayMessage("NoItem")
                        self.displayMessage("Help")
                        continue

                    # If remove all of the products
                    if all == 'true':
                        for itemName in items:
                            ret = self.shoppingCart.removeItem(itemName)
                            if ret:
                                print(colored("Successfully remove " + itemName + " from cart!", 'green'))
                        self.shoppingCart.printCart()
                        continue

                    # If remove a certain number of products
                    else:
                        # If number of items are not specified
                        if len(number) < len(items):
                            for itemName in items:
                                item = self.itemsInfo[itemName]
                                self.askForQuantity(item, 'remove')
                                continue

                        else:
                            for i in range(len(items)):
                                item = self.itemsInfo[items[i]]
                                ret = self.shoppingCart.editCart(Item(item.itemName), int(number[i]))
                                if ret:
                                    print(colored(
                                        "Successfully remove " + str(number[i]) + ' ' + items[i] + " from cart!",
                                        'green'))
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
                    self.displayMessage('Greeting')

                else:
                    self.displayMessage("Error")

            if debug:
                print("echo " + userInput)


def main():
    global debug
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True
    shoppingBot = ShoppingBot("Grocery/price.txt")
    shoppingBot.run()


if __name__ == '__main__':
    main()
