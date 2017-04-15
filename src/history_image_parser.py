import os
import vk_tool_core
import urllib
import shutil
import sys

def get_dialogs(access_token, offset = 0, count = 200, return_count = False):
	method_name = "messages.getDialogs"
	parameters = {
				"offset": offset,
				"count": count,
	}
	json_data = vk_tool_core.make_vk_request(access_token, method_name, parameters)

	if return_count:
		return json_data['response']['count']

	return json_data['response']['items']

def get_history_images(access_token, dialog_id, count=200):
	method_name = "messages.getHistoryAttachments"
	parameters = {
			"peer_id": dialog_id,
			"count": count,
			"media_type": "photo"
	}

	json_data = vk_tool_core.make_vk_request(access_token, method_name, parameters)
	return json_data['response']['items']

def save_image(access_token, user_id):
	images_json = get_history_images(access_token, user_id)
			
	for index, image in enumerate(images_json):
		print("==> copy image №" + str(index))
		image_key = find_max_image_key(image['attachment']['photo'].keys())
		image_url = image['attachment']['photo'][image_key]
		image_name = image_url[image_url.rfind('/'):]
		try:
			urllib.request.urlretrieve(image_url, user_id + "/" + image_name)
		except:
			print("can't download image - " + image_url)
			continue

def find_max_image_key(keys):
	image_keys = [key for key in keys if "photo_" in key]
	image_keys.reverse()
	return image_keys[0]

def remove_empty_folders():
	path = os.getcwd()
	for folder in os.listdir(path):
		if os.path.isdir(path + "/" + folder):
			if not len(os.listdir(path + "/" + folder)):
				shutil.rmtree(path + "/" + folder)

def get_user_name(access_token, user_id):
	method_name = "users.get"
	parameters = {
				"user_ids": user_id
	}

	json_data = vk_tool_core.make_vk_request(access_token, method_name, parameters)
	return json_data['response'][0]['first_name'] + json_data['response'][0]['last_name']

if __name__ == "__main__":
	access_token = vk_tool_core.get_access_token()

	print("dialogs count = " + str(get_dialogs(access_token, return_count=True)))
	
	offs = 0
	i = 1
	dialogs_json = get_dialogs(access_token, offset = offs)

	while len(dialogs_json) > 0:
		for dialog in dialogs_json:
			user_id = str(dialog['message']['user_id'])
			print('check image for ' + user_id + " dialog №" + str(i))
			i += 1

			if dialog['message']['title'] != " ... ":
				continue

			if not os.path.isdir(user_id):
				os.mkdir(user_id)
			else:
				print('skip ' + user_id + ' dialog - folder already exists')
				continue

			save_image(access_token, user_id)

		offs += 200
		dialogs_json = get_dialogs(access_token, offset = offs)

	print("remove empty folders")
	remove_empty_folders()
	print("Success")
