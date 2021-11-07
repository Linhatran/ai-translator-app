from flask import Flask, redirect, url_for, request, render_template, session
import requests
import os
import uuid
import json
import sys
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # retrieve form values
    input_text = request.form['text']  # target textarea
    # choose from language dropdown
    selected_language = request.form['language']

    # get values from .env file
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # indicate API v3.0
    path = '/translate?api-version=3.0'
    # target language as param
    language_param = '&to=' + selected_language
    url = endpoint + path + language_param

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': input_text}]
    translator_request = requests.post(url, headers=headers, json=body)
    translator_response = translator_request.json()
    translated_text = translator_response[0]['translations'][0]['text']
    return render_template('results.html', translated_text=translated_text, input_text=input_text, selected_language=selected_language)
