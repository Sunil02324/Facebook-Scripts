import requests # pip install requests
import json
import facebook
from prettytable import PrettyTable
from collections import Counter


#INPUT YOUR ACCESS_TOKEN
ACCESS_TOKEN = '' #Insert access token here.

base_url = 'https://graph.facebook.com/me'
g = facebook.GraphAPI(ACCESS_TOKEN)

#PRINTING YOUR FRIEND ALL "favorite_teams"
fs = g.get_object("me/friends")
for f in fs['data']:
	#print f
	#print f['name'],f['id']
	print f['name']
	for x in g.get_object(f['id'])['favorite_teams']:
		print x['name']


#SEACHING TOP 10 PAGE ON INPUTTING PAGE NAME AND OUTPUT AS PAGE ID OF FACEBOOK 
x= g.request('search', {'q' : 'pepsi', 'type' : 'page', 'limit' : 10})['data'][0]['id']



#GET ALL STATUS POST ON PARTICULAR PAGE(X=PAGE ID)
for x1 in g.get_connections(x, 'feed')['data']:
	print x1
	for x2 in x1:
	 	print x2
	 	if(x2['type']=='status'):
		 	x2['message']





# Analyze all likes from friendships for frequency
friends_likes = Counter([like['name']
                         for friend in likes 
                           for like in likes[friend]
                               if like.get('name')])

pt = PrettyTable(field_names=['Name', 'Freq'])
pt.align['Name'], pt.align['Freq'] = 'l', 'r'
[ pt.add_row(fl) for fl in friends_likes.most_common(10) ]

print 'Top 10 likes amongst friends'
print pt

# Analyze all like categories by frequency

friends_likes_categories = Counter([like['category'] 
                                    for friend in likes 
                                      for like in likes[friend]])

pt = PrettyTable(field_names=['Category', 'Freq'])
pt.align['Category'], pt.align['Freq'] = 'l', 'r'
[ pt.add_row(flc) for flc in friends_likes_categories.most_common(10) ]

print "Top 10 like categories for friends"
print pt