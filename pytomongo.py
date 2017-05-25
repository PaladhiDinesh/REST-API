from flask import Flask,jsonify,request
from flask.ext.pymongo import PyMongo
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongodb1';
app.config['MONGO_URI']='mongodb://dinesh:password@ds149511.mlab.com:49511/connect_to_mongodb1';

mongo = PyMongo(app)


#post data to add 
@app.route('/data',methods =['POST'])
def insert_data():
    data = request.json
    mongo.db.users.insert(data)
    return jsonify({'output': 'Inserted'})
    

#get all data
#get single user
@app.route('/data',methods =['GET'])
def get_single_user():
    get_params =  request.args
    user = mongo.db.users
    output = []

    for doc in user.find(get_params, {'_id': False}):
        output.append(doc)
    if len(output):
        return jsonify(output)
    else:
        return jsonify({'output': 'No results found'})
#to delete data
@app.route('/data', methods =['DELETE'])
def delete_data():
    get_params = request.args
    if len(get_params):
        user = mongo.db.users
        count = user.find(get_params).count()
        if count:
            for doc in user.find(get_params):
                user.remove(doc)
            return jsonify({'output': 'Deleted'})
        else:   
            return jsonify({'output': 'Object not found'})
    else:
        return jsonify({'output': 'Please send parameters to delete an object'})
    
    
@app.route('/data',methods=['PUT'])
def update_data():
    data = request.json
    mongo.db.users.update(data['query'],data['update'])
    return jsonify({'output': 'Updated'})

@app.route('/data/count',methods=['GET'])
def get_data_count():
    user = mongo.db.users
    count = user.find().count()
    return jsonify({'output': count})


    
if __name__ == '__main__':
    app.run(debug = True)