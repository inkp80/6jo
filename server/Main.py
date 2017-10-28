from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__);

testVar = 0;

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]



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
@app.route("/post", methods=["POST"])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        return "ok, " + title;
    else :
        return "error";

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5009);
