import os
import sys
from flask import Flask
from flask import jsonify
from flask import request
from dqn_agent import DQNAgent
import numpy as np

app = Flask(__name__);

enable_actions = np.arange ( 8 * 8 )
#BLACK == 1
#WHITE == 2
#BLANK == 0

testVar = 0;
# dqnAgentObj = DQNAgent(enable_actions, 1, 8, 8);


enable_actions = np.arange(64)
name = os.path.splitext (os.path.basename(__file__))[ 0 ]
agent = DQNAgent(enable_actions, name, 8, 8)


@app.route("/")
def helloWorld():
    a = "12341"
    return "python server, current testVar is " +str(testVar);

@app.route("/loadData", methods=["GET","POST"])
def loadData():
    global testVar
    testVar += 1
    return "this is from python server";

#jsonify -
@app.route("/json", methods=["GET"])
def getTask():
    return jsonify({"tasks": tasks});

#POST
#get Data json in flask
#https://stackoverflow.com/questions/43218413/get-data-json-in-flask
#Error : global name 'request' is not defined flask
#Solution : add 'from flask import request'

# self .Blank =  0
# self .Black =  1
# self .White =  2
@app.route("/post", methods=["POST"])
def upload():
    if request.method == 'POST':
        # title = request.form['title']
        status = request.form['status']

        statusArr = np.array([]);
        statusList = [];
        statusRes = [];
        cnt = 0;
        for i in range(0, len(status)):
            cnt += 1;
            ch = status[i]
            if ch == "0":
                statusList.append(0)
            elif ch == "1":
                statusList.append(1)
            elif ch == "2":
                statusList.append(2)
            if cnt == 8:
                cnt = 0;
                statusRes.append(statusList)
                statusList = []

        statusArr = np.array(statusRes)
        print(statusArr);

        target = request.form['target']
        targetList = [];
        targetList = target.split(',')
        targetList = targetList[:-1]
        targetList = list(map(int, targetList))
        Q_max, Q_action = agent.select_enable_action(statusRes, targetList)
        print(targetList)
        targetList = []

        # dqnAgentObj.select_enable_action(statusRes, targetList)
        # Q_max, Q_action = dqnAgentObj.select_enable_action(statusRes, targetList)
        res = int(Q_action)
        print("AI's turn : " + str(res))

        return str(res)
        # return "ok, " + status + ", " + target;
    else :
        return "error";

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5090);
