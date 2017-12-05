'''
Here is our 

'''
from __future__ import print_function

import os
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )

    import apiai

CLIENT_ACCESS_TOKEN = 'c7329636abe648c9ad117c83c0f3bb1f'


class ShoppingBot():
    
    def __init__(self, data_file):
        self.items_info = {}
    # read data from file

    def displayGreeting(self):
        print
        'Hi! Welcome to our grocery store! You can always type Help to get more information about our system!'

    def displayHelp(self):
        print
        'Buy something -- Say "add something to my cart"'

        print
        'Remove something -- Say "remove something"'

        print
        'List items in your shopping cart -- Type list-items'

        print
        'Check out -- Type checkout'

    def run(self):
        self.displayGreeting()
        self.displayHelp()

        userInput = sys.stdin.readline()

        while userInput !=:


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.event_request(apiai.events.Event("my_custom_event"))

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    response = request.getresponse()

    print(response.read())

    shoppingBot = ShoppingBot("items.txt")

    shoppingBot.run()


if __name__ == '__main__':
    main()

