import requests
import json
from urllib.request import urlopen
import csv
import secrets

from torch import numel

CACHE_FILENAME = "yelp_cache.json"
CACHE_DICT = {}

yelp_key = secrets.YELP_API_KEY

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

def make_request(baseurl, params, headers=None):
    '''Make a request to the Web API using the baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    response = requests.get(endpoint_url, params=params, headers=headers)
    json_data = response.json()

    return json_data

def make_request_with_cache(baseurl, params, headers=None):
    '''Check the cache for a saved result for this baseurl+params
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        return CACHE_DICT[request_key]
    else:
        CACHE_DICT[request_key] = make_request(baseurl, params, headers)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

CACHE_DICT = open_cache()

endpoint_url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': yelp_key}
results = []
for offset in range(0, 1000, 50):
        params = {
            'location': 'MI',
            'limit': '50',
            'sort_by':'rating',
            'offset': offset
        }
        results.extend(make_request_with_cache(endpoint_url, params=params, headers=headers)['businesses'])


restaurants = []

for i in results:

    try:
        restaurants.append({
            'name': i['name'],
            'categories': i['categories'],
            'rating': i['rating'],
            'price': i['price'],
            'city': i['location']['city'],
            'address': i['location']['display_address'],
            'phone': i['display_phone']
            
        })
    except:
        restaurants.append({
            'name': i['name'],
            'categories': i['categories'],
            'rating': i['rating'],
            'price': 'Price not provided',
            'address': i['location']['display_address'],
            'city': i['location']['city'],
            'address': i['location']['display_address'],
            'phone': i['display_phone']
        })


# Categories

cities = []
for i in restaurants:
    if i['city'] not in cities:
        cities.append(i['city'])
    else:
        continue
cities.sort()
print(cities)
print(len(cities))

categories = ['Deli', 'Coffee and Tea', 'Deserts', 'American', 'Healthy', 
'International', 'Bars', 'Mediterranean and Seafood']

# Subcategories
Deli = ['Sandwiches', 'Delis', 'Bakeries','Bagels']

CoffeeAndTea = ['Coffee & Tea', 'Cafes', 'Coffee Roasteries', 'Tea Rooms']

Deserts = ['Desserts', 'Chocolatiers & Shops', 'Ice Cream & Frozen Yogurt', 
'Patisserie/Cake Shop', 'Gelato', 'Macarons', 'Shaved Ice', 'Custom Cakes', 'Cupcakes', 'Candy Stores' ]

American = ['American (Traditional)', 'Middle Eastern', 'American (New)',
'Pizza','Breakfast & Brunch','Diners','Fast Food','Burgers','Hot Dogs',
'Chicken Wings','Donuts','Soul Food','Cheesesteaks','Southern','Cajun/Creole'
,'Steakhouses','Smokehouse','Barbeque','Waffles']

Healthy = ['Juice Bars & Smoothies','Salad','Soup','Vegan','Health Markets',
'Vegetarian','Gluten-Free','Wraps','Fruits & Veggies','Live/Raw Food']

International = ['Africa', 'Asia', 'Latin America', 'Europe', 'Canada']

Bars = ['Distilleries','Whiskey Bars','Cocktail Bars','Wine Bars','Beer Bar',
'Tiki Bars','Bars','Brewpubs','Dive Bars','Breweries','Gastropubs','Pubs','Meaderies',
'Beer, Wine & Spirits','Speakeasies','Beer Gardens','Sports Bars','Irish Pub',
'Hookah Bars','Karaoke','Restaurants','Pool Halls','Eatertainment']

MediterraneanAndSeafood = ['Seafood','Mediterranean','Seafood Markets']

# Africa = ['African','Moroccan','Senegalese','Ethiopian']

# Asia = ['Lebanese','Chinese','Indian','Himalayan/Nepalese','Halal',
# 'Asian Fusion','Arabic','Ramen','Japanese','Noodles','Bubble Tea','Sushi Bars','Thai',
# 'Pan Asian','Poke','Syrian','Vietnamese','Bangladeshi','Russian','Izakaya','Armenian',
# 'Filipino','Korean','Szechuan','Falafel','Dim Sum','Laotian','Pakistani']

# LatinAmerica = ['Tapas/Small Plates','Mexican','Tacos','Salvadoran','Peruvian','Venezuelan',
# 'Argentine','Food Stands','Caribbean','Cuban','Latin American','Honduran','Tapas Bars','Dominican',
# 'Brazilian','Acai Bowls']

# Europe = ['Italian','Polish','Greek','Fish & Chips','Ukrainian','Spanish','Modern European','German',
# 'Irish','Hungarian','Kebab','British','Belgian','French','Creperies']

# Canada = ['Canadian (New)','Poutineries']

int_file = open('International.txt', 'r')
line = int_file.readlines()
int_file.close()
cleanList = [x.strip("\n") for x in line]

Africa = cleanList[cleanList.index('Africa')+1:cleanList.index('Asia')]
Asia = cleanList[cleanList.index('Asia')+1:cleanList.index('Latin America')]
LatinAmerica = cleanList[cleanList.index('Latin America')+1:cleanList.index('Europe')]
Europe = cleanList[cleanList.index('Europe')+1:cleanList.index('Canada')]
Canada = cleanList[cleanList.index('Canada')+1:]

prices = ['$', '$$', '$$$', '$$$$', '$$$$$']

dicts = {}

deli_dict = {}
coffee_dict = {}
deserts_dict = {}
american_dict = {}
healthy_dict = {}
international_dict = {}
bars_dict = {}
med_dict = {}
africa_dict = {}
asia_dict = {}
latin_dict = {}
europe_dict = {}
canada_dict = {}


for z in restaurants:
    for c in z['categories']:
        try:
            rest = {
                'name': z['name'],
                'rating': z['rating'],
                'price': z['price'],
                'city': z['city'],
                'address': z['address'][0],
                'phone': z['phone']
            }
        except:
            rest = {
                'name': z['name'],
                'rating': z['rating'],
                'price': 'Price not provided',
                'city': z['city'],
                'address': z['address'][0],
                'phone': z['phone']
            }
        if c['title'] in Deli:
            if c['title'] in deli_dict.keys():
                deli_dict[c['title']].append(rest)
            else:
                deli_dict[c['title']] = [rest]
        elif c['title'] in CoffeeAndTea:
            if c['title'] in coffee_dict.keys():
                coffee_dict[c['title']].append(rest)
            else:
                coffee_dict[c['title']] = [rest]
        elif c['title'] in Deserts:
            if c['title'] in deserts_dict.keys():
                deserts_dict[c['title']].append(rest)
            else:
                deserts_dict[c['title']] = [rest]
        elif c['title'] in American:
            if c['title'] in american_dict.keys():
                american_dict[c['title']].append(rest)
            else:
                american_dict[c['title']] = [rest]
        elif c['title'] in Healthy:
            if c['title'] in healthy_dict.keys():
                healthy_dict[c['title']].append(rest)
            else:
                healthy_dict[c['title']] = [rest]
        elif c['title'] in Africa:
                if c['title'] in africa_dict.keys():
                    africa_dict[c['title']].append(rest)
                else:
                    africa_dict[c['title']] = [rest]
        elif c['title'] in Asia:
            if c['title'] in asia_dict.keys():
                asia_dict[c['title']].append(rest)
            else:
                asia_dict[c['title']] = [rest]
        elif c['title'] in LatinAmerica:
            if c['title'] in latin_dict.keys():
                latin_dict[c['title']].append(rest)
            else:
                latin_dict[c['title']] = [rest]
        elif c['title'] in Europe:
            if c['title'] in europe_dict.keys():
                europe_dict[c['title']].append(rest)
            else:
                europe_dict[c['title']] = [rest]
        elif c['title'] in Canada:
            if c['title'] in canada_dict.keys():
                canada_dict[c['title']].append(rest)
            else:
                canada_dict[c['title']] = [rest]
        elif c['title'] in Bars:
            if c['title'] in bars_dict.keys():
                bars_dict[c['title']].append(rest)
            else:
                bars_dict[c['title']] = [rest]
        elif c['title'] in MediterraneanAndSeafood:
            if c['title'] in med_dict.keys():
                med_dict[c['title']].append(rest)
            else:
                med_dict[c['title']] = [rest]


international_dict['Africa'] = africa_dict
international_dict['Asia'] = asia_dict
international_dict['Latin America'] = latin_dict
international_dict['Europe'] = europe_dict
international_dict['Canada'] = canada_dict

dicts[categories[0]] = deli_dict
dicts[categories[1]] = coffee_dict
dicts[categories[2]] = deserts_dict
dicts[categories[3]] = american_dict
dicts[categories[4]] = healthy_dict
dicts[categories[5]] = international_dict
dicts[categories[6]] = bars_dict
dicts[categories[7]] = med_dict

write_json('test.json', dicts)

dicts2 = {'Deli': {'Sandwiches': [{'name': "Ernie's Market", 'rating': 5.0, 'price': '$', 'city': 'Oak Park', 'address': '8500 Capital St', 'phone': '(248) 541-9703'}, {'name': "Rocco's Italian Deli", 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '3627 Cass Ave', 'phone': '(313) 315-3033'}], 'Delis': [{'name': "Ernie's Market", 'rating': 5.0, 'price': '$', 'city': 'Oak Park', 'address': '8500 Capital St', 'phone': '(248) 541-9703'}, {'name': 'Beirut Bakery', 'rating': 5.0, 'price': '$', 'city': 'Redford', 'address': '25706 Schoolcraft', 'phone': '(313) 533-4422'}], 'Bakeries': [{'name': 'Beirut Bakery', 'rating': 5.0, 'price': '$', 'city': 'Redford', 'address': '25706 Schoolcraft', 'phone': '(313) 533-4422'}]}, 'Coffee and Tea': {'Coffee & Tea': [{'name': 'Qahwah House', 'rating': 5.0, 'price': '$$', 'city': 'Dearborn', 'address': '6655 Schaefer Rd', 'phone': '(313) 908-4521'}], 'Cafes': [{'name': 'The Narrow Way Cafe & Shop', 'rating': 5.0, 'price': '$', 'city': 'Detroit', 'address': '19331 Livernois Ave', 'phone': '(313) 397-7727'}, {'name': 'Kidcadia Play Café', 'rating': 5.0, 'price': 'Price not provided', 'city': 'Dearborn', 'address': '13939 Michigan Ave', 'phone': '(313) 771-9000'}]}, 'Deserts': {'Desserts': [{'name': 'Qahwah House', 'rating': 5.0, 'price': '$$', 'city': 'Dearborn', 'address': '6655 Schaefer Rd', 'phone': '(313) 908-4521'}, {'name': 'Bon Bon Bon', 'rating': 5.0, 'price': '$$', 'city': 'Hamtramck', 'address': '11360 Joseph Campau', 'phone': '(313) 316-1430'}], 'Chocolatiers & Shops': [{'name': 'Bon Bon Bon', 'rating': 5.0, 'price': '$$', 'city': 'Hamtramck', 'address': '11360 Joseph Campau', 'phone': '(313) 316-1430'}], 'Ice Cream & Frozen Yogurt': [{'name': 'Detroit Cookie Company', 'rating': 4.5, 'price': '$$', 'city': 'Ferndale', 'address': '23421 Woodward Ave', 'phone': '(248) 246-8060'}, {'name': 'The Proving Grounds', 'rating': 5.0, 'price': '$', 'city': 'Royal Oak', 'address': '417 S Washington Ave', 'phone': '(248) 716-0088'}]}, 'American': {'American (Traditional)': [{'name': 'Boostan Cafe', 'rating': 5.0, 'price': '$', 'city': 'Hamtramck', 'address': '3470 Holbrook Ave', 'phone': '(313) 456-8100'}], 'Middle Eastern': [{'name': 'Boostan Cafe', 'rating': 5.0, 'price': '$', 'city': 'Hamtramck', 'address': '3470 Holbrook Ave', 'phone': '(313) 456-8100'}, {'name': 'Sahara', 'rating': 4.5, 'price': '$$', 'city': 'Dearborn', 'address': '22815 Michigan Ave', 'phone': '(313) 406-5959'}], 'American (New)': [{'name': 'Chartreuse', 'rating': 4.5, 'price': '$$$', 'city': 'Detroit', 'address': '15 E Kirby St', 'phone': '(313) 818-3915'}, {'name': 'Dime Store', 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '719 Griswold St', 'phone': '(313) 962-9106'}], 'Pizza': [{'name': 'Michigan & Trumbull', 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '1441 W Elizabeth St', 'phone': '(313) 637-4992'}, {'name': 'Pie Sci', 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '5163 Trumbull Ave', 'phone': '(313) 818-0290'}], 'Breakfast & Brunch': [{'name': 'Dime Store', 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '719 Griswold St', 'phone': '(313) 962-9106'}], 'Diners': [{'name': 'Dime Store', 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '719 Griswold St', 'phone': '(313) 962-9106'}], 'Fast Food': [{'name': "Zo's Good Burger - Dearborn", 'rating': 4.5, 'price': '$', 'city': 'Dearborn', 'address': '14311 Michigan Ave', 'phone': '(313) 584-3114'}], 'Burgers': [{'name': "Zo's Good Burger - Dearborn", 'rating': 4.5, 'price': '$', 'city': 'Dearborn', 'address': '14311 Michigan Ave', 'phone': '(313) 584-3114'}]}, 'Healthy': {'Juice Bars & Smoothies': [{'name': 'Boostan Cafe', 'rating': 5.0, 'price': '$', 'city': 'Hamtramck', 'address': '3470 Holbrook Ave', 'phone': '(313) 456-8100'}], 'Salad': [{'name': 'Sahara', 'rating': 4.5, 'price': '$$', 'city': 'Dearborn', 'address': '22815 Michigan Ave', 'phone': '(313) 406-5959'}], 'Soup': [{'name': 'Sahara', 'rating': 4.5, 'price': '$$', 'city': 'Dearborn', 'address': '22815 Michigan Ave', 'phone': '(313) 406-5959'}], 'Vegan': [{'name': 'Unburger Grill', 'rating': 4.5, 'price': '$', 'city': 'Dearborn', 'address': '22018 Michigan Ave', 'phone': '(313) 633-0881'}], 'Health Markets': [{'name': 'The Sprout House Natural Foods Market', 'rating': 5.0, 'price': '$', 'city': 'Grosse Pointe Park', 'address': '15233 Kercheval St', 'phone': '(313) 331-3200'}]}, 'International': {'Africa': {'African': [{'name': 'Baobab Fare', 'rating': 5.0, 'price': '$$', 'city': 'Detroit', 'address': '6568 Woodward Ave', 'phone': '(313) 265-3093'}]}, 'Asia': {'Lebanese': [{'name': 'Beirut Bakery', 'rating': 5.0, 'price': '$', 'city': 'Redford', 'address': '25706 Schoolcraft', 'phone': '(313) 533-4422'}], 'Chinese': [{'name': "Tj's Shanghai Dumplings", 'rating': 5.0, 'price': 'Price not provided', 'city': 'Madison Heights', 'address': '27312 John R Rd', 'phone': '(248) 586-9588'}], 'Halal': [{'name': "Peepo's Subs & Shawarma", 'rating': 4.5, 'price': '$', 'city': 'Taylor', 'address': '10890 S Beech Daly Rd', 'phone': '(313) 299-9992'}, {'name': "Zo's Good Burger - Dearborn", 'rating': 4.5, 'price': '$', 'city': 'Dearborn', 'address': '14311 Michigan Ave', 'phone': '(313) 584-3114'}]}, 'Latin America': {'Tapas/Small Plates': [{'name': 'Chartreuse', 'rating': 4.5, 'price': '$$$', 'city': 'Detroit', 'address': '15 E Kirby St', 'phone': '(313) 818-3915'}], 'Mexican': [{'name': 'Taqueria El Rey', 'rating': 4.5, 'price': '$', 'city': 'Detroit', 'address': '4730 W Vernor Hwy', 'phone': '(313) 357-3094'}, {'name': 'Honey Bee La Colmena', 'rating': 4.5, 'price': '$', 'city': 'Detroit', 'address': '2443 Bagley St', 'phone': '(313) 237-0295'}], 'Tacos': [{'name': 'The Taco Stand Taqueria', 'rating': 4.5, 'price': '$', 'city': 'Allen Park', 'address': '5038 Allen Rd', 'phone': '(313) 724-6221'}]}, 'Europe': {'Italian': [{'name': "Rocco's Italian Deli", 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '3627 Cass Ave', 'phone': '(313) 315-3033'}, {'name': "Giovanni's Ristorante", 'rating': 4.5, 'price': '$$$', 'city': 'Detroit', 'address': '330 S Oakwood', 'phone': '(313) 841-0122'}, {'name': "Buddy's Pizza", 'rating': 4.5, 'price': '$$', 'city': 'Detroit', 'address': '17125 Conant St', 'phone': '(313) 892-9001'}, {'name': 'Oak & Reel', 'rating': 4.5, 'price': 'Price not provided', 'city': 'Detroit', 'address': '2921 E Grand Blvd', 'phone': '(313) 270-9600'}]}}, 'Bars': {}, 'Mediterranean and Seafood': {'Seafood': [{'name': 'Taqueria El Rey', 'rating': 4.5, 'price': '$', 'city': 'Detroit', 'address': '4730 W Vernor Hwy', 'phone': '(313) 357-3094'}, {'name': 'Andalus Mediterranian Grill', 'rating': 4.5, 'price': '$$', 'city': 'Dearborn', 'address': '3765 S Telegraph Rd', 'phone': '(313) 551-3356'}, {'name': 'Oak & Reel', 'rating': 4.5, 'price': 'Price not provided', 'city': 'Detroit', 'address': '2921 E Grand Blvd', 'phone': '(313) 270-9600'}], 'Mediterranean': [{'name': 'Andalus Mediterranian Grill', 'rating': 4.5, 'price': '$$', 'city': 'Dearborn', 'address': '3765 S Telegraph Rd', 'phone': '(313) 551-3356'}]}}

write_json('test2.json', dicts2)

class Tree():
    def __init__(self,root):
        self.root = root
        self.children = []
        self.Nodes = []
        
    def addNode(self,obj):
        self.children.append(obj)

    def show_tree(self):
        print(self)
    
    def getChildNode(self):
        i = 1
        for child in self.children:
            print(f"{i} - {child.data}")
            i +=1

class Node():
    def __init__(self, data):
        self.data = data
        self.children = []
        self.index = 0
    
    def addNode(self,obj):
        self.children.append(obj)
    
    def printChildNodes(self):
         i = 1
         for child in self.children:
             if self.children:
                print(f"{i} - {child.data}")
                i +=1
    def getChildNodes(self):
         return self.children

tree = Tree('Restaurants')
# for k in dicts:
#     tree.addNode(Node(k)) # Add categories


# Creating tree with recursion

def create_tree(dicts, tree):
    x = tree
    if isinstance(dicts, list) and 'name' in dicts[0]:
        for i in dicts:
           tree.addNode(Node(i))
        return tree
    else:
        counter = 0
        for z in dicts.keys():
            tree.addNode(Node(z))
            counter += 1
            x = create_tree(dicts[z], tree.children[counter-1])
            
        return x

create_tree(dicts, tree)

# Instantiating  subcategories without recursion
 
# counter = 0
# for k in dicts:
#     tree.addNode(Node(k)) # Add categories
#     counter2 = 0
#     for i in dicts[k]:
#         counter3 = 0
#         if i in International:
#             tree.children[counter].addNode(Node(i)) #Add International subcategories (American)
#             for z in dicts[k][i]: 
#                 tree.children[counter].children[counter2].addNode(Node(z)) #Add International subsubcategories (Burguer)
#                 for m in dicts[k][i][z]:
#                     tree.children[counter].children[counter2].children[counter3].addNode(Node(m)) # Add International Restaurants
#                 counter3 += 1
#         else:
#             tree.children[counter].addNode(Node(i)) #Add subcategories
#             for y in dicts[k][i]: # Add restaurants  
#                 tree.children[counter].children[counter2].addNode(Node(y))
#         counter2 += 1
#     counter += 1
    

# if __name__ == "__main__":

#     while True:
#         print('Hi, welcome to the restaurant curator!\n') 
#         print('What type of food would you like to eat? \n') 
#         tree.getChildNode()
#         value = input('Enter a number for the category of your choice, or "exit" to quit: ')
        
#         if value.lower() == 'exit':
#             print('\nSee you next time!\n')
#             break
#         elif value.isnumeric() == False:
#             print('\nYou need to insert a number. \n')
#         else:
#             value = int(value)
#             tree.children[value-1].printChildNodes()

#             value2 = input(f'Which of these subcategories you like the most for {tree.children[value-1].data} category? ')

#             if value2.lower() == 'exit':
#                 print('\nSee you next time!\n')
#                 break
#             elif value2.isnumeric() == False:
#                 print('\nYou need to insert a number. \n')

#             elif value == 6:
#                 value2 = int(value2)
#                 tree.children[value-1].children[value2-1].printChildNodes()
#                 value3 = input(f'Which type of restaurant from {tree.children[value-1].children[value2-1].data} cuisine are you up to? ')
                
#                 if value3.lower() == 'exit':
#                     print('\nSee you next time!\n')
#                     break
#                 elif value3.isnumeric() == False:
#                     print('\nYou need to insert a number. \n')
                
#                 else:
#                     value3 = int(value3)
#                     print(f"Great! Here is the list of {tree.children[value-1].children[value2-1].children[value3-1].data} restaurants in Michigan that I recommend based on your answers: \n")
#                     rest = tree.children[value-1].children[value2-1].children[value3-1].getChildNodes()
#                     for i in rest:
#                         rest_name = i.data['name']
#                         rest_rating = i.data['rating']
#                         rest_price = i.data['price']
#                         rest_city = i.data['city']
#                         rest_address = i.data['address']
#                         rest_phone = i.data['phone']
#                         print(f"Restaurant: {rest_name}")
#                         print('----------------------------')
#                         print(f"-> Rating: {rest_rating}")
#                         print(f"-> Price: {rest_price}")
#                         print(f"-> City: {rest_city}")
#                         print(f"-> Address: {rest_address}")
#                         print(f"-> Phone: {rest_phone}")
#                         print('\n#######################################\n')

#                     value4 = input('Do you want to search again? ')
#                     if value4.lower() != 'yes':
#                         print('Great! Hope you enjoy my recommendation!')
#                         break
#                     else:
#                         continue
#             else:
#                 value2 = int(value2)
#                 print(f"Great! Here is the list of {tree.children[value-1].children[value2-1].data} restaurants in Michigan that I recommend based on your answers: ")
#                 rest = tree.children[value-1].children[value2-1].getChildNodes()
#                 for i in rest:
#                     rest_name = i.data['name']
#                     rest_rating = i.data['rating']
#                     rest_price = i.data['price']
#                     rest_city = i.data['city']
#                     rest_address = i.data['address']
#                     rest_phone = i.data['phone']
#                     print(f"Restaurant: {rest_name}")
#                     print('----------------------------')
#                     print(f"-> Rating: {rest_rating}")
#                     print(f"-> Price: {rest_price}")
#                     print(f"-> City: {rest_city}")
#                     print(f"-> Address: {rest_address}")
#                     print(f"-> Phone: {rest_phone}")
#                     print('\n#######################################\n')
            
#                 value4 = input('Do you want to search again? ')
#                 if value4.lower() != 'yes':
#                     print('Great! Hope you enjoy my recommendation!')
#                     break
#                 else:
#                     continue