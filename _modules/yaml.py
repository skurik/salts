# See e.g. https://github.com/saltstack/salt/blob/develop/salt/modules/postgres.py

from __future__ import absolute_import

import yaml
import datetime
import logging
import os

def __virtual__():
    return True

def load_yaml(path):
	with file(path, 'r') as stream:
		data = yaml.load(stream)

	return data

def save_yaml(yaml_doc, path):
	with file(path, 'w') as out_stream:
		yaml.dump(yaml_doc, out_stream)
		out_stream.close()

def get_value(yaml_doc, key_path):	
	for path_token in key_path.split('/'):
		yaml_doc = yaml_doc.get(path_token, None)
		if yaml_doc == None:
			break

	return yaml_doc

def modify_yaml(yaml_doc, key_path, value):
	path_tokens = key_path.split('/')
	token_data = [(path_tokens[i], (i + 1) == len(path_tokens)) for i in range(0, len(path_tokens))]

	for token_info in token_data:
		token = token_info[0]
		is_last = token_info[1]

		if is_last:
			yaml_doc[token] = value
		else:
			yaml_doc = yaml_doc.get(token, None)
			if yaml_doc == None:
				new_node = {}
				yaml_doc[token] = new_node
				yaml_doc = new_node

	return True
	