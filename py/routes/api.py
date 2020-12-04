from flask import Blueprint, current_app, render_template, jsonify, request, json
from py.routes import decorators
from py.models.card import Card
from py.models.user import User
from py.models.deck import Deck

api = Blueprint('api', __name__)

@api.route('/test', methods = ['POST'])
def test():
	return jsonify(True)


@api.route('/create_user', methods = ['POST'])
def create_user():
	req_json = request.json
	username = req_json.get('username')
	password = req_json.get('password')
	password_confirm = req_json.get('password_confirm')
	user = User.create_user(username, password, password_confirm)
	if user is None:
		return jsonify(
			{'success': False}
			)

	return jsonify(
		{
			'user':user.serialize(),
			'success': True
		}
	)

@api.route('/login_user', methods = ['POST'])
def login_user():
	req_json = request.json
	username = req_json.get('username')
	password = req_json.get('password')
	user = User.login(username, password)
	if user is None:
		return jsonify(
				{'success': False}
			)

	return jsonify(
		{
			'user': user.serialize(),
			'success': True
		}
	)

@api.route('/get_decks', methods = ['POST'])
def get_decks():
	"""
	:Arguments are 
	:jwt: User JWT
	"""
	page = request.json.get('page')
	deck_query,pages,dropDown = Deck.get_decks(page)

	return jsonify(
		{
			'decks': deck_query,
			'num_pages': pages,
			'dropDown': dropDown,
			'success': True
		}
		)

@api.route('/add_deck_to_tmp_collection', methods = ['POST'])
def add_deck_to_tmp_collection():

	deck_id = request.json.get('deck_id')
	deck = Deck.query.filter_by(deck_id = deck_id).first()
	tmp_collection = request.json.get('temporary_collection')
	new_collection = Deck.add_deck_to_tmp(deck,tmp_collection)

	return jsonify(
		{
			'success': True,
			'updated_collection': tmp_collection,
			'deck': deck.serialize()
		})

@api.route('/remove_deck_from_tmp_collection', methods= ['POST'])
def remove_deck_from_tmp_collection():

	deck_id = request.json.get('deck_id')
	deck = Deck.query.filter_by(deck_id = deck_id).first()
	tmp_collection = request.json.get('temporary_collection')
	new_collection = Deck.remove_deck_from_tmp(deck,tmp_collection)

	return jsonify(
		{
			'success': True,
			'updated_collection': tmp_collection,
			'deck': deck.serialize()
		})
	
@api.route('/check_has_deck', methods = ['POST'])
def check_has_deck():
	"""
	:Arguments are
	:
	:deck_id : the deck we are checking
	"""
	deck_id = request.json.get('deck_id')
	tmp_collection = request.json.get('tmp_collection')
	missing_cards = request.json.get('missing_cards')
	deck = Deck.query.filter_by(deck_id = deck_id).first()
	has_deck,missing_from_deck = Deck.has_deck(deck,tmp_collection,missing_cards)

	return jsonify({
		"success": True,
		"deck_id": deck_id,
		"has_deck": has_deck,
		"missing_from_deck": missing_from_deck
		})

@api.route('/get_user_info', methods = ['POST'])
@decorators.check_user_jwt
def get_user_info(user):
	"""
	: Given a json object with 
	: jwt : User JWT
	: Returns serialzied user in JSON form
	: Adding @decorators.check_user_jwt 
	: will automatically read the jwt in the json data 
	: and decode the user and return it as user above.
	: We'll use this a lot. It returns jsonify None otherwise
	"""
	return jsonify ({
		"success" : True,
		"user" : user.serialize()
	})


@api.route('/update_collection_card_quantity', methods = ['POST'])
@decorators.check_user_jwt
def update_collection_card_quantity(user):
	"""
	: Arguments are 
	: jwt: user jwt
	: card_id : the card_id we are adding 
	: new_quantity: new quantity of the card we're updating
	: Updates the user object with the new quantity 
	"""
	PRACTICALLY_INFINITY = 10000
	card_id = request.json.get('card_id')
	new_quantity = request.json.get('new_quantity')
	if new_quantity > PRACTICALLY_INFINITY or new_quantity < 0:
		return jsonify({
			"success": False
			})

	card = Card.query.filter_by(card_id = card_id).first()
	user.remove_card_from_collection(card, PRACTICALLY_INFINITY)
	user.add_card_to_collection(card, new_quantity)
	serialized_user = user.serialize()
	return jsonify({
		"user" : serialized_user,
		"success": True
	})


@api.route('/query_cards', methods = ['POST'])
@decorators.check_user_jwt
def query_cards(user):
	"""
	: search_query: string input for what the user typed
	: return type: List of cards that match the search query
	: A match is defined if the formatted search_query is a substring of the 
	: search_card name property. 
	"""

	search_query = request.json.get('search_query')
	card_query = user.query_cards(search_query)
	return jsonify({
		"queried_cards" : card_query,
		"user" : user.serialize(),
		"success": True		
	})





