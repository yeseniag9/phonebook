from functools import wraps
import secrets 
from flask import request, jsonify, json
import decimal

from models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        # The process below will help us modify the token into such a way that we can use the token and authenticate it
        #  It allows us to either modify the token or send back specific errors detailing what's gone wrong if we make 
        # a faulty api call
        if 'x-access-token' in request.headers: # Checking to see if 'x-access-token' is in our headers for out api calls 
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        
        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated # Part of the checking process is the function returning itself

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)