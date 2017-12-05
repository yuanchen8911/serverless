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
class ShoppingCart(self):
	def __init__(self):
		