import os
from janus_tool import *

from flask import Flask, jsonify, render_template
from threading import Thread

apisecret = "janusrocks"
app = Flask(__name__, instance_relative_config=True, 
            static_url_path='', static_folder='static')
   


@app.route('/')
@app.route('/list')
def list():
    ret_list = []
    ls = list_streams(apisecret)
    for s in ls:
        ret_list.append(stream_info(apisecret, s['id']))
    return render_template("video_list.html", stream_list = ret_list)
    return jsonify(ret_list)

@app.route('/video/<video_id>')
def video(video_id):
    return render_template("video.html", video_id = video_id)
@app.route('/video_simple/<video_id>')
def video_simple(video_id):
    return render_template("video_simple.html", video_id = video_id)




app.run(debug=True, host= '0.0.0.0', port= 5001)

#   Preparing parameters for flask to be given in the thread
#   so that it doesn't collide with main thread

