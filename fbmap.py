# MAPS PAGES UPTO 3 LEVELS FROM USER LEVEL
# Multiple nesting of for-loops is bad programming

import requests	
import json
import treelib

from treelib import Tree

f = open("pages.txt","w+")					# we will bewriting into file for test purposes
url_string1 = 'https://graph.facebook.com/'			# all requests go to the Facebook Graph API
url_string2 = '/likes?access_token='
user_id ='me'
access_token =''#Insert access token here.
 
tree = Tree()
r0 = requests.get(url_string1 + user_id + url_string2 + access_token)
f.write(r0.text)
tree.create_node(user_id , "user_id")
dictionary = r0.json()

for parent_page in dictionary['data']:
	parent_page_id = parent_page['id']
	print "Parent page ID: " + parent_page_id
	tree.create_node(parent_page_id , "parent_page_id: " + parent_page['id'] , parent = "user_id")
	r1 = requests.get(url_string1 + parent_page_id + url_string2 + access_token)
	dictionary = r1.json()

	for page in dictionary['data']:	
		try:		
			page_id = (page['id'])
			print "Page ID: " + page_id
			tree.create_node(page_id , "page_id: " + page['id'] , parent = "parent_page_id: " + parent_page['id'])
			r2 = requests.get(url_string1 + page_id + url_string2 + access_token)
			dictionary = r2.json()
		except:
			print "Exception at level 2 ..."	# exceptions in case of request failiure and  multiple nodes
			continue		

		for in_page in dictionary['data']:
			try:
				in_page_id = (in_page['id'])
				print "Leaf Page ID: " + in_page_id
				tree.create_node(in_page_id ,"in_page_id: " + in_page['id'] , parent = "page_id: " + page['id']) 
				r3 = requests.get(url_string1 + in_page_id + url_string2 + access_token)			
			except:
				print "Exception at level 3 ..."
				continue	
			f.write(r3.text)
		f.write(r2.text)
	f.write(r1.text)	

tree.show()
f.close()


###############################################################################################################################################################################################
# in case of token expiration
# url_new = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=<CLIENT ID KEY>& client_secret=<CLIENT SECRET KEY>&fb_exchange_token=<SHORT LIVED TOKEN KEY>'
# r = requests.get(url_new)