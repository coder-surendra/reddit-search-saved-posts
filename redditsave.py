import re
import requests

CLIENT_ID = ''
SECRET_KEY = ''
username = ''
password = ''

def getHeaders():

	auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

	data = {
		'grant_type' : 'password',
		'username' : username,
		'password': password
	}
	headers = {'User-Agent': 'MyAPI/0.0.1'}
	headers['User-Agent'] = 'MyAPI/0.0.1' 
	
	res = requests.post(
		'https://www.reddit.com/api/v1/access_token',
		auth=auth,data=data,headers=headers
	)
	TOKEN = res.json()['access_token']

	headers["Authorization"] = f'bearer {TOKEN}'

	return headers

# ---end of getHeaders ---


def searchText( string ,headers):

	redditURL = 'https://www.reddit.com'
	acceptableResult = ['y',"Y",'']
	after = ''
	userInput = 'y'
	while(userInput in acceptableResult):
		print(' ')
		print(' ')
		print('################ LOADING NEW SET OF RESULTS ################')
		print(' ')
		print(' ')
		
		if(after == None):
			print('SORRY, we have reached the end')
			break
		response = requests.get(
			"https://oauth.reddit.com/user/"+username+"/saved", 
			headers = headers, 
			params = {
				'limit' : '100',
				'after' : after
			}
		)

		post = response.json()['data']

		after = post['after']
		
		for d in post['children']:

			kind = d['kind']
			if( kind == 't1'):
				# its comment 
				if( re.search(string,d['data']['link_title'],re.IGNORECASE) or re.search(string, d['data']['body'], re.IGNORECASE)):
					print('\n---------------------')
					print('Match found : COMMENT')
					print('---------------------')
					print('Title : ',d['data']['link_title'])
					print('PermaLink : ', redditURL + d['data']['permalink'])
					
					if(len(d['data']['body']) >= 250):
						print('Comment is too long !!! ')
						print("Do you still want to see it ?")
						print("Press 'y' to yes")
						
						userInput = input()
						if( userInput == 'y' or userInput == 'Y' ):
							print('Comment : ')
							print(d['data']['body'])
					else:
						# print('Comment : ',d['data']['body_html'])
						print('Comment : ',d['data']['body'])
						
					print('--------------------------')
					print("want to continue searching?")
					print("Press ENTER to continue ,or 'X' to STOP") 
					
					userInput = input()
					
					
			elif( kind == 't3'):
				# its a post
				
				if( re.search(string, d['data']['selftext'], re.IGNORECASE) or re.search( string, d['data']['title'], re.IGNORECASE) ) :
					print('\n------------------')
					print('Match found : POST')
					print('------------------')
					print('Title : ',d['data']['title'])
					print('PermaLink : ', redditURL + d['data']['permalink'])

					if( len(d['data']['selftext']) >= 250 ):
						print('Body is too big !!! ')
						print("Still display?")
						print("Press 'y' for yes")
						userInput = input()
						if( userInput == 'y' or userInput == 'Y'):
							print('Body : ')
							print(d['data']['selftext'])
					else:
						if( len(d['data']['selftext']) == 0):
							print('Body : null' )
						else:
							print('Body : ', d['data']['selftext'])
						
					print('-----------------------------')
					print("Want to continue searching?")
					print("Press ENTER to continue ,or 'X' to STOP") 
					userInput = input()

			else:
				pass


			if(userInput  not in  acceptableResult):
				break

		# end of for - loop

	# end of while - loop

# end of searchText 


def redditSeachInSaved():
	

	headers = getHeaders()   

	userInput = input('Enter text to search : ')
	
	print("Finding '" + userInput + "'")
	searchText(userInput, headers)
	
	print(' == Hope this tool helped you == ')

	
redditSeachInSaved()


