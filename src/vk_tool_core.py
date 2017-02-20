# -*- coding: utf-8 -*-

"""
    Author: Eugene Tolpygo (eugenetolpygo@gmail.com)
    License: Apache-2.0, see LICENSE file for details
    Creation date: 16.02.2017

    Module vk_tool_core.py is base for all other vk_tools scripts. it's used 
    vk api methods (https://vk.com/dev/methods) to get some data from vk social 
    network (www.vk.com).
"""

import os
import re
import requests
import urllib
import time 


vk_api_version = "5.62"
my_app_id = "5879335"
access_token_url = ("https://oauth.vk.com/authorize?"
                    "client_id=%s&"
                    "display=page&"
                    "redirect_uri=https://oauth.vk.com/blank.html&"
                    "scope=photos,messages&"
                    "response_type=token&"
                    "v=%s&"
                    "state=123456" % (my_app_id, vk_api_version))

base_api_url = ("https://api.vk.com/method/METHOD_NAME?"
                "PARAMETERS&"
                "access_token=ACCESS_TOKEN&"
                "v=%s" % (vk_api_version))

def error_handle(json):
    """
        Handle errors. All error doc - https://vk.com/dev/errors

        Args:
            json: json with error message and error_code. 
    """
    print(json['error']['error_msg'])
    error_code = json['error']['error_code']

    if error_code == 6: # Too much requests per second
        print("wait 10 second")
        time.sleep(10)
    else:
        exit(1)

def reg_access_token():
    """
        Print url for getting access token. User must open url, accept term and 
        copy request url or only access token parameter to script's console. Access token
        is stored in access_token.txt file. VK api works with oauth 2.0 protocol. For more
        information - https://vk.com/dev/access_token
    """
    access_token = input("%s\nopen url in browser and copy access token or url to console:"
                         % (access_token_url))

    with open("access_token.txt", 'w') as f:
        if "access_token=" in access_token:
            f.write(re.search(r"access_token=\w+", access_token).group(0)[13:])
        else:
            f.write(access_token)

def get_access_token():
    """
        Returns:
            access token from access_token.txt file. Call reg_access_token() if file 
            is not found.
    """
    if os.path.isfile("access_token.txt"):
        with open("access_token.txt", 'r') as f:
            return f.read()
    else:
        print("can't find access token")
        reg_access_token()
        return get_access_token()

def make_vk_request(access_token, method_name, parameters):
    """
        Main method for all vk_tools requests to vk api. Call error_handle method
        if json's response has 'error' object.

        Args:
            access_token: access token to vk api.
            method_name: name of vk api method. All vk api method - https://vk.com/dev/methods
            parameters: parameters of vk api method.

        Returns:
            Json object which corresponds to a vk api method
    """
    request_str = re.sub('METHOD_NAME', method_name, base_api_url)
    request_str = re.sub('ACCESS_TOKEN', access_token, request_str)
    request_str = re.sub('PARAMETERS', urllib.parse.urlencode(parameters), request_str)

    response = requests.get(request_str)

    if 'error' in response.json():
        error_handle(response.json())
        return make_vk_request(access_token, method_name, parameters) 

    return response.json()