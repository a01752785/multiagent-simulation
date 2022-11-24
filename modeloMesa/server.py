#----------------------------------------------------------
# Evidencia 1. Actividad Integradora
# Python flask server to interact with Unity. Based on the 
# code provided by Sergio Ruiz.
# Octavio Navarro. October 2021
# 
# Date: 21-Nov-2022
# Authors:
#           Eduardo Joel Cortez Valente A01746664
#           Paulo Ogando Gulias A01751587
#           David Damián Galán A01752785
#           José Ángel García Gómez A01745865
#----------------------------------------------------------

from flask import Flask, request, jsonify
from model import *


app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel

    if request.method == 'POST':
        cars = int(request.form.get('NCars'))

        print(request.form)
        print(cars)
        randomModel = CityModel(cars)
        currentStep = 0

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getCar', methods=['GET'])
def getCar():
    global randomModel

    if request.method == 'GET':
        carPosition = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z, "isInDestiny":agent.isInDestiny} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, Car)]

        return jsonify({'positions':carPosition})

@app.route('/getTraffic_Light', methods=['GET'])
def getTraffic_Light():
    global randomModel

    if request.method == 'GET':
        traficLightPosition = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z, "state":agent.state} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, Traffic_Light)]

        return jsonify({'positions':traficLightPosition})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
