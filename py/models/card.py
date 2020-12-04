
import jwt
import os
from passlib.hash import argon2
from flask_sqlalchemy import SQLAlchemy
from py.models.database import db
from py.models.model_config import TableNames


class Card(db.Model):
	__tablename__ = TableNames.Card
	card_id = db.Column(db.Integer, primary_key=True, unique = True, autoincrement = True)
	name = db.Column(db.String, nullable = False, unique = True)
	search_name = db.Column(db.String, unique = True)
	date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
										   onupdate=db.func.current_timestamp())

	
	def __init__(self, name):
		self.name = name
		self.search_name = Card.format_card_name_for_search(name)
		
	def serialize(self):
		output = {}
		output['card_id'] = self.card_id
		output['name'] = self.name
		return output

	@staticmethod
	def format_card_name_for_search(input_name):
		REMOVED_CHARACTERS = [" ", "\\", ",", ".", "'"]
		formatted_string = input_name
		for c in REMOVED_CHARACTERS:
			formatted_string = formatted_string.replace(c, "")
		return formatted_string.lower()

	@staticmethod 
	def search_card_by_name(input_name):
		"""
		: Given a card's name, we search for it in our database and 
		: return the corresponding card object if there is a match.
		:
		: One tricky thing to account for is the appearance of "\" 
		: in the mtgtop8 data and also  
		: We use the format or removing spaces and all "\" chracters for now and will
		: audible if we need to define other formatting
		: 
		: Returns None if can't be found
		"""
		formatted_name = Card.format_card_name_for_search(input_name)
		search_card = Card.query.filter_by(search_name = formatted_name).first()
		return search_card



