"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# Initialize Flask app and configuration
app = Flask(__name__)
app.url_map.strict_slashes = False  # Allows routes to work with or without a trailing slash
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize the Jackson family data structure
jackson_family = FamilyStructure("Jackson")

# Standard error handler for API exceptions
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Root route to generate a sitemap of all available endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1) Endpoint to retrieve the complete list of family members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# 2) Endpoint to retrieve a specific member by their unique ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"msg": "Not found"}), 404

# 3) Endpoint to add a new member; returns the created object to satisfy test requirements
@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Body required"}), 400
    
    # Logic in datastructures.py handles ID assignment if not provided in the body
    new_member = jackson_family.add_member(body)
    return jsonify(new_member), 200

# 4) Endpoint to remove a member; returns the 'done' key as required by automated tests
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    if success:
        return jsonify({"done": True}), 200
    return jsonify({"msg": "Not found"}), 404

# Main entry point to run the server
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

