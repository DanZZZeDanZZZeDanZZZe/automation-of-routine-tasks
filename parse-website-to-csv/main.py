import os
import csv
import json
import requests
from bs4 import BeautifulSoup

CONFIG_PATH = './config.json'

def get_word_from_page(page):
	return page.select("h1")[0].contents[0]

def get_translation_from_page(page):
	return page.select("div.t_inline_en")[0]

def get_transcription_from_page(page):
	return page.select("span.transcription")[0]

def get_phrases_from_page(page):
	li = page.select("div.block.phrases")[0]
	return li 

def get_sentences_from_page(page):
	li = page.select("div.block")[1]
	return li 	

def create_title(text, page):
	h3 = page.new_tag("h3")
	h3.append(text)
	return h3

# def get_examples_from_page(page):

# 	print(create_title("phrases", page))
# 	return get_phrases_from_page(page)

def get_examples_from_page(page):
	li = [
		create_title("phrases", page),
		get_phrases_from_page(page),
		create_title("sentences", page),
		get_sentences_from_page(page),
	]
	return ''.join([str(i) for i in li])

# def get_content(page):
# 	return {	
# 		"word": get_word_from_page(page),
# 		"translation": get_translation_from_page(page),
# 		"transcription": get_transcription_from_page(page),
# 		"examples": get_examples_from_page(page)
# 	}

def get_content(page):
	return [
		get_word_from_page(page),
		get_translation_from_page(page),
		get_transcription_from_page(page),
		get_examples_from_page(page)
	]

with open(CONFIG_PATH) as config_file:
	configuration = json.load(config_file)
	config_file.close()

txt_file_path = os.path.join(
	configuration['input-file']['path'],
	configuration['input-file']['name']
)

output_file_path = os.path.join(
	configuration['output-file']['path'],
	configuration['output-file']['name']
)

with open(txt_file_path) as txt_file: 
	english_words = txt_file.readlines()
	txt_file.close()

content_url = configuration['content']['url']

content_paths = [f'{content_url}/{word.strip()}' for word in english_words]

responses = [requests.get(path) for path in content_paths]

pages = [BeautifulSoup(response.text, 'html.parser') for response in responses]

content = [get_content(page) for page in pages]

with open('output-file.tsv', 'w', newline='') as tsvfile:
    # fieldnames = ["word", "translation", "transcription", "examplest"]
    writer = csv.writer(tsvfile, delimiter='\t')

    # writer.writeheader()
    for row in content: 
    	writer.writerow(row)

    tsvfile.close()