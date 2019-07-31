# -*- coding: utf-8 -*-

"""
Proj: CoreHaMenu - a menu fetching bot

Auth: Nate Koike, Ken Fung

Desc: Pull menu information off of the Hamilton College site with faster access
      times than the official Hamilton College app
"""
# needed to pull website information and code to be processed by this program
import requests
# needed to extraxt information from a json representation of the food
import json
# needed to isolate the id number of the food and perform general operations
import re
# needed to prevent the legacy server from timing out the connection
import time
# needed to find the day of the week for proper formatting of menu
import datetime

# for the parsing of raw HTML data
from bs4 import BeautifulSoup as bs
import urllib3
import ast

#for utf-8 encoding purposes
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Get the raw data fron the bon appetit site
data = 'https://hamilton.cafebonappetit.com/cafe/soper-commons-cafe/'

# Use urllib and beautifulsoup to parse the raw HTML data
http = urllib3.PoolManager()
beautiful = http.request('GET', data).data
soup = bs(beautiful,'html.parser')
soup_str = str(soup)

# Isolate the menu items from the entire clusterfuck of html bon appetit code
regex_menu = r'Bamco.menu_items+\s+=+\s+(.*)'
menu_matches = re.findall(regex_menu, soup_str)

# Convert the Bamco.menu_items things into json
dishes = json.loads(menu_matches[0][0:-1])

# For diagnostic purposes
#dish_keys = (list(dishes.keys()))
# for x in dish_keys:
#     print(dishes.get(x).get("label"))

# Get the menu items for the day from Bamco.dayparts
list_of_dicts = []
for i in range(len(soup.find_all('script'))):
	if "Bamco.dayparts" in str(soup.find_all('script')[i]):
		soup3 = soup.find_all('script')[i]
		x = str(soup3.text)

		x = x.replace("Bamco.dayparts", "")
		x= x.replace("=", "")
		x= x.replace("Bamco", "")
		x= x.replace("||", "")
		x= x.replace(";", "")
		x= x.replace("function", "")
		x= x.replace("{}", "")
		x= x.replace("(", "")
		x= x.replace(")", "")

		x = ' '.join(x.split())
		y = json.loads(x[8:-1])

		list_of_dicts.append(y)

# For each station, get the label and the list of food items
breakfast_label_list = []
breakfast_id_list = []
breakfast_food_list = []

brunch_label_list = []
brunch_id_list = []
brunch_food_list = []

lunch_label_list = []
lunch_id_list = []
lunch_food_list = []

dinner_label_list = []
dinner_id_list = []
dinner_food_list = []

for x in range(len(list_of_dicts)):
	if list_of_dicts[x].get('label') == 'Breakfast':
		station = list_of_dicts[x].get('stations')
		for g in range(len(station)):
			breakfast_label_list.append(station[g].get("label"))
			breakfast_id_list.append(station[g].get("items"))

for x in range(len(list_of_dicts)):
	if list_of_dicts[x].get('label') == 'Brunch':
		station = list_of_dicts[x].get('stations')
		for g in range(len(station)):
			brunch_label_list.append(station[g].get("label"))
			brunch_id_list.append(station[g].get("items"))

for x in range(len(list_of_dicts)):
	if list_of_dicts[x].get('label') == 'Lunch':
		station = list_of_dicts[x].get('stations')
		for g in range(len(station)):
			lunch_label_list.append(station[g].get("label"))
			lunch_id_list.append(station[g].get("items"))

for x in range(len(list_of_dicts)):
	if list_of_dicts[x].get('label') == 'Dinner':
		station = list_of_dicts[x].get('stations')
		for g in range(len(station)):
			dinner_label_list.append(station[g].get("label"))
			dinner_id_list.append(station[g].get("items"))

#For diagnostics

# print("Breakfast Label List: " + str(breakfast_label_list))
# print("Breakfast ID List: " + str(breakfast_id_list))
#
# print("Brunch Label List: " + str(brunch_label_list))
# print("Brunch ID List: " + str(brunch_id_list))
#
# print("Lunch Label List: " + str(lunch_label_list))
# print("Lunch ID List: " + str(lunch_id_list))
#
# print("Dinner Label List: " + str(dinner_label_list))
# print("Dinner ID List: " + str(dinner_id_list))

# Converting the food ids to actual food names
# Create the blank lists for each meal category first
for x in range(len(breakfast_id_list)):
    breakfast_food_list.append([])

for x in range(len(lunch_id_list)):
    lunch_food_list.append([])

for x in range(len(dinner_id_list)):
    dinner_food_list.append([])

for x in range(len(breakfast_id_list)):
    for y in breakfast_id_list[x]:
        z = dishes.get(str(y)).get("label")
        breakfast_food_list[x].append(z)

for x in range(len(lunch_id_list)):
    for y in lunch_id_list[x]:
        z = dishes.get(str(y)).get("label")
        lunch_food_list[x].append(z)

for x in range(len(dinner_id_list)):
    for y in dinner_id_list[x]:
        z = dishes.get(str(y)).get("label")
        dinner_food_list[x].append(z)

# Create lists for (breakfast, lunch and dinner) (ids and food names)
bil = []
for thing in breakfast_id_list:
    for stuff in thing:
        bil.append(stuff)

lil = []
for thing in lunch_id_list:
    for stuff in thing:
        lil.append(stuff)

dil = []
for thing in dinner_id_list:
    for stuff in thing:
        dil.append(stuff)

bfl = []
for thing in breakfast_food_list:
    for stuff in thing:
        bfl.append(stuff)

lfl = []
for thing in lunch_food_list:
    for stuff in thing:
        lfl.append(stuff)

dfl = []
for thing in dinner_food_list:
    for stuff in thing:
        dfl.append(stuff)

#Put all those bil bfl lil lfl dil dfl into one big list
big_list = {}
count = 1

for i in range(len(bil)):
    big_list[bil[i]] = bfl[i]
    count += 1

for i in range(len(lil)):
    if lil[i] in bil:
        continue
    else:
        big_list[lil[i]] = lfl[i]
        count += 1

for i in range(len(dil)):
    if (dil[i] in bil) or (dil[i] in lil):
        continue
    else:
        big_list[dil[i]] = dfl[i]
        count += 1
#
# Make dictionary file and put the big list inside
food_file = open("foods_final.dict", "w")
food_file.write(str(big_list))
food_file.close()
print(count)

# Test code to get food name from resulting dictionary foods_final.dict
# This should ideally be in another python file

# t = open("foods_final.dict", "r")
# t_new = ast.literal_eval(t.read())
#
# print(t_new.get("4904128").encode('utf-8'))

# When we arrive back at Hamilton, figure out the relevant labels to add below!

# Grab the dinner home items and put them into a new file
dinner_home_list = []
for x in range(len(dinner_label_list)):
    if dinner_label_list[x] == "home":
        for id in dinner_id_list[x]:
            print(id)
            dinner_home_list.append(t_new.get(id))

dinner_home_file = open("dinner_home_list", "w")
dinner_home_file.write(str(dinner_home_list))
dinner_home_file.close()

# Grab the breakfast omelet items and put them into a new file
breakfast_omelet_list = []
for x in range(len(breakfast_label_list)):
    if breakfast_label_list[x] == "omelets":
        for id in breakfast_id_list[x]:
            print(id)
            breakfast_omelet_list.append(t_new.get(id))

breakfast_omelet_file = open("breakfast_omelet_list", "w")
breakfast_omelet_file.write(str(breakfast_omelet_list))
breakfast_omelet_file.close()


# # For diagnostics purposes
# print("Dinner home list: " + str(dinner_home_list))
# print("Breakfast omelet list: " + str(breakfast_omelet_list))

# if __name__ == "__main__":
#     main()
