"""
Proj: CoreHaMenu - a menu fetching bot

Auth: Nate Koike, Ken Fung

Desc: Pull menu information off of the Hamilton College site with faster access
      times than the official Hamilton College app
"""
# needed to pull website information and code to be processed by this program
import requests
# needed to extract information from a json representation of the food
import json
# needed to isolate the id number of the food and perform general operations
import re
# needed to prevent the legacy server from timing out the connection
import time
# needed to find the day of the week for proper formatting of menu
import datetime
# needed to import the dictionary
import ast
# needed to make the dictionary if it doesn't already exist
import makeDictionary
# needed to run code dail

""" get all of the IDs of the foods """
def getID(ls):
    for i in range(len(ls)):
        id = ""
        for c in ls[i]:
            if c in "1234567890":
                id += c

        ls[i] = id

    return ls

""" Get all the names of the food based on the id numbers"""
def food_name(id_list, dict):
    food_name_list = []
    for id in id_list:
        food_name_list.append(dict.get(id))
    return food_name_list

""" get the menu for a weekday """
def weekday(menu, dict):
    page = str(requests.get(menu).content)

    ids = re.findall("data-id=..........", page)

    # get all the breakfast ids
    # the first 10 items belong to breakfast and have their ids show up twice so
    # we need to skip every other index
    bk = getID(ids[0:20:2])
    # print(bk)
    print(food_name(bk, dict))

    # get all the lunch ids
    # 20 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    ln = getID(ids[527:567:2])
    # print(ln)
    print(food_name(ln, dict))

    # get all the lunch ids
    # 16 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    dn = getID(ids[2226:2258:2])
    print(food_name(dn, dict))

""" get the menu for a weekend """
def weekend(menu, dict):
    page = str(requests.get(menu).content)

    ids = re.findall("data-id=..........", page)

    # get all the breakfast ids
    # the first 10 items belong to breakfast and have their ids show up twice so
    # we need to skip every other index
    bk = getID(ids[0:20:2])
    if not bk[0] == "7946024":
        # print(bk)
        print("Breakfast:")
        print(bk)
        print(food_name(bk, dict))
        print("")

    # this contains temporary values and will be fixed later
    br = getID(ids[0:20:2])
    if not br[0] == "7946024":
        # print(br)
        print("Brunch:")
        print(br)
        print(food_name(br, dict))
        print("")

    # these values are wrong and will be fixed later
    # get all the lunch ids
    # 20 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    ln = getID(ids[527:567:2])
    if not ln[0] == "4904249":
        print(ln)
        print("Lunch:")
        print(food_name(ln, dict))
        print("")

    # these values are rong an will be fixed later
    # get all the lunch ids
    # 16 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    dn = getID(ids[2226:2258:2])
    if not dn[0] == "4904249":
        print(dn)
        print("Dinner:")
        print(food_name(dn, dict))

""" make a dictionary of all of the food IDs and their names """
def make_dict():
    dict = open("foods.dict", "w")

""" parse the hamilton dining options and return them in plain text """
def main():
    commons = "https://hamilton.cafebonappetit.com/cafe/soper-commons-cafe/"
    backend = "https://legacy.cafebonappetit.com/api/2/items?format=json&item"

    # check to see if the current date is a weekday so the format is correct
    # if (datetime.date.today().weekday()) < 5:
    #     weekday(commons)
    # else:
    try:
        dict = ast.literal_eval((open("foods.dict", "r")).read())
    except:
        # makeDictionary.create()
        print("ran")
        return

    if 1 == 1:
        weekend(commons, dict)

if __name__ == "__main__":
    main()
