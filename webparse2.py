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


from bs4 import BeautifulSoup as bs
import urllib3
import ast


""" get all of the IDs of the foods """
def getID(ls):
    for i in range(len(ls)):
        id = ""
        for c in ls[i]:
            if c in "1234567890":
                id += c

        ls[i] = id

    return ls

""" Get a single name of a food based on its id number"""
def single_food_name(id):
    mainsite = 'https://legacy.cafebonappetit.com/api/2/items?format=json&item=' + str(id)
    request = requests.get(mainsite)
    jsonTest = request.json()

    return jsonTest.get('items').get(str(id)).get('label')

""" Get all the names of the food based on the id numbers"""
def food_name(id_list):
    food_name_list = []
    for x in id_list:
        food_name_list.append(single_food_name(x))
    return food_name_list

""" get the menu for a weekday """
def weekday(menu):
    page = str(requests.get(menu).content)

    ids = re.findall("data-id=..........", page)

    # get all the breakfast ids
    # the first 10 items belong to breakfast and have their ids show up twice so
    # we need to skip every other index
    bk = getID(ids[0:20:2])
    # print(bk)
    print(food_name(bk))

    # get all the lunch ids
    # 20 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    ln = getID(ids[527:567:2])
    # print(ln)
    print(food_name(ln))

    # get all the lunch ids
    # 16 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    dn = getID(ids[2226:2258:2])
    # print(dn)

    time.sleep(3)
    print(food_name(dn))

""" get the menu for a weenend """
def weekend(menu):
    page = str(requests.get(menu).content)

    ids = re.findall("data-id=..........", page)

    # get all the breakfast ids
    # the first 10 items belong to breakfast and have their ids show up twice so
    # we need to skip every other index
    bk = getID(ids[0:20:2])
    if not bk[0] == "7946024":
        # print(bk)
        print("Breakfast:")
        print(food_name(bk))

    # this contains temporary values and will be fixed later
    br = getID(ids[0:20:2])
    if not br[0] == "7946024":
        # print(br)
        print("Brunch:")
        print(food_name(br))

    # these values are wrong and will be fixed later
    # get all the lunch ids
    # 20 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    ln = getID(ids[527:567:2])
    if not ln[0] == "4904249":
        # print(ln)
        print("Lunch:")
        print(food_name(ln))

    # these values are rong an will be fixed later
    # get all the lunch ids
    # 16 items belong to lunch and have their ids show up twice so we need to
    # skip every other index
    dn = getID(ids[2226:2258:2])
    if not dn[0] == "4904249":
        # print(dn)
        time.sleep(3)
        print("Dinner:")
        print(food_name(dn))

""" parse the hamilton dining options and return them in plain text """
def main():
    commons = "https://hamilton.cafebonappetit.com/cafe/soper-commons-cafe/"

    # check to see if the current date is a weekday so the format is correct
    # if (datetime.date.today().weekday()) < 5:
    #     weekday(commons)
    # else:
    if 1 == 1:
        weekend(commons)

# if __name__ == "__main__":
#     main()











































"""
Everything under here should work now.
"""
import ast


data = 'https://hamilton.cafebonappetit.com/cafe/soper-commons-cafe/'

http = urllib3.PoolManager()
beautiful = http.request('GET', data).data

soup = bs(beautiful,'html.parser')
soup_str = str(soup)



# Isolate the menu items from the entire clusterfuck of html bon appetit code
regex_menu = r'Bamco.menu_items+\s+=+\s+(.*)'
menu_matches = re.findall(regex_menu, soup_str)

# Convert the Bamco.menu_items things into json
dishes = json.loads(menu_matches[0][0:-1])

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

#Next, convert the ids to actual food names
for x in range(len(breakfast_id_list)):
    breakfast_food_list.append([])

for x in range(len(lunch_id_list)):
    lunch_food_list.append([])

for x in range(len(dinner_id_list)):
    dinner_food_list.append([])

for x in range(len(breakfast_id_list)):
    for y in breakfast_id_list[x]:
        try:
            z = dishes.get(str(y)).get("label")
            breakfast_food_list[x].append(z)
        except:
            print(str(y) + " returned an error (Breakfast)!")

for x in range(len(lunch_id_list)):
    for y in lunch_id_list[x]:
        try:
            z = dishes.get(str(y)).get("label")
            lunch_food_list[x].append(z)
        except:
            print(str(y) + " returned an error (Lunch)!")

for x in range(len(dinner_id_list)):
    for y in dinner_id_list[x]:
        z = dishes.get(str(y)).get("label")
        dinner_food_list[x].append(z)

# Create lists for (breakfast, lunch and dinner) (ids and food names)
bil = []
for thing in breakfast_id_list:
    for shit in thing:
        bil.append(shit)

lil = []
for thing in lunch_id_list:
    for shit in thing:
        lil.append(shit)

dil = []
for thing in dinner_id_list:
    for shit in thing:
        dil.append(shit)

bfl = []
for thing in breakfast_food_list:
    for shit in thing:
        bfl.append(shit)

lfl = []
for thing in lunch_food_list:
    for shit in thing:
        lfl.append(shit)

dfl = []
for thing in dinner_food_list:
    for shit in thing:
        dfl.append(shit)

# Put all those bil bfl lil lfl dil dfl into one big set
big_list = {}

for i in range(len(bil)):
    big_list[bil[i]] = bfl[i]

for i in range(len(lil)):
    if lil[i] in bil:
        continue
    else:
        big_list[lil[i]] = lfl[i]

for i in range(len(dil)):
    if (dil[i] in bil) or (dil[i] in lil):
        continue
    else:
        big_list[dil[i]] = dfl[i]

# Make dictionary file and put the big list inside
food_file = open("foods.dict", "w")
food_file.write(str(big_list))
food_file.close()

# Test code to get food name from resulting dictionary foods.dict
# This should ideally be in another python file

# t = open("foods.dict", "r")
# t_new = ast.literal_eval(t.read())
#
# print(t_new.get("4904219").encode('utf-8'))



















#{"7946024": "whole egg", "7946025": "liquid egg", "7946026": "egg white", "7946027": "egg beaters", "7946028": "bell pepper", "7946029": "broccoli", "7946031": "mushroom", "7946032": "onion", "7946033": "spinach", "7946034": "tomato", "7946036": "pepper", "7946045": "pico de gallo", "7946046": "salt", "7946047": "american cheese", "7946048": "cheddar cheese", "7946051": "swiss cheese", "7946052": "bacon", "7946055": "turkey breakfast sausage", "7946056": "pork breakfast sausage", "7946058": "smoked ham", "7946061": "pan spray", "7940390": "6' corn tortilla", "7437083": "10' flour tortilla", "7940391": "6' flour tortilla", "4904469": "fresh fruit salad", "4903885": "seven-grain bread", "4903886": "whole grain bread", "4903887": "whole wheat English muffin", "4903888": "rye bread", "4903889": "cinnamon raisin bread", "4903891": "potato bread", "4903892": "sourdough bread", "4903894": "white bread", "4903895": "white English muffin", "4903901": "whole wheat bagel", "4903902": "marble bagel", "4903903": "multigrain bagel", "4903904": "plain bagel", "4903906": "blueberry bagel", "4903907": "everything bagel", "4903908": "onion bagel", "4903909": "Udi's plain bagel", "4903910": "poppy seed bagel", "4903916": "blueberry crumb muffin", "4903917": "blueberry muffin", "4903919": "corn muffin", "4903920": "cranberry orange muffin", "4903921": "chocolate chip muffin", "4903922": "raisin bran muffin", "4937252": "blueberry scone", "4903924": "apple danish", "4903926": "blueberry danish", "4903927": "cheese danish", "4903928": "cinnamon swirl danish", "4903929": "lemon danish", "4903930": "raspberry danish", "4903937": "extra virgin olive oil", "4903938": "peanut butter", "4903939": "tofu cream cheese", "4903940": "blueberry cream cheese", "4903941": "butter unsalted", "4903942": "cream cheese", "4903943": "grape jelly", "4903944": "margarine smart balance", "4903945": "orange marmalade", "4903946": "red raspberry preserves", "4903947": "strawberry preserves", "4903948": "vegetable cream cheese", "9021587": "jelly", "4903755": "whole grain french toast", "11474916": "house-made quinoa pancakes", "11474917": "blueberry whole wheat pancakes", "11474918": "buckwheat pancakes", "11474919": "whole wheat pancakes", "11474920": "house-made blueberry oatmeal pancakes", "11474921": "whole grain French toast", "11474922": "whole grain French toast", "11474923": "multi-grain waffles", "11474924": "whole wheat waffle", "11474925": "Kashi gluten free waffles", "4903756": "buttermilk pancakes", "4903759": "french toast", "11474926": "buttermilk waffle", "11474927": "malted waffles", "11474928": "house-made buttermilk pancakes", "11474929": "golden malted pancakes", "11474930": "buttermilk pancakes", "11474931": "blueberry pancakes", "11474932": "chocolate chip pancakes", "11474933": "banana pancakes", "11474934": "Texas French toast", "11474935": "French toast", "11474936": "brioche french toast", "11474942": "sweet potato hash", "4903864": "home-fried potatoes", "4903865": "tater tots", "11474943": "O'Brien potatoes", "11474944": "sweet potato tots", "11474945": "tater tots", "5185339": "fried egg", "5185340": "scrambled eggs", "5185341": "hard-boiled egg", "7946019": "scrambled eggs", "7946020": "scrambled egg whites", "7946021": "scrambled cholesterol free eggs (egg beaters)", "7946022": "hard-boiled eggs", "5185982": "bacon", "5185983": "pork breakfast sausage", "5185984": "turkey breakfast sausage links", "11479579": "pork breakfast sausage links", "11479535": "egg, ham and cheese on white English muffin", "11479539": "egg, ham and cheese croissant", "4937202": "iced tea unsweetened", "4937203": "earl grey tea", "4937204": "black coffee", "4937205": "iced coffee", "4937206": "hot cocoa", "4937207": "sweet tea", "4937208": "brown sugar", "4937209": "granulated sugar", "4937210": "honey", "4904033": "old-fashioned oatmeal", "4904035": "cream of rice", "4904036": "cream of wheat", "4904037": "grits", "4904038": "cheese grits", "4904059": "Bran Flakes", "4904060": "Cheerios", "4904061": "Corn Flakes", "4904063": "low fat granola with fruit", "4904064": "Raisin Bran cereal", "4904065": "Rice Chex cereal", "4904066": "Special K with Red Berries cereal", "4904067": "Cocoa Puffs", "4904068": "Golden Grahams", "4904069": "house-made granola", "4904070": "Cinnamon Toast Crunch", "4904071": "Cocoa Puffs", "4904072": "Froot Loops cereal", "4904073": "Lucky Charms", "4904076": "raisins", "4904077": "dried cranberry", "4904078": "cinnamon", "4904079": "maple syrup", "4904080": "honey", "4904081": "brown sugar", "4904711": "yogurt plain low fat", "4904712": "yogurt vanilla low fat", "4904713": "yogurt fruit low fat", "4904714": "cottage cheese 2%", "4904715": "yogurt plain full fat greek", "4936985": "orange juice", "4936986": "apple juice", "4936987": "cranberry juice", "4936988": "grape juice", "5185957": "lemonade", "4936992": "almond milk", "4936993": "soy milk vanilla", "4936994": "skim milk", "4936997": "1% chocolate milk", "4936995": "2% milk", "4936996": "whole milk", "4937003": "coca-cola", "4937004": "cherry coca-cola", "4937005": "dr. pepper", "4937006": "ginger ale", "4937177": "diet coke", "4937166": "coke zero", "4937195": "sprite zero", "13110861": "blueberry muffins", "13116642": "coffee cake  muffins"}
