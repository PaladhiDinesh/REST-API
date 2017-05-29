from flask import Flask,jsonify,request,json,render_template, url_for
from flask_pymongo import PyMongo 
import os

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongodb1';
app.config['MONGO_URI']='mongodb://dinesh:password@ds149511.mlab.com:49511/connect_to_mongodb1';

mongo = PyMongo(app)


#daily updating the database
@app.route('/dailyupdate',methods=['POST'])
def daily_update():
    filename = os.path.join(app.static_folder, 'data.json')
    with open(filename) as blog_file:
        data = json.load(blog_file)
        for element in data:
            mongo.db.users.update(element,element,upsert=True)
    return jsonify({'output': 'Inserted'})

#post data to add 
@app.route('/data',methods =['POST'])
def insert_data():
    data = request.json
    for element in data:
        mongo.db.users.update(element,element,upsert=True)
    return jsonify({'output': 'Inserted'})
    

#get all data
#get single user
@app.route('/data',methods =['GET'])
def get_single_user():
    get_params =  request.args
    count = request.headers.get('count')
    user = mongo.db.users
    output = []
    num = 0
    
    if count == None:
        for doc in user.find(get_params, {'_id': False}):
            output.append(doc)
        val=len(output)    
        if val:
            return jsonify({'count':{'totalcount':val},'output':output})
        else:
            return jsonify({'output': 'No results found'})
    else:
        for doc in user.find(get_params, {'_id': False}):
            output.append(doc)
            num = num +1
            if num == int(count):
                break
        if len(output):
            return jsonify({'count':{'totalcount':num},'output':output})
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