import json

from flask import Flask, request,jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)


firebase_admin.initialize_app(cred)

firestoredb = firestore.client()



students_ref = firestoredb.collection(u'students')
students = students_ref.stream()



def getstudents():
    students = students_ref.stream()
    return [voter.to_dict() for voter in students]



@app.route('/')
def index():
    return "Welcome to the ashesi social connect api"


#1. Register a student 
@app.route('/register', methods=['POST'])
def register():
    record = json.loads(request.data)
    StudID=None
    email = None

    #check for student id and email
    for key in record.keys():
        if key == 'StudID':
            StudID = record.get(key)
            print(StudID)
        if key == 'email':
            email=record.get(key)
        
    #check if student id is available
    if not StudID:
        return jsonify({'error':'student id is not available'}),400

    if not email or not email.endswith('@ashesi.edu.gh'):
        return jsonify({'error':'Invalid email'}),404
    else:
        for details in students:
            details = details.to_dict()
            if details["StudID"] == StudID:
                return jsonify({"error": "the id already exists in the records"}),404
        students_ref.document(record['StudID']).set(record)
         
        return jsonify(record)


# 2. Updating the registered information
@app.route('/update-student/<int:id>', methods=['PUT'])
def update_record(id:int):
    record = json.loads(request.data)
    voter_ref = firestoredb.collection(u'students').document(str(id))
    voter = voter_ref.get()
    
    if voter.exists:
        voter_ref.set(record, merge=True)
        return jsonify(record), 200
    else:
        return ({'Error': 'There is no voter with that ID'}), 404


# 3. Retriving registered student
@app.route('/get_student/<int:StudID>/', methods = ['GET'])
def retrieve_voter(StudID:int):
    for record in students:
        record = record.to_dict()
        if record['StudID'] == str(StudID):
            return jsonify(record), 200
    return jsonify({'error':'data not found'}), 404


def entry_point(request):
    #Create a new app context for the internal app
    internal_ctx = app.test_request_context(path=request.full_path,
                                            method=request.method)
    
    #Copy main request data from original request
    #According to your context, parts can be missing. Adapt here!
    internal_ctx.request.data = request.data
    internal_ctx.request.headers = request.headers
    
    #Activate the context
    internal_ctx.push()
    #Dispatch the request to the internal app and get the result 
    return_value = app.full_dispatch_request()
    #Offload the context
    internal_ctx.pop()
    
    #Return the result of the internal app routing and processing      
    return return_value


if __name__ == "__main__":
    app.run(debug=True)


