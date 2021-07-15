from flask import Blueprint, request, make_response, jsonify, redirect


restaurant_blueprint = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@restaurant_blueprint.route("/add", methods=['POST'])
def add_resturant():
    return {"message":"ok"}


@restaurant_blueprint.route("/list")
def get_resturant():
    return {"message":"ok"}

