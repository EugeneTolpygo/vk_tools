import os
import re
import requests
import urllib
import time 

vk_api_version = "5.62"
my_app_id = "5879335"
access_token_url = "https://oauth.vk.com/authorize?client_id=" + my_app_id + "&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,messages&response_type=token&v=" + vk_api_version + "&state=123456"
base_api_url = "https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=" + vk_api_version

def error_handle(json):
	print(json['error']['error_msg'])
	error_code = json['error']['error_code']
	
	if error_code == 6:
		print("wait 10 second")
		time.sleep(10)

def reg_access_token():
	access_token = input(access_token_url + "\nopen url in browser and copy access token or url to console:")
	with open("access_token.txt", 'w') as f:
		if ("access_token="):
			f.write(re.search(r"access_token=\w+", access_token).group(0)[13:])
		else:
			f.write(access_token)

def get_access_token(repeat = False):
	if os.path.isfile("access_token.txt") and not repeat:
		return open("access_token.txt", 'r').readlines()[0]
	else:
		print("can't find access token")
		reg_access_token()
		return get_access_token()

def make_vk_request(access_token, method_name, parameters):
	request_str = re.sub('METHOD_NAME', method_name, base_api_url)
	request_str = re.sub('ACCESS_TOKEN', access_token, request_str)
	request_str = re.sub('PARAMETERS', urllib.parse.urlencode(parameters), request_str)

	response = requests.get(request_str)

	if 'error' in response.json():
		error_handle(response.json())
		return make_vk_request(access_token, method_name, parameters) 

	return response.json()