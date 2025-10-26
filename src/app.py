"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/members', methods=['POST'])
def add_member():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    try:
        new_member = request.get_json()
        if not new_member.get("first_name"):
            return jsonify({"reason": "You are missing the first name"}), 400
        jackson_family.add_member(new_member)
        return jsonify(new_member), 200
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if deleted is None:
            return jsonify({"reason": "Member not found"}), 400
        return jsonify({"done": True}), 200
    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
