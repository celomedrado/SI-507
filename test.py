# from datetime import datetime

# my_string = '2019-10-31'

# # Create date object in given time format yyyy-mm-dd
# my_date = datetime.strptime(my_string, "%Y-%m-%d")

# print(my_date)
# print('Type: ',type(my_date))

# print('Month: ', my_date.month) # To Get month from date
# print('Year: ', my_date.year) # To Get month from year


# def printParents(node, adj, parent):

# 	# current node is Root, thus, has no parent
# 	if (parent == 0):
# 		print(node, "->Root")
# 	else:
# 		print(node, "->", parent)
		
# 	# Using DFS
# 	for cur in adj[node]:
# 		if (cur != parent):
# 			printParents(cur, adj, node)

# # Function to print the children of each node
# def printChildren(Root, adj):

# 	# Queue for the BFS
# 	q = []
	
# 	# pushing the root
# 	q.append(Root)
	
# 	# visit array to keep track of nodes that have been
# 	# visited
# 	vis = [0]*len(adj)
	
# 	# BFS
# 	while (len(q) > 0):
# 		node = q[0]
# 		q.pop(0)
# 		vis[node] = 1
# 		print(node, "-> ", end=" ")

# 		for cur in adj[node]:
# 			if (vis[cur] == 0):
# 				print(cur, " ", end=" ")
# 				q.append(cur)
# 		print("\n")

# # Function to print the leaf nodes
# def printLeafNodes(Root, adj):

# 	# Leaf nodes have only one edge and are not the root
# 	for i in range(0, len(adj)):
# 		if (len(adj[i]) == 1 and i != Root):
# 			print(i, end=" ")
# 	print("\n")

# # Function to print the degrees of each node
# def printDegrees(Root, adj):

# 	for i in range(1, len(adj)):
# 		print(i, ": ", end=" ")
		
# 		# Root has no parent, thus, its degree is equal to
# 		# the edges it is connected to
# 		if (i == Root):
# 			print(len(adj[i]))
# 		else:
# 			print(len(adj[i])-1)

# # Driver code

# # Number of nodes
# N = 7
# Root = 1

# # Adjacency list to store the tree
# adj = []
# for i in range(0, N+1):
# 	adj.append([])
	
# # Creating the tree
# adj[1].append(2)
# adj[2].append(1)

# adj[1].append(3)
# adj[3].append(1)

# adj[1].append(4)
# adj[4].append(1)

# adj[2].append(5)
# adj[5].append(2)

# adj[2].append(6)
# adj[6].append(2)

# adj[4].append(7)
# adj[7].append(4)

# # Printing the parents of each node
# print("The parents of each node are:")
# printParents(Root, adj, 0)

# # Printing the children of each node
# print("The children of each node are:")
# printChildren(Root, adj)

# # Printing the leaf nodes in the tree
# print("The leaf nodes of the tree are:")
# printLeafNodes(Root, adj)

# # Printing the degrees of each node
# print("The degrees of each node are:")
# printDegrees(Root, adj)

# print(adj)

class Tree():
    def __init__(self,root):
        self.root = root
        self.children = []
    def addNode(self,obj):
        self.children.append(obj)

class Node():
    def __init__(self, data):
        self.data = data
        self.children = []
    
    def addNode(self,obj):
        self.children.append(obj)

FunCorp =  Tree('Head Honcho') # Create a tree and add root data.
print(FunCorp.root) # ask the Tree for it's root.
#>> Head Honcho
# Add children to root:
FunCorp.addNode(Node('VP of Stuff'))
FunCorp.addNode(Node('VP of Shenanigans'))
FunCorp.addNode(Node('VP of Hootenanny'))


# url = 'https://api.themoviedb.org/3/authentication/token/new?api_key=7f9c917ba6b080f5484d0655667ac04d'

# api_token = '7f9c917ba6b080f5484d0655667ac04d'

# request_token = get_json_file(url)['request_token']

# auth_url = 'https://www.themoviedb.org/authenticate/' + request_token



# url_page_1 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=1&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_2 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=2&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_3 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=3&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_4 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=4&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_5 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=5&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_6 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=6&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_7 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=7&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_8 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=8&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_9 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=9&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'
# url_page_10 = 'https://api.themoviedb.org/3/discover/movie?api_key=' + api_token + '&sort_by=vote_average.desc&page=10&primary_release_date.gte=2009-01-01&primary_release_date.lte=2021-04-01&vote_count.gte=1000'






# movies = get_json_file(url_page_1)['results']
# movies.extend(get_json_file(url_page_2)['results'])
# movies.extend(get_json_file(url_page_3)['results'])
# movies.extend(get_json_file(url_page_4)['results'])
# movies.extend(get_json_file(url_page_5)['results'])
# movies.extend(get_json_file(url_page_5)['results'])
# movies.extend(get_json_file(url_page_6)['results'])
# movies.extend(get_json_file(url_page_7)['results'])
# movies.extend(get_json_file(url_page_8)['results'])
# movies.extend(get_json_file(url_page_9)['results'])
# movies.extend(get_json_file(url_page_10)['results'])

# print(len(movies))


# for i in movies:
#     print(f"{i['original_title']} {i['vote_average']} {i['vote_count']}")


# oscars = read_csv_to_dicts('oscarnominees.csv')

# for i in oscars:
#     i['Year'] = int(i['Year'])

# winners = []

# for i in oscars:
#     if i['Year'] > 2010 and i['Award'] == 'Picture' and i['Winner'] == 'Y':
#         winners.append({'Title': i['Title'], 'Year': i['Year']})

# movies = []

# for i in winners:
#     query = i['Title']
#     url_page_1 = 'https://api.themoviedb.org/3/search/movie?api_key=' + api_token + '&query=' + query
#     movies_dict = (get_json_file(url_page_1)['results'])
#     if len(movies_dict) > 1:
#         for o in oscars:
#             for m in movies_dict:
#                 year = datetime.strptime(m['release_date'], '%Y-%m-%d')
#                 year = year.year
#                 print(year)
#                 # if o['Title'] == m['original_title'] and o['Year'] == int(year):
#                 #     movies.append(m)


# for i in movies:
#     print(f"{i}\n")

# new_list = []

# for i in oscars:
#     for m in movies:
#         if i['Title'].lower() == m['original_title'].lower():
#             print(m['original_title'])

# print(new_list)

dicts ={}
marcelove = 'aaaa'
if dicts['marcelo']:
    dicts['marcelo'].append(marcelove)
else:
    dicts['marcelo'] = 'oiii'