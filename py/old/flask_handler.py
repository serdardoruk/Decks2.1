from flask import Flask, Response, request, jsonify, json
from deck import Collection,Deck,Card
from xls_parser import XlsParser

app = Flask(__name__, static_url_path='', static_folder = "../react/")
test_collection = Collection("TEST NAME")

@app.route('/')
def root():
	index = 'index.html'
	return app.send_static_file(index)


@app.route('/api/add_card', methods=['POST'])
def add_card():
	json_post = json.loads(request.data)
	return add_cards(json_post)

@app.route('/api/add_cards', methods=['POST'])
def add_cards(card_data = None):
	if card_data is None:
		json_post = json.loads(request.data)
	else:
		json_post = card_data
	#json_post = request.json // how a normal request would work

	#just going to add as many cards as were sent, instead of 1 card maximum
	for dictionary in json_post:
		card_quantity = 0
		card_name = None
		for key,value in dict.items(dictionary):
			if key == "quantity":
				card_quantity = value
			else:
				card_name = value

		test_collection.add_card(Card(card_name,int(card_quantity)))
	return jsonify(test_collection.__dict__)

@app.route('/api/remove_cards', methods=['DELETE'])
def remove_cards():
	json_post = json.loads(request.data)

	for dictionary in json_post:
		card_quantity = 0
		card_name = None
		for key,value in dict.items(dictionary):
			if key == "quantity":
				card_quantity = value
			else:
				card_name = value

		test_collection.remove_card(Card(card_name,int(card_quantity)))

	return jsonify(test_collection.__dict__) 


@app.route('/api/all_decks', methods=['GET'])
def all_decks():
	#return a a list of all decks that can be made from existing collection
	MISSING_CARDS = 3
	parser = XlsParser()
	list_of_decks = []
	for x in range(2,582):
		deck = parser.parse_deck(str(x))
		if test_collection.has_deck(deck,MISSING_CARDS):
			list_of_decks.append(deck.serialize())

	return jsonify(list_of_decks)



if __name__ == '__main__':
	pass
	#app.run(debug=True)
	#app.run()

