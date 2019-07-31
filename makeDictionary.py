"""
Proj: CoreHaMenu

Auth: Nate Koike

Desc: Pull menu information and assemble a dictionary with the resulting data.
      This operation will take a long time because of the extremely frequent web
      and disk access
"""
# needed to access a web page
import requests as rq
# needed to pull information from a web page
import json
# needed to prevent the site from thworing an error because of hightened access
import time
# needed to make a dictionary from a file
import ast

""" update the dictionary web must be a json compatible web address """
def update(web):
    dict = ast.literal_eval((open("foods.dict", "r").read()))

    # loop through an absurd number of numbers until there is no value
    for i in range(99999999):
        request = web + str(i) # append the number to the end of the address

        if (type(dict.get(str(i))) == "NoneType") or dict.get(str(i)) == "None":
            print(i)
            name = "None"

            # this will exit the loop once the number stops being a valid menu item
            try:
                name = rq.get(request).json().get("items").get(str(i)).get("label")
            except:
                0 == 0

            # add the item to the dictionary with the number as the key (id: food)
            dict[str(i)] = name

            # wait for the server to clear up again
            time.sleep(3)

    # write the dictionary to a file
    output = open("foods.dict", "w")
    output.write(str(dict))
    output.close()

    return

""" create the dictionary; web must be a json compatible web address """
def create(web):
    dict = {} # make a dictionary as a set

    # loop through an absurd number of numbers until there is no value
    for i in range(99999999):
        request = web + str(i) # append the number to the end of the address
        name = "None"

        print(i)

        # this will exit the loop once the number stops being a valid menu item
        try:
            name = rq.get(request).json().get("items").get(str(i)).get("label")
        except:
            0 == 0

        # add the item to the dictionary with the number as the key (id: food)
        dict[str(i)] = name

    # write the dictionary to a file
    output = open("foods.dict", "w")
    output.write(str(dict))
    output.close()

    return
