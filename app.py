from flask import Flask, render_template, request
import pickle
import pandas as pd

app=Flask(__name__)
model=pickle.load(open('physical_properties.pkl','rb'))
data=pd.read_csv('aluminum_wire_properties_10000.csv')

@app.route("/")
def index():
    heat_treat=sorted(data['Heat Treatment (Yes=1, No=0)'].unique())
    bae={0:"NO",1:"YES"}
    return render_template('index2.html',heat_treat=bae.values())

@app.route("/predict",methods=['GET','POST'])
def predict():
    heat_treatment=['NO','YES']
    al = float(request.form.get('al'))
    mg = float(request.form.get('mg'))
    si = float(request.form.get('si'))
    zn = float(request.form.get('zn'))
    temp = float(request.form.get('temp'))
    rs = float(request.form.get('rs'))
    heat = request.form.get('heat')
    bae={0:"NO",1:"YES"}
    prediction = model.predict([[al, mg, si, zn, temp, rs, heat_treatment.index(heat)]])
    output1 = round(prediction[0][0], 2)
    output2 = round(prediction[0][1], 2)
    output3 = round(prediction[0][2], 2)
    # print(output[0])
    return render_template("index2.html",output1_text=f'Tensile Strength (MPa): {output1}',output2_text=f'Yield Strength (MPa): {output2}',output3_text=f'Elongation (%): {output3}',heat_treat=bae.values())

if __name__=="__main__":
    app.run(debug=True)