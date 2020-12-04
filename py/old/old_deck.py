



class Card:
	def __init__(self, name, quantity):
		"""
		: A card object in a deck is defined by its 
		: name - name of the card (str)
		: quantity - how many are in the deck (int)
		: main_deck - True if in the main_deck, False if sideboard (bool)
		"""
		self.name = name
		self.quantity = quantity

	def __str__(self):
		return  str(self.quantity) + " " + self.name

	def serialize(self):
		return {"quantity": self.quantity, "name": self.name}

class Deck:
	#def __init__(self, main_deck, sideboard, name, deck_format, date, event, num_players):
	def __init__(self, main_deck, sideboard, name = "Unnamed Deck"):	
		"""
		: Feel free to add more variables that you think might be 
		: important for a Deck object, I've just listed some basic ones 
		: for now.
		:
		: main_deck - cards in the main deck (list of card objects)
		: sideboard - cards in the sideboard (list of card objects)
		: name - name of the deck (str)
		: deck_format - format the deck is  (str)
		: event - name of event (str)
 		: date - date of event (str)
 		: num_players - number of players in the event (int)
		"""

		self.main_deck = main_deck
		self.sideboard = sideboard
		self.name = name
		"""
		self.deck_format = deck_format
		self.date = date
		self.event = event
		self.num_players = num_players
		"""
	def __str__(self):

		output_main_deck = []
		output_sideboard = []
		for card in self.main_deck:
			output_main_deck.append(str(card))

		for card in self.sideboard:
			output_sideboard.append(str(card))

		return "main deck\n" + "\n".join(output_main_deck) + "\n\nsideboard" + "\n".join(output_sideboard)

	def serialize(self):
		serialized_main_deck = []
		serialized_sideboard = []
		for card in self.main_deck:
			serialized_main_deck.append(card.serialize())
		for card in self.sideboard:
			serialized_sideboard.append(card.serialize())

		return [
		{"main deck": serialized_main_deck},
		{"sideboard": serialized_sideboard}
		]



class Collection:
	def __init__(self, name):
		"""
		: Magic card collection object
		: name - name of owner who owns this collection (str)
		: cards - cards in the users collection (dictionary of card objects) initialized to an empty dictionary
		: key is card name and value is quantity
		"""
		self.name = name
		self.cards = {}

	def size(self):
		"""
		: returns an integer with the number of cards in the collection
		"""
		size = 0
		for card_name in self.cards.keys():
			size += self.cards.get(card_name)
		return size

	def add_card(self, card):
		"""
		: adds this card and quantity to the collection
		: if the card already exists, we increment it's amount
		: return type: None
		"""
		pass

	def remove_card(self, card):
		"""
		: removes this card quantity pair from user's collection. 
		: If the collection doesn't have 
		"""
		pass

	def missing_cards_from_main_deck(self, deck):
		"""
		: Given a deck returns a tuple with 2 lists of 
		: card objects indicating which cards are missing 
		: from the main deck and sideboard
		: return type: tuple of list of cards
		"""
		output = []
		for card in deck.main_deck:
			if self.cards.get(card.name):
				if self.cards[card.name] < card.quantity:
					new_card = Card(card.name,card.quantity - self.cards[card.name])
					output.append(new_card)
			else:
				new_card = Card(card.name,card.quantity)
				output.append(new_card)	
		return output

	def missing_cards_from_sideboard(self, deck):
		"""
		: Given a deck returns a tuple with 2 lists of 
		: card objects indicating which cards are missing 
		: from the main deck and sideboard
		: return type: tuple of list of cards
		"""
		output = []
		for card in deck.sideboard:
			if self.cards.get(card.name):
				duplicate_offset = 0
				for possible_duplicate in deck.main_deck:
					if possible_duplicate.name == card.name:
						if self.cards.get(possible_duplicate.name) < possible_duplicate.quantity + card.quantity:
							if(possible_duplicate.quantity > self.cards.get(possible_duplicate.name)):
								duplicate_offset = self.cards.get(possible_duplicate.name)
							else:
								duplicate_offset = possible_duplicate.quantity
						break
				if self.cards[card.name] - duplicate_offset < card.quantity:
					new_card = Card(card.name,card.quantity - self.cards[card.name] + duplicate_offset)
					output.append(new_card)
			else:
				new_card = Card(card.name,card.quantity)
				output.append(new_card)	
		return output

	def has_deck(self, deck, missing_cards = 0):
		
		"""
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

		main_deck_missing_cards = self.missing_cards_from_main_deck(deck)
		sideboard_missing_cards = self.missing_cards_from_sideboard(deck)

		num_missing_md = 0
		num_missing_sb = 0

		for card in main_deck_missing_cards:
			num_missing_md += card.quantity

		for card in sideboard_missing_cards:
			num_missing_sb += card.quantity

		return (num_missing_md + num_missing_sb) <= missing_cards




	def remove_deck(self, deck):
		"""
		: for every card in the deck, remove each card and it's quantity
		: from the collection. If the collection doesn't have every card in the deck
		: then do nothing to the collection and return None. Otherwise return the deck object
		: return type: deck object
		"""
		
		if not self.has_deck(deck):
			return None

		for card in deck.main_deck:
			self.remove_card(card)

		for card in deck.sideboard:
			self.remove_card(card)

		return deck


	def add_deck(self, deck):
		"""
		: for every card in the deck, add each card and it's quantity
		: to this collection
		: No return value
		"""

		for card in deck.main_deck:
			self.add_card(card)

		for card in deck.sideboard:
			self.add_card(card)


# if __name__ == '__main__':
	
	"""
	my_collection = Collection("Dteam")

	for x in range(0,10):
		card_name = "card"
		card_name += str(x)
		new_card = Card(card_name,4)
		my_collection.add_card(new_card)

	a_main_deck = [] 
	for x in range(0,12):
		card_name = "card"
		card_name += str(x)
		new_card = Card(card_name,2)
		a_main_deck.append(new_card)

	a_side_board = []
	for x in range(5,8):
		card_name = "card"
		card_name += str(x)
		new_card = Card(card_name,1)
		a_side_board.append(new_card)

	my_deck = Deck(a_main_deck, a_side_board)
	"""
