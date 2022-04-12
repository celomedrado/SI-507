
from sys import intern
from nbformat import write
import requests
import json
from urllib.request import urlopen
import csv
from datetime import datetime
from http import client
import secrets

from torch import numel

CACHE_FILENAME = "yelp_cache.json"
CACHE_DICT = {}

yelp_key = secrets.YELP_API_KEY
# client_secret = secrets.TWITTER_API_SECRET

# access_token = secrets.TWITTER_ACCESS_TOKEN
# access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

# oauth = OAuth1(client_key,
#             client_secret=client_secret,
#             resource_owner_key=access_token,
#             resource_owner_secret=access_token_secret)

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


def read_csv(filepath, encoding='ISO-8859-1', newline='', delimiter=','):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data

def read_csv_to_dicts(filepath, encoding='ISO-8859-1', newline='', delimiter=','):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

        return data

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
        print("cache hit!", request_key)
        return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
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


# print(results[0])

# print(len(results))
# print(type(results))

# for i in results[0].keys():
#     print(i)

# categories = []
# for i in results:
#     for z in i['categories']:
#         if z['title'] not in categories:
#             categories.append(z['title'])



# print(len(categories))

restaurants = []

for i in results:

    try:
        restaurants.append({
            'name': i['name'],
            'categories': i['categories'],
            'rating': i['rating'],
            'price': i['price']
        })
    except:
        restaurants.append({
            'name': i['name'],
            'categories': i['categories'],
            'rating': i['rating']
        })


categories = ['Deli', 'Coffee and Tea', 'Deserts', 'American', 'Healthy', 
'International', 'Bars', 'Mediterranean and Seafood']

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

# cat_file = open('Categories.txt', 'r')

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
                    'price': z['[price'],
                }
        except:
            rest = {
                'name': z['name'],
                'rating': z['rating'],
                'price': 'Price not provided',
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
        elif c['title'] in MediterraneanAndSeafood:
            if c['title'] in med_dict.keys():
                med_dict[c['title']].append(rest)
            else:
                med_dict[c['title']] = [rest]


international_dict['Africa'] = africa_dict
international_dict['Asia'] = asia_dict
international_dict['Latin America'] = latin_dict
international_dict['Europe'] = europe_dict

dicts[categories[0]] = deli_dict
dicts[categories[1]] = coffee_dict
dicts[categories[2]] = deserts_dict
dicts[categories[3]] = american_dict
dicts[categories[4]] = healthy_dict
dicts[categories[5]] = international_dict
dicts[categories[6]] = bars_dict
dicts[categories[7]] = med_dict


# print(len(dicts))




write_json('test.json', dicts)

class Tree():
    def __init__(self,root):
        self.root = root
        self.children = []
        self.Nodes = []
        
    def addNode(self,obj):
        self.children.append(obj)

    def show_tree(self):
        print(self)

    def getAllNodes(self):
        self.Nodes.append(self.root)
        for child in self.children:
            self.Nodes.append(child.data)
        for child in self.children:
            if child.getChildNodes(self.Nodes) != None:
                child.getChildNodes(self.Nodes)
        print(*self.Nodes, sep = "\n")
        print('Tree Size:' + str(len(self.Nodes)))

class Node():
    def __init__(self, data):
        self.data = data
        self.children = []
        self.index = 0
    
    def addNode(self,obj):
        self.children.append(obj)
    
    def getChildNodes(self,Tree):
        for child in self.children:
            if child.children:
                child.getChildNodes(Tree)
                Tree.append(child.data)
            else:
                Tree.append(child.data)


tree = Tree('Restaurants')

# Instantiating  subcategories
 
counter = 0
for k in dicts:
    tree.addNode(Node(k)) # Add categories
    counter2 = 0
    for i in dicts[k]:
        counter3 = 0
        if i in International:
            tree.children[counter].addNode(Node(i)) #Add International subcategories (American)
            for z in dicts[k][i]: 
                tree.children[counter].children[counter2].addNode(Node(z)) #Add International subsubcategories (Burguer)
                for m in dicts[k][i][z]:
                    tree.children[counter].children[counter2].children[counter3].addNode(Node(m)) # Add International Restaurants
            counter3 += 1
        else:
            tree.children[counter].addNode(Node(i)) #Add subcategories
            for y in dicts[k][i]: # Add restaurants  
                tree.children[counter].children[counter2].addNode(Node(y))
        counter2 += 1
    counter += 1
    
## Test
# print(tree.children[0].data) # Deli
# print(tree.children[1].data) # Coffee And Tea
# print(tree.children[2].data) # Deserts
# print(tree.children[3].data) # American
# print(tree.children[4].data) # Healthy
# print(tree.children[5].data) # International
# print(tree.children[6].data) # Bars
# print(tree.children[7].data) # Mediterranean and seafood


# print(tree.children[0].children[3].data) # Bagels
# print(tree.children[5].children[0].data) # Africa
# print(tree.children[5].children[1].data) # Asia
# print(tree.children[5].children[2].data) # Latin America
# print(tree.children[5].children[3].data) # Europe
# print(tree.children[5].children[0].children[1].data) # Morocan
# print(tree.children[5].children[1].children[0].data) # Lebanese
# print(tree.children[5].children[2].children[0].data) # Tapas/Small Plates
# print(tree.children[5].children[3].children[0].data) # Italian
# print(tree.children[5].children[3].children[0].children[0].data) # Italian


if __name__ == "__main__":

    

    # value2 = "+".join(value.split(' '))

    while True:
        print('Hi, welcome to the restaurant curator!\n') 
        print('What type of food would you like to eat? \n') 

        # value = input('What type of food would you like to eat? ')
        tree.getAllNodes(tree[0])
        
        # if isinstance(value, str):
        #     if value.lower() == 'exit':
        #         print('\nSee you next time!\n')
        #         break
        #     else:
                

                

        #         for i in media_list:
        #             if i['wrapperType'] == 'track':
        #                 if i['kind'] == 'song':
        #                     media.append(Song(json=i))
        #                 elif i['kind'] == 'feature-movie':
        #                     media.append(Movie(json=i))
        #             else:
        #                 media.append(Media(json=i))

        #         categorized_list = []

        #         n = 0
        #         s = 0
        #         print(f"\nSONGS")
        #         for item in media:
        #             if isinstance(item, Song):
        #                 n += 1
        #                 s += 1
        #                 print(f"{n} {item.info()}")
        #                 categorized_list.append(item)
        #         if s == 0:
        #             print('There are no songs related to your search.')

        #         f = 0
        #         print(f"\nMOVIES")
        #         for item in media:
        #             if isinstance(item, Movie):
        #                 n += 1
        #                 f += 1
        #                 print(f"{n} {item.info()}")
        #                 categorized_list.append(item)
        #         if f == 0:
        #             print('There are no movies related to your search.')

        #         m = 0
        #         print(f"\nOTHER MEDIA")
        #         for item in media:
        #             if isinstance(item, Media) and not isinstance(item, Song) and not isinstance(item, Movie):
        #                 n += 1
        #                 m += 1
        #                 print(f"{n} {item.info()}")
        #                 categorized_list.append(item)
        #         if m == 0:
        #             print('There are no other media related to your search.\n')

        #         if n == 0:
        #             message = 'Enter a search term, or "exit" to quit: '
        #         else:
        #             message = 'Enter a number for more info, or another search term, or exit: '
                
        #         while True:
        #             value = input(message)
        #             value2 = "+".join(value.split(' '))
                        
        #             if value2.isnumeric():
        #                 integer = int(value2)
        #                 if n != 0 and integer > n:
        #                     print('\nEnter a number within the interval of the list.\n')
        #                     continue
        #                 elif n == 0:
        #                     print('\nYour search had no results. Enter a search term, or "exit" to quit.\n')
        #                     continue
        #                 else:
        #                     for i in range(len(categorized_list)):
        #                         if int(i) == integer - 1:
        #                             print(integer)
        #                             url_open = categorized_list[i].url
        #                             print(f"Launching\n{url_open}\nin web browser...")
        #                             webbrowser.open_new_tab(f"{url_open}")
        #             elif isinstance(value2, str):
        #                 break
        #             else:
        #                 continue





