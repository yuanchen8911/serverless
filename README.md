# Shopping Bot CUI
## Overview 
A shopping CUI that allows the user adding/removing items toward a shopping cart, reviewing and checking out shopping cart. 
## User Stories
User A: As someone don’t want to go shopping, user would like to order my daily groceries by entering the name of the item and the amount in common language. In this way, user can access the basic functionality of the product.


User B: As a user, I want to see what are in my shopping cart every time I make any changes, such as adding or removing things from my shopping cart, so that it reminds me what else I need to purchase and helps to to compare different options.

User C: As users might mistype things, the app should be able to understand some synonyms as well as giving suggestions as it couldn’t find synonyms in database. In this way, the application can handle mistakes made by users. 

User D: As users who want to make changes, users would want to remove items from their shopping cart, this will support user to change their minds and making the application more usable. 

## Features

* Add certain amount of items to shopping cart.
* Matching partial names to item full name in the store. e.g. trouts" -> "smoked rainbow trout"
* Remove certain amount of items from shopping cart.
* List current status of the shopping cart.
* checkout items from shopping cart.
* Debug Mode

## Dependencies (Install required Python packages)
> sudo pip install apiai

> sudo pip install termcolor
## Running example 
start the program 
> python ShoppingBot.py

add to cart
> add two apples

remove from cart
> delete two apples

list status
> show me the cart

checkout 
> that's it, check out!

greeting
> What's up 

Enter Debug Mode
> python ShoppingBot.py --debug
## List of Available Products (Common groceries can be found at store.)
#### Our database contains around 2000 items, some of them are less commonly seen, here are some common ones.The full list of items is in Grocery/prices.txt
"sushi" -> "california roll sushi"

"alaskan cod" -> "mulit grain alaskan cod"

"apple" -> "organic honeycrisp apple"

"lemons" -> "organic lemons"

"chicharrones" -> "hot n spicy chicharrones"

"trouts" -> "smoked rainbow trout"

## Synonyms Data Preparation and Matching
1. Preprocess the given items (https://www.instacart.com/datasets/grocery-shopping-2017)
2. Establish synonym connections between potential search items with products names stored in database.

## Logic flow 
### checkout and greetings
![](https://github.com/wwyiyi/95729cui/blob/master/images/1.png)
### adding and remove items
![](https://github.com/wwyiyi/95729cui/blob/master/images/3.png)
### List of Intents
* addToCart
* checkOut
* greeting
* itemCount
* removeFromCart
### List of Entities
* apples
* pear
* and many more 
