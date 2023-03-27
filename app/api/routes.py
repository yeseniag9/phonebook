from flask import Blueprint, request, jsonify, render_template # jsonify will take our data and put it in JSON format so we can persue the data using JS and python
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema 

api = Blueprint('api', __name__, url_prefix='/api') # Every time we write an api route, we have to have /api before the slug

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'} # Looks like a dicitonary but instead returns json (package of data)

@api.route('/contacts', methods = ['POST']) # We'll be posting data to the database
@token_required # Going to keep looping over and over until it gets the token (either throw an erorr or be successful)
def create_contact(current_user_token):
    name = request.json['name'] # Going to bring back the key of the name (name on one side, value on other)
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token)

    db.session.add(contact)
    db.session.commit() # Puts all the information in the database from Contact

    response = contact_schema.dump(contact)
    return jsonify(response) # When we run this funciton, whatever we send to it will actually be shown on our api
    # The above two lines send the Contact information from line 25 back to our requester (insomnia in our case) to 
    # show it what the current databse holds

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

# Example of how to isolate one contact
@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id): # id became a variable that could be pulled down into the function
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

# Update endpoint
@api.route('/contacts/<id>', methods = ['POST', 'PUT']) # PUT means replace 
@token_required
def update_contact(current_user_token, id):
    contact = Contact.query.get(id)
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# Delete endpoint
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)