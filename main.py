# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 19:30:28 2019

@author: ghosh
"""

from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
