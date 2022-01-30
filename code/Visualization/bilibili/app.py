#import webbrowser

import pymysql
from flask import Flask
from pyecharts.charts import Bar, Funnel
import numpy as np
import pandas as pd
import os
import select,socket
app = Flask(__name__)

@app.route('/')
def route():


    #return "welcome to use"
    #os.system('./Desktop/static/index.html')
   #webbrowser.open("./Desktop/static/index.html ")
   return 'try "/static/templates/index.html"'
   ###@app.route('/index')



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
