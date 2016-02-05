from facepy import GraphAPI
import json;
import csv,os, sys, urllib,urllib2, datetime,requests,json,solr,time
from datetime import date
from datetime import datetime
from json import loads
from urllib2 import urlopen
from optparse import OptionParser
from pprint import pprint

# Command Line Arguments Parser
cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-T", "--OAuthToken", 		type="string", 	action="store", dest="oauth_access_token", help="Facebook OAuth Access Token (You can get your on here https://developers.facebook.com/tools/explorer/) (optional)")
cmd_parser.add_option("-F", "--FacebookObjectId", 	type="string", 	action="store", dest="facebook_object_id", help="Facebook Object Id. You can find more about it here https://developers.facebook.com/docs/reference/api/")
cmd_parser.add_option("-L", "--PageSize", 			type="int", 	action="store", dest="page_size", help="Pagination size (1-999) (optional)", default=500)
cmd_parser.add_option("-O", "--Offset", 			type="int", 	action="store", dest="offset", help="Pagination offset (optional)",default=0)
cmd_parser.add_option("-S", "--Solr", 				type="string", 	action="store", dest="solr_address", help="Solr Address (optional)")

(cmd_options, cmd_args) = cmd_parser.parse_args()

if not (cmd_options.facebook_object_id or cmd_options.oauth_access_token):
    cmd_parser.print_help()
    sys.exit(3)

# Program parameters
_page_size 			= cmd_options.page_size
_start_offset 		= cmd_options.offset
_access_token 		= cmd_options.oauth_access_token
_facebook_object_id = cmd_options.facebook_object_id
_solr_address 		= cmd_options.solr_address

# global variables
_total = 0
_startTime = datetime.now()

def buildSelectStatement(objectId,limit,offset):
	selectStatement = "SELECT id, username, fromid, likes ,text, time FROM comment "
	selectStatement += " WHERE object_id IN (" +str(objectId)+ ")"
	selectStatement += " ORDER BY id ASC LIMIT " + str(limit)
	selectStatement += " OFFSET " + str(offset)

	return selectStatement

def sendDocumentToSolr(comment):
	dateTimeFormat = '%Y-%m-%dT%H:%M:%SZ'
	created_time = datetime.fromtimestamp(long(comment['time'])).strftime(dateTimeFormat)

	try:
		print "send it to solr"
		
		s.add(
			in_reply_to_object_id=objectId,
			user_id=comment['fromid'],
			name=comment['username'],
			like_count=comment['likes'],
			id=comment['id'],
			created_at=created_time,
			text_length_i=len(comment['text']),
			text=comment['text']);

	except solr.core.SolrException as solrerror:
		print "OUCH !! Something bad happened Larry!" 
		print solrerror


def printComment(comment):
	print "id: " 		+ comment['id']
	print "user id: " 	+ str(comment['fromid'])
	print "text: " 		+ comment['text']
	print "timestamp: " +  str(datetime.fromtimestamp(long(comment['time'])))
	print "likes: " 	+ str(comment['likes'])
	print "--------------------------------------------"



def loadFacebookCommentsFromObjectId(objectId,limit=999,offset=0):
	print "- objectId : " + str(objectId)
	print "- limit : " + str(limit) 
	print "- offset : " + str(offset)
	
	#execute query on facebook graph api
	response = graph.fql(buildSelectStatement(objectId,limit,offset))

	#check if there is any data	
	if(response.has_key('data')):
		comments = response['data']	

		#check if there is any comment
		if len(comments) > 0:

			#iterate over comments
			for comment in comments:
				global _total
				_total += + 1

				#just for debug
				print str(_total)
				
				printComment(comment)

				if(_solr_address != None):
					#send it to solr
					sendDocumentToSolr(comment)
			
			next_offset = offset + _page_size
			print "Loading next page..."
			loadFacebookCommentsFromObjectId(objectId,_page_size,next_offset)

	#finished		
	global _startTime

	now = datetime.now()		
	
	print "\nFINISHED ################################\n"
	print "Start at " + _startTime.ctime()
	print "Finished at " + now.ctime()
	print "Total of collected comments : " + str(_total)

# Initialize the Graph API with a valid access token (optional, but will allow you to do all sorts of fun stuff).
graph = GraphAPI(_access_token)

# create a connection to a solr server
#"http://pattie.fe.up.pt/solr/facebook"

if(_solr_address != None):
	s = solr.SolrConnection(_solr_address)

#Start collecting comments
loadFacebookCommentsFromObjectId(_facebook_object_id,_page_size,_start_offset)