# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask
app = Flask(__name__)

import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO

import string
import json

# Set image_url to the URL of an image that you want to analyze.
#flag is true if the file is online
#flag is false if the file is offline
image_url = "https://image.shutterstock.com/image-photo/melbourne-australia-april-5-2015-260nw-268315469.jpg"


def extractWords(image_url):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, json=data)
    response.raise_for_status()
    
    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.
    
    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]
    
    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        
        time.sleep(1)
        if ("recognitionResults" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll = False
    
    polygons = []
    if ("recognitionResults" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["recognitionResults"][0]["lines"]]

    word = []
    for i in polygons:
        word.append(i[1])
    return(word)

    


#input (phrase) must be a string
def autocorrect(phrase):
    api_key = "b43eadb7fd814561ab19b57faaceaab8"
    example_text = phrase # the text to be spell-checked
    endpoint = "https://spellchecking.cognitiveservices.azure.com/bing/v7.0/spellcheck"
    
    data = {'text': example_text}
    
    params = {
    'mkt':'en-us',
    'mode':'proof'
    }
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Ocp-Apim-Subscription-Key': api_key,
    }
    
    response = requests.post(endpoint, headers=headers, params=params, data=data)

    json_response = response.json()
    return(json.dumps(json_response, indent=4))

def main():
    words = (extractWords(image_url))
    autocorrectWords = json.loads(autocorrect(' '.join(words)))
    for i in autocorrectWords['flaggedTokens']:
        for j in range(0,len(words)):
            if words[j]==i['token']:
                words[j]=i['suggestions'][0]['suggestion']
    for i in range(0,len(words)):
        for char in string.punctuation:
            words[i] = words[i].replace(char, '')
            words[i]=words[i].replace(' ', '')

    types = ['regular','diesel','plus','premium','vpower','supreme','extra','unleaded']
    #for i in words:
    dict_fuels = {}
    for i in range(0,len(words)):
        if words[i].lower() in types:
            for j in range(i+1,len(words)):
                if (words[j].isdigit()) and (words[i].lower() in types):
                    words[j]=words[j][:1]+'.'+words[j][1:]
                    dict_fuels.update({words[i]:words[j]})
                    i = j+1
                    j = len(words)
        
    print(json.dumps(dict_fuels))
    
      #      for 
#def extractPriceAndType(words):
    
main()
    
