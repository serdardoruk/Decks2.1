
import jwt
import os
from passlib.hash import argon2
from flask_sqlalchemy import SQLAlchemy
from py.models.database import db
from py.models.model_config import TableNames
from py.models.card import Card

UTF8 = "utf-8"
algorithm = "HS256"
SECRET_KEY = "SECRET_KEY"


class CollectionCard(db.Model):
	__tablename__ = TableNames.CollectionCard

	collection_card_id = db.Column(db.Integer, primary_key=True, unique = True, autoincrement = True)
	user_id = db.Column(db.Integer, db.ForeignKey(TableNames.User + '.user_id'), nullable = False)
	card_id = db.Column(db.Integer, db.ForeignKey(TableNames.Card + '.card_id'), nullable = False)
	quantity = db.Column(db.Integer, nullable = False)
	
	card = db.relationship(TableNames.Card , lazy = True,
		primaryjoin="CollectionCard.card_id == Card.card_id")

	date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())

	def serialize(self):
		output = {}
		output['collection_card_id'] = self.collection_card_id
		output['card_id'] = self.card_id
		output['user_id'] = self.user_id
		output['quantity'] = self.quantity
		output['card'] = self.card.serialize()
		return output


class User(db.Model):
	__tablename__ = TableNames.User
	user_id = db.Column(db.Integer, primary_key=True, unique = True, autoincrement = True)
	collection = db.relationship(TableNames.CollectionCard, backref = "owner", lazy = True,
		primaryjoin="User.user_id == CollectionCard.user_id")

	username = db.Column(db.String, nullable = False)
	password_hash = db.Column(db.String, nullable = False)
	date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())


	def __init__(self, username, password):
		"""
		: Initializes a user with an empty collection
		"""
		self.username = username
		self.password_hash = User.argonHash(password)
		self.jwt = self.create_jwt()
		

	def __repr__(self):
		return '<User %r >' % (self.username)

	def __str__(self):
		"""
		: returns a string with the user's information 
		: including their collection
		: Make the string however you see fit
		"""
		pass

	

	def serialize(self, include_jwt = True):
		"""
		: Returns the user and their collection in dictionary form
		: This function needs to be implemented
		"""
		output = {}
		output['user_id'] = self.user_id
		output['username'] = self.username
		if include_jwt:
			output['jwt'] = self.create_jwt()

		output['collection'] = [card.serialize() for card in self.collection]
		return output


	def collection_size(self):
		"""
		: returns an integer with the number of cards in the collection
		"""
		size = 0
		for card in self.collection:
			size += card.quantity
		return size

	def query_cards(self, search_query, query_limit = 100):
		"""
		: search_query: string input for what the user typed
		: return type: List of cards that match the search query.
		: A match is defined if the formatted search_query is a substring of the 
		: search_card name property.
		: Make sure to include the quantity of each card for this user 
		"""
		search_name = Card.format_card_name_for_search(search_query)
		matching_cards = Card.query.filter(Card.search_name.contains(search_name)).limit(query_limit)
		
		output = []
		for card in matching_cards:
			check_if_in_collection = CollectionCard.query.filter_by(user_id = self.user_id, card_id = card.card_id).first()
			if check_if_in_collection:
				card_dict = {"quantity": check_if_in_collection.quantity, "card": card.serialize()}
				output.append(card_dict)
			else:
				card_dict = {"quantity": 0, "card": card.serialize()}
				output.append(card_dict)
		return output

	def add_card_to_collection(self, card, quantity):
		"""
		: card: is a Card object from card.py
		: quantity : non-negative integer
		: adds this card and quantity to the user's collection
		: if the card already exists, we increment it's amount
		: return type: None
		"""
		if card is None:
			return None
		
		if quantity < 1:
			return None

		check_if_in_collection = CollectionCard.query.filter_by(user_id = self.user_id, card_id = card.card_id).first()

		if check_if_in_collection:
			check_if_in_collection.quantity += quantity
			db.session.commit()
			return None

		else:
			new_card = CollectionCard(user_id = self.user_id, card_id = card.card_id, quantity = quantity)
			db.session.add(new_card)
			db.session.commit()
			return None

	def remove_card_from_collection(self, card, quantity):
		"""
		: card: is a Card object from card.py
		: quantity: non-negative integer
		: removes this card quantity pair from the collection. 
		: If the collection doesn't have this amount of the 
		: card, then remove all copies of the card 
		: Remember when you set a card's quantity to zero
		: to actually delete the row from the database
		: return type: None
		"""
		if card is None:
			return None
		if quantity < 1:
			return None
		check_if_in_collection = CollectionCard.query.filter_by(user_id = self.user_id, card_id = card.card_id).first()
		if check_if_in_collection is None:
			return None
		if check_if_in_collection.quantity > quantity:
			check_if_in_collection.quantity -= quantity
			db.session.commit()
		else: 
			db.session.delete(check_if_in_collection)
			db.session.commit()
		
	def missing_cards_from_main_deck(self, deck):
		"""
		: deck : Deck object from deck.py
		: Given a deck returns a list of tuples
		: indicating which cards are missing from the main deck
		: return type: list of tuples with Card object and quantity 
		: example output: [(name, quantity),....]
		"""
		output = []
		for deck_card in deck.main_deck:
			check_if_in_collection = CollectionCard.query.filter_by(user_id = self.user_id, card_id = deck_card.card_id).first()
			if check_if_in_collection:
				if check_if_in_collection.quantity < deck_card.quantity:
					card_dict = {"name": deck_card.card.name, "quantity": deck_card.quantity - check_if_in_collection.quantity, "card": deck_card.card}
					output.append(card_dict)
			else:
				if deck_card.quantity == 0:
					continue
				card_dict = {"name": deck_card.card.name, "quantity": deck_card.quantity, "card": deck_card.card}
				output.append(card_dict)
		return output

	def missing_cards_from_sideboard(self, deck):
		"""
		: deck : Deck object from deck.py
		: Given a deck returns a list of tuples of indicating 
		: which cards are missing  from the sideboard
		: return type: list of tuples with Card object and quantity 
		: example output: [(name, quantity),....]
		: Hint: Get missing cards from deck and subtract missing cards from main_deck
		: Do this method last
		"""
		missing_from_whole_deck = self.missing_cards_from_deck(deck)
		missing_from_main_deck = self.missing_cards_from_main_deck(deck)
		output = []
		for triple in missing_from_whole_deck:
			for also_triple in missing_from_main_deck:
				if also_triple["name"] == triple["name"]:
					if triple["quantity"] > also_triple["quantity"]:
						new_triple = {"name": triple["name"], "quantity": triple["quantity"] - also_triple["quantity"], "card": triple["card"]}
						output.append(new_triple)
						missing_from_whole_deck.remove(triple)
					else:
						missing_from_whole_deck.remove(triple)

		output = output + missing_from_whole_deck
		return output

	def missing_cards_from_deck(self, deck):
		"""
		: deck : Deck object from deck.py
		: Given a deck returns a tuple with 2 lists of 
		: card objects indicating which cards are missing 
		: from the main deck and sideboard
		: return type: list of tuples with Card object and quantity 
		: example output: [(name, quantity),....]
		"""
		md_list = deck.main_deck
		sb_list = deck.sideboard
		needed_list = {}
		for deck_card in (md_list + sb_list):
			card_id = deck_card.card_id
			if needed_list.get(card_id):
				needed_list[card_id] += deck_card.quantity
			else:
				needed_list[card_id] = deck_card.quantity
		merged_list = md_list + sb_list
		output = []
		for card_id, quantity in needed_list.items():
			collection_card = CollectionCard.query.filter_by(user_id = self.user_id, card_id = card_id).first()
			this_card  = Card.query.filter_by(card_id = card_id).first()
			if collection_card:
				if collection_card.quantity < quantity:
					card_dict = {"name": this_card.name, "quantity": quantity - collection_card.quantity, "card": this_card}
					output.append(card_dict)
			else:
				card_dict = {"name": this_card.name, "quantity": quantity, "card": this_card}
				output.append(card_dict)
		return output

	def has_deck(self, deck, missing_cards = 0):
		"""
		: deck : Deck object from deck.py
		: given a deck returns True if this collection can make the given deck 
 		: with this collection. 
 		: Optinal missing_cards parameter allows that many number of 
 		: cards from the collection that cannot be in the deck.
 		: 
 		: Example: if a user had all of Jeskai except 4 Scalding Tarns
 		: this function would return True for arguemnts (Jeskai, misisng_cards) where
 		: missing_cards >= 4 and false for missing_cards < 4

 		: return type: boolean
		"""
		if deck is None:
			return None
		missing_from_whole_deck = self.missing_cards_from_deck(deck)
		if (missing_from_whole_deck is None) and missing_cards == 0:
			return True
		count = 0
		for triple in missing_from_whole_deck:
			count += triple["quantity"]
		return count <= missing_cards

	def remove_deck(self, deck):
		"""
		: for every card in the deck, remove each card and it's quantity
		: from the collection. If the collection doesn't have every card in the deck
		: then do nothing to the collection and return None. Otherwise return the deck object
		: return type: deck object
		"""
		if not self.has_deck(deck):
			return None
		for deck_card in deck.main_deck:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			self.remove_card_from_collection(card, deck_card.quantity)
		for deck_card in deck.sideboard:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			self.remove_card_from_collection(card, deck_card.quantity)
		return deck

	def add_deck(self, deck):
		"""
		: for every card in the deck, add each card and it's quantity
		: to this collection
		: No return value
		"""
		for deck_card in deck.main_deck:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			self.add_card_to_collection(card, deck_card.quantity)
		for deck_card in deck.sideboard:
			card = Card.query.filter_by(card_id = deck_card.card_id).first()
			self.add_card_to_collection(card, deck_card.quantity)

	@staticmethod
	def login(username, password):
		"""
		: Given a login attempt, returns the corresponding user if credentials are valid
		: If invalid, then returns None
		"""
		user_matches = User.query.filter_by(username = username).all()
		if len(user_matches) == 0:
			return None
		user = user_matches[0]
		if User.argonCheck(password, user.password_hash) == False:
			return None
		return user

	@staticmethod
	def check_password(password, password_confirm):
		if (password == "") or (password is None) or (password != password_confirm):
			return False
		return True

	@staticmethod
	def create_user(username, password, password_confirm):
		check_if_username_is_in_database = User.query.filter_by(username = username).first()
		check_if_legal_password = User.check_password(password, password_confirm)
		if (check_if_username_is_in_database is not None) or (not check_if_legal_password):
			return None
		else:
			new_user = User(username = username, password = password)
			db.session.add(new_user)
			db.session.commit()
			return new_user

	def create_jwt(self):
		payload = self.serialize(include_jwt = False)
		secret_key = os.environ.get(SECRET_KEY)
		this_jwt = jwt.encode(payload, secret_key, algorithm = algorithm)
		return this_jwt.decode(UTF8)

	@staticmethod
	def decode_jwt(jwt_str):
		if jwt_str is None:
			return None
		try:
			encoded = jwt_str.encode(UTF8)
			decoded = jwt.decode(encoded, os.environ.get(SECRET_KEY), algorithms=[algorithm])
			user_id = decoded.get("user_id")
			if user_id is None:
				return None
			jwt_user = User.query.filter_by(user_id = user_id).first()
			return jwt_user
		except:
			return None

	@staticmethod
	def argonHash(pre_hash):
		"""
		: Uses argon algorithm to hash a string 
		"""
		return argon2.using(rounds=4).hash(pre_hash)

	@staticmethod
	def argonCheck(pre_hash, post_hash):
		"""
		: Uses argon hash to check if the pre_hash and post_hash are a match
		: Returns True if so and False otherwise
		"""
		if pre_hash is None:
			return False
		return argon2.verify(pre_hash, post_hash)
