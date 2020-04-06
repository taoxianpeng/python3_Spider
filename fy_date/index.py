from flask import Flask
from flask import render_template
from flask import request as flask_request
from fyspider import FySpyder
from weather import Weather
import os

app=Flask(__name__)
fy = FySpyder()
w = Weather()



def added(td,yd):
    c = int(td)-int(yd)
    if c>=0:
        return td+' (较昨日：+'+str(c)+')'
    else:
        return td+' (较昨日：'+str(c)+')'

@app.route('/index')
def index():

    return render_template('index.html',
        weather = w.parse()[0], 
        temperature = w.parse()[1],
        deadline = fy.parse()[0][0],
        total_num = added(fy.parse()[0][1],fy.parse()[1][0]),
        suspect_num = fy.parse()[0][2]+' (较昨日：'+fy.parse()[1][1]+')',
        dead_num = added(fy.parse()[0][3],fy.parse()[1][2]),
        recover_num = added(fy.parse()[0][4],fy.parse()[1][3])
        )

if __name__ == "__main__":
    app.run()