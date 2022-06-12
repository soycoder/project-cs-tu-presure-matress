import flask
from flask import Flask,render_template,url_for,request,send_file,jsonify,make_response ,Response
import pickle
import numpy as np
import pandas as pd

import time
from threading import Timer
run = True

def generateCardRiskPosition():

    date = time.strftime('%Y%m%d')

    # ! Read history
    file_name = (
        "../python/history/history.csv")

    raw_data = pd.read_csv(file_name, header=None)
    # print(raw_data)
    raw_pressure = raw_data[1]
    raw_class = raw_data[2]
    index = raw_pressure.index
    number_of_rows = len(index)

    # print(number_of_rows)
    _class = raw_class[number_of_rows-1]

    s_haed = s_shoulder_R = s_shoulder_L = s_elbow_R = s_elbow_L = s_center_hip = s_heel_R = s_heel_L = 0
    r_haed = r_shoulder_R = r_elbow_R = r_center_hip = r_talus = 0
    l_haed = l_shoulder_L = l_elbow_L = l_center_hip = l_talus = 0
    # Risk results
    n_row_fogus = 2
    max_mmHg = 10
    for i in range(n_row_fogus):
        _pressure = raw_pressure[number_of_rows-i-1]
        # { 1 : "Supine", 2 : "Right", 3 : "Left"}
        _pressure = np.fromstring(_pressure[1:-1], dtype=float, sep=' ')
        # print(_pressure)
        _pressure_2d = _pressure.reshape((32, 16))
        max_s_haed = max_s_shoulder_R = max_s_shoulder_L = max_s_elbow_R = max_s_elbow_L = max_s_center_hip = max_s_heel_R = max_s_heel_L = 0
        max_r_haed = max_r_shoulder_R = max_r_elbow_R = max_r_center_hip = max_r_talus = 0
        max_l_haed = max_l_shoulder_L = max_l_elbow_L = max_l_center_hip = max_l_talus = 0
        for yi in range(32):
            for xi in range(16):
                # ? Supine
                if _class == 1:
                    # Head Area
                    if (yi >= 1 and yi <= 4) and (xi >= 5 and xi <= 10):
                        if (max_s_haed < _pressure_2d[yi][xi]):
                            max_s_haed = _pressure_2d[yi][xi]
                    # shoulder_R Area
                    elif (yi >= 5 and yi <= 8) and (xi >= 2 and xi <= 5):
                        if (max_s_shoulder_R < _pressure_2d[yi][xi]):
                            max_s_shoulder_R = _pressure_2d[yi][xi]
                    # shoulder_L Area
                    elif (yi >= 5 and yi <= 8) and (xi >= 10 and xi <= 13):
                        if (max_s_shoulder_L < _pressure_2d[yi][xi]):
                            max_s_shoulder_L = _pressure_2d[yi][xi]
                    # elbow_R Area
                    elif (yi >= 11 and yi <= 12) and (xi >= 1 and xi <= 5):
                        if (max_s_elbow_R < _pressure_2d[yi][xi]):
                            max_s_elbow_R = _pressure_2d[yi][xi]
                    # elbow_L Area
                    elif (yi >= 11 and yi <= 12) and (xi >= 10 and xi <= 14):
                        if (max_s_elbow_L < _pressure_2d[yi][xi]):
                            max_s_elbow_L = _pressure_2d[yi][xi]
                    # center_hip
                    elif (yi >= 13 and yi <= 16) and (xi >= 5 and xi <= 11):
                        if (max_s_center_hip < _pressure_2d[yi][xi]):
                            max_s_center_hip = _pressure_2d[yi][xi]
                    # heel_R Area
                    elif (yi >= 26 and yi <= 29) and (xi >= 1 and xi <= 5):
                        if (max_s_heel_R < _pressure_2d[yi][xi]):
                            max_s_heel_R = _pressure_2d[yi][xi]
                    # heel_L Area
                    elif (yi >= 26 and yi <= 29) and (xi >= 8 and xi <= 14):
                        if (max_s_heel_L < _pressure_2d[yi][xi]):
                            max_s_heel_L = _pressure_2d[yi][xi]
                # ? Right-side
                elif _class == 2:
                    # Head Area
                    if (yi >= 1 and yi <= 4) and (xi >= 5 and xi <= 10):
                        if (max_r_haed < _pressure_2d[yi][xi]):
                            max_r_haed = _pressure_2d[yi][xi]
                    # shoulder_R Area
                    elif (yi >= 6 and yi <= 9) and (xi >= 5 and xi <= 10):
                        if (max_r_shoulder_R < _pressure_2d[yi][xi]):
                            max_r_shoulder_R = _pressure_2d[yi][xi]
                    # elbow_R Area
                    elif (yi >= 10 and yi <= 12) and (xi >= 1 and xi <= 7):
                        if (max_r_elbow_R < _pressure_2d[yi][xi]):
                            max_r_elbow_R = _pressure_2d[yi][xi]
                    # center_hip
                    elif (yi >= 13 and yi <= 17) and (xi >= 5 and xi <= 11):
                        if (max_r_center_hip < _pressure_2d[yi][xi]):
                            max_r_center_hip = _pressure_2d[yi][xi]
                    # talus Area
                    elif (yi >= 26 and yi <= 30) and (xi >= 1 and xi <= 14):
                        if (max_r_talus < _pressure_2d[yi][xi]):
                            max_r_talus = _pressure_2d[yi][xi]
                # ? Left-side
                elif _class == 3:
                    # Head Area
                    if (yi >= 1 and yi <= 4) and (xi >= 5 and xi <= 10):
                        if (max_l_haed < _pressure_2d[yi][xi]):
                            max_l_haed = _pressure_2d[yi][xi]
                    # shoulder_L Area
                    elif (yi >= 6 and yi <= 9) and (xi >= 5 and xi <= 10):
                        if (max_l_shoulder_L < _pressure_2d[yi][xi]):
                            max_l_shoulder_L = _pressure_2d[yi][xi]
                    # elbow_L Area
                    elif (yi >= 10 and yi <= 12) and (xi >= 1 and xi <= 7):
                        if (max_l_elbow_L < _pressure_2d[yi][xi]):
                            max_l_elbow_L = _pressure_2d[yi][xi]
                    # center_hip
                    elif (yi >= 13 and yi <= 17) and (xi >= 5 and xi <= 11):
                        if (max_l_center_hip < _pressure_2d[yi][xi]):
                            max_l_center_hip = _pressure_2d[yi][xi]
                    # talus Area
                    elif (yi >= 26 and yi <= 30) and (xi >= 1 and xi <= 14):
                        if (max_l_talus < _pressure_2d[yi][xi]):
                            max_l_talus = _pressure_2d[yi][xi]

        # Checking Risk 
        # ? Supine
        if max_s_haed >= max_mmHg:
            s_haed = s_haed + 1
        if max_s_shoulder_R >= max_mmHg:
            s_shoulder_R = s_shoulder_R + 1
        if max_s_shoulder_L >= max_mmHg:
            s_shoulder_L = s_shoulder_L + 1
        if max_s_elbow_R >= max_mmHg:
            s_elbow_R = s_elbow_R + 1
        if max_s_elbow_L >= max_mmHg:
            s_elbow_L = s_elbow_L + 1
        if max_s_center_hip >= max_mmHg:
            s_center_hip = s_center_hip + 1
        if max_s_heel_R >= max_mmHg:
            s_heel_R = s_heel_R + 1
        if max_s_heel_L >= max_mmHg:
            s_heel_L = s_heel_L + 1
        # ? Right-side
        if max_r_haed >= max_mmHg:
            r_haed = r_haed + 1
        if max_r_shoulder_R >= max_mmHg:
            r_shoulder_R = r_shoulder_R + 1
        if max_r_elbow_R >= max_mmHg:
            r_elbow_R = r_elbow_R + 1
        if max_r_center_hip >= max_mmHg:
            r_center_hip = r_center_hip + 1
        if max_r_talus >= max_mmHg:
            r_talus = r_talus + 1
        # ? Left-side
        if max_l_haed >= max_mmHg:
            l_haed = l_haed + 1
        if max_l_shoulder_L >= max_mmHg:
            l_shoulder_L = l_shoulder_L + 1
        if max_l_elbow_L >= max_mmHg:
            l_elbow_L = l_elbow_L + 1
        if max_l_center_hip >= max_mmHg:
            l_center_hip = l_center_hip + 1
        if max_l_talus >= max_mmHg:
            l_talus = l_talus + 1

    # print(s_haed, s_shoulder_R, s_shoulder_L, s_elbow_R, s_elbow_L, s_center_hip, s_heel_R, s_heel_L)
    # print(r_haed, r_shoulder_R, r_elbow_R, r_center_hip, r_talus)
    # print(l_haed, l_shoulder_L, l_elbow_L, l_center_hip, l_talus)

    # Response Back
    riskList = []
    # ? Supine 
    if s_haed == n_row_fogus:
        riskList.append("บริเวณหัว")
    if s_shoulder_R == n_row_fogus:
        riskList.append("หัวไหล่ขวา")
    if s_shoulder_L == n_row_fogus:
        riskList.append("หัวไหล่ซ้าย")
    if s_elbow_R == n_row_fogus:
        riskList.append("ข้อศอกขวา")
    if s_elbow_L == n_row_fogus:
        riskList.append("ข้อศอกซ้าย")
    if s_center_hip == n_row_fogus:
        riskList.append("บริเวณก้นกบและสะโพก")
    if s_heel_R == n_row_fogus:
        riskList.append("ส้นเท้าขวา")
    if s_heel_L == n_row_fogus:
        riskList.append("ส้นเท้าซ้าย")
    # ? Right-side 
    if r_haed == n_row_fogus:
        riskList.append("บริเวณหัว")
    if r_shoulder_R == n_row_fogus:
        riskList.append("หัวไหล่ขวา")
    if r_elbow_R == n_row_fogus:
        riskList.append("ข้อศอกขวา")
    if r_center_hip == n_row_fogus:
        riskList.append("บริเวณสะโพกขวา")
    if r_talus == n_row_fogus:
        riskList.append("ตาตุ่ม")
    # ? Left-side 
    if l_haed == n_row_fogus:
        riskList.append("บริเวณหัว")
    if l_shoulder_L == n_row_fogus:
        riskList.append("หัวไหล่ซ้าย")
    if l_elbow_L == n_row_fogus:
        riskList.append("ข้อศอกซ้าย")
    if l_center_hip == n_row_fogus:
        riskList.append("บริเวณสะโพกซ้าย")
    if l_talus == n_row_fogus:
        riskList.append("ตาตุ่ม")

    # riskList = ["บริเวณก้นกบและสะโพก"]

    # riskList
    innerHTML = ""
    if len(riskList) == 0:
        return innerHTML
    else:
        for i in riskList:
            riskTag = (f'''<div class="row">
                <div class="card mt-10 card-green" style="margin-left: 40px;">
                    <div class="card-body">
                        <i class="fa fa-plus" style="font-size: 30px;color: #089bab;" ></i>
                    </div>
                </div>
                <p class="font-weight-bold" style="margin: auto auto auto 20px;">{i}</p>
            </div>''')
            innerHTML += riskTag

        return innerHTML


#Initializing new Flask instance. Find the html template in "templates".
app = flask.Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_mat_plotly')
def get_mat_plotly():
    file_name = ("../python/images/fig1.png")
    return send_file(file_name, mimetype='image/png')

@app.route('/get_riskPosition')
def get_riskPosition():
    response = generateCardRiskPosition()
    return jsonify({
        "riskPositionTag":response
    })
        

if __name__ == '__main__':
	app.run(debug=True)