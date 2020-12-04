# import os
# import unittest

# from flask import render_template, json
# from deck import Card, Collection


# class RouteTests(unittest.TestCase):

# 	@classmethod
# 	def setUpClass(cls):
# 		pass 

# 	@classmethod
# 	def tearDownClass(cls):
# 		pass 

# 	def setUp(self):
# 		self.test_collection = Collection("TEST NAME")
# 		# creates a test client
# 		self.app = app.test_client()
# 		# propagate the exceptions to the test client
# 		self.app.testing = True 

# 	def tearDown(self):
# 		pass 

# 	def test_home_status_code(self):
# 		# sends HTTP GET request to the application
# 		# on the specified path
# 		result = self.app.get('/') 

# 		# assert the status code of the response
# 		self.assertEqual(result.status_code, 200) 


# 	def test_create_account(self):
# 		test_account = {
# 			"username" : "TEST_USERNAME",
# 			"password" : "password"
# 		}


# 		json_str = jsonify(test_account)

# 		rv = self.app.post('/api/create_account', data=json_str)
# 		self.assertEqual(rv.status_code, 200)

# 		"""
# 		: Assert the following
# 		: If an account is created, but an account with same username exists do not create the account
# 		: The account was actually created and stored in the database (is not None)
# 		: The account's information matches the username and password
# 		: The account's collection is empty
# 		"""
		

# 	def test_login_account(self):
# 		"""
# 		: 1. Create an account with sample credentials
# 		: 2. Attempt the login 
# 		"""

# 		# create test account here 
# 		# test_account = {
# 		# 	"username" : "TEST_USERNAME",
# 		# 	"password" : "password"
# 		# }

# 		bad_login = {
# 			"username": "TEST_USERNAME",
# 			"password" : "bad_password",
# 		}

# 		json_str = jsonify(bad_login)
# 		rv = self.app.post('/api/login', data=json_str)
# 		self.assertEqual(rv.status_code, 200)
# 		# Assert that the response is not a login response with the user object

# 		good_login = {
# 			"username": "TEST_USERNAME",
# 			"password" : "bad_password",
# 		}

# 		json_str = jsonify(good_login)
# 		rv = self.app.post('/api/login', data=json_str)
# 		self.assertEqual(rv.status_code, 200)
# 		self.assertEqual(rv.data.user.username, good_login['username'])


# 	def test_add_card_to_collection(self):
# 		"""
# 		: Given a user credentials (either as JWT or as username), card_id and quantity, 
# 		: adds the card / quantity to the user's collection
# 		: Assert that the collection was succesfully updated
# 		"""
# 		pass

# 	def test_remove_card_from_collection(self):
# 		"""
# 		: Given a user credentials (either as JWT or as username), card_id and quantity, 
# 		: removes the card / quantity from the user's collection
# 		: Assert that the collection was succesfully updated
# 		"""
# 		pass

# 	def test_get_user_info(self):
# 		"""
# 		: Given user credentials, returns the user information
# 		: Assert the information is correct
# 		: Assert that no information is returned when credentials are wrong
# 		"""
# 		pass


	

