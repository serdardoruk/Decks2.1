from flask import Blueprint, jsonify, request
from py.models.user import User

from functools import wraps


def check_user_jwt(func):
	@wraps(func)
	def wrapper():
		jwt = request.json.get('jwt')
		this_user = User.decode_jwt(jwt)
		if this_user == None:
			return jsonify({
					"success" : False
				})
		return func(this_user)
	return wrapper