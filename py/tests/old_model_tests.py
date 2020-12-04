"""import random
import unittest
from deck import Collection,Deck,Card
from xls_parser import XlsParser



TEST_COLLECTION_NAME = "DTEAM"

class TestCollectionMethods(unittest.TestCase):

	def test_add_card(self):
		test_collection = Collection(TEST_COLLECTION_NAME)

		# assert the collection starts at size 0
		self.assertEqual(test_collection.size(), 0)

		# assert that adding a card with no quantity doesn't
		# update the size of the collection
		zero_card = Card("card0", 0)
		test_collection.add_card(zero_card)
		self.assertEqual(test_collection.size(), 0)

		# add cards with random non-negative quantities
		# and assert the new size of the collection
		running_size = 0
		for x in range(0, 100):
			quantity = random.randint(0,20)
			# we divide by 2 so we add the same card name twice 
			card = Card("card" + str(x // 2), quantity)
			test_collection.add_card(card)
			running_size += quantity
			self.assertEqual(test_collection.size(), running_size)


		
	def test_remove_card(self):
		test_collection = Collection(TEST_COLLECTION_NAME)

		#assert the collection starts at size 0
		self.assertEqual(test_collection.size(), 0)

		#assert that trying to remove a card from an empty collection
		#that nothing happens
		for x in range(0,100):
			card = Card("card" +str(x), random.randint(0,10) - 10)
			test_collection.remove_card(card)
			self.assertEqual(test_collection.size(), 0)

		#populate the collection and keep track of size
		running_size = 0
		for x in range(0, 100):
			quantity = random.randint(0,20)
			card = Card("card" + str(x), quantity)
			test_collection.add_card(card)
			running_size += quantity
			self.assertEqual(test_collection.size(), running_size)


		# remove cards with random quantities - including negative
		# if quantity is <= 0 running size should stay the same
		# if quantity is > collection[cardname] running size should stay the same
		# else decrement running size by quantity
		for x in range(0,250):
			quantity = random.randint(0,50) - 20
			card = Card("card" +str(x//2), quantity)

			#do nothing if trying to remove a negative quantity, or trying to remove a card not in dict
			#or if trying to remove a quantity greater than the quantity in dict
			if (quantity < 1) or (not test_collection.cards.get(card.name)) or (test_collection.cards.get(card.name) < quantity):
				pass
			else:
				running_size -= quantity

			test_collection.remove_card(card)

			self.assertEqual(test_collection.size(), running_size)
		
	def test_missing_cards_from_main_deck(self):

		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		test_main_deck = []
		empty_sideboard =[]
		CARDS_IN_MAIN_DECK = 25
		ARBITRARY_NUMBER = 5 #must be less than CARDS_IN_MAIN_DECK


		for x in range(0,CARDS_IN_MAIN_DECK):
			quantity = random.randint(1,4)
			card = Card("card"+str(x),quantity)
			test_main_deck.append(card)

		test_deck = Deck(test_main_deck,empty_sideboard)

		#an empty collection should be missing every card from a maindeck
		cards_missing_from_main_deck = test_collection.missing_cards_from_main_deck(test_deck)
		
		#assert that return list is of equal length to deck
		self.assertEqual(len(cards_missing_from_main_deck),CARDS_IN_MAIN_DECK)
		index = 0
		for card in cards_missing_from_main_deck:
			#assert that return list has a list of cards equivalent to main deck
			self.assertEqual(card.name,test_deck.main_deck[index].name)
			self.assertEqual(card.quantity,test_deck.main_deck[index].quantity)
			index += 1


		#a "full" collection should be missing no card from a maindeck
		for x in range(0,CARDS_IN_MAIN_DECK+CARDS_IN_MAIN_DECK):
			quantity = random.randint(4,10)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)

		cards_missing_from_main_deck = test_collection.missing_cards_from_main_deck(test_deck)
		self.assertEqual(len(cards_missing_from_main_deck),0)

		#a "partially full" collection should be missing some cards from a maindeck
		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		
		for x in range(0,CARDS_IN_MAIN_DECK - ARBITRARY_NUMBER):
			quantity = random.randint(0,2)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)
		cards_missing_from_main_deck = test_collection.missing_cards_from_main_deck(test_deck)

		index = 0
		for card in test_deck.main_deck:
			if not test_collection.cards.get(card.name):
				self.assertEqual(cards_missing_from_main_deck[index].name,card.name)
				self.assertEqual(cards_missing_from_main_deck[index].quantity,card.quantity)
				index += 1
			elif test_collection.cards.get(card.name) < card.quantity:
				self.assertEqual(cards_missing_from_main_deck[index].name,card.name)
				self.assertEqual(cards_missing_from_main_deck[index].quantity,card.quantity - test_collection.cards.get(card.name))
				index += 1


	def test_missing_cards_from_sideboard(self):
		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		empty_main_deck = []
		test_sideboard =[]
		CARDS_IN_SIDEBOARD = 25
		ARBITRARY_NUMBER = 5 #must be less than CARDS_IN_SIDEBOARD

		for x in range(0,CARDS_IN_SIDEBOARD):
			quantity = random.randint(1,4)
			card = Card("card"+str(x),quantity)
			test_sideboard.append(card)

		test_deck = Deck(empty_main_deck,test_sideboard)

		#an empty collection should be missing every card
		cards_missing_from_sideboard = test_collection.missing_cards_from_sideboard(test_deck)
		
		#assert that return list is of equal length to deck
		self.assertEqual(len(cards_missing_from_sideboard),CARDS_IN_SIDEBOARD)
		index = 0
		for card in cards_missing_from_sideboard:
			#assert that return list has a list of cards equivalent to sideboard
			self.assertEqual(card.name,test_deck.sideboard[index].name)
			self.assertEqual(card.quantity,test_deck.sideboard[index].quantity)
			index += 1


		#a "full" collection should be missing no cards
		for x in range(0,CARDS_IN_SIDEBOARD+CARDS_IN_SIDEBOARD):
			quantity = random.randint(4,10)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)

		cards_missing_from_sideboard = test_collection.missing_cards_from_main_deck(test_deck)
		self.assertEqual(len(cards_missing_from_sideboard),0)

		#a "partially full" collection should be missing some cards
		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		
		for x in range(0,CARDS_IN_SIDEBOARD - ARBITRARY_NUMBER):
			quantity = random.randint(0,2)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)
		
		cards_missing_from_sideboard = test_collection.missing_cards_from_sideboard(test_deck)

		index = 0
		for card in test_deck.sideboard:
			if not test_collection.cards.get(card.name):
				self.assertEqual(cards_missing_from_sideboard[index].name,card.name)
				self.assertEqual(cards_missing_from_sideboard[index].quantity,card.quantity)
				index += 1
			elif test_collection.cards.get(card.name) < card.quantity:
				self.assertEqual(cards_missing_from_sideboard[index].name,card.name)
				self.assertEqual(cards_missing_from_sideboard[index].quantity,card.quantity - test_collection.cards.get(card.name))
				index += 1

		#test when cards are overlapping from sideboard and maindeck
		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		test_sideboard = []
		test_main_deck = []

		#populate collection
		for x in range(0,1000):
			quantity = random.randint(1,20)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)

		#populate sideboard
		for x in range(0,1000):
			quantity = random.randint(1,10)
			card = Card("card"+str(x),quantity)
			test_sideboard.append(card)

		#populate maindeck
		for x in range(0,1000):
			quantity = random.randint(1,10)
			card = Card("card"+str(x),quantity)
			test_main_deck.append(card)
		self.assertEqual(len(test_sideboard),1000)
		self.assertEqual(len(test_main_deck),1000)
		test_deck = Deck(test_main_deck, test_sideboard)
		cards_missing_from_sideboard = test_collection.missing_cards_from_sideboard(test_deck)
		cards_missing_from_main_deck = test_collection.missing_cards_from_main_deck(test_deck)
		sideboard_index = 0
		main_deck_index = 0

		#quantity in collection + cards_missing_from_main_deck + cards_missing_from_sideboard (cmm)
		# = main_deck + sideboard
		#if quanitity in collection < quantity main + quantity board
		md_bounds = len(cards_missing_from_main_deck)
		sb_bounds = len(cards_missing_from_sideboard)
		for x in range(0,1000):
			current_card = "card"+str(x)
			cmm_quantity = 0
			tmp_side = 0
			tmp_main = 0
			if sideboard_index < sb_bounds:
				if cards_missing_from_sideboard[sideboard_index].name == current_card:
					tmp_side = cards_missing_from_sideboard[sideboard_index].quantity
					cmm_quantity += cards_missing_from_sideboard[sideboard_index].quantity
					sideboard_index += 1

			if main_deck_index < md_bounds:
				if cards_missing_from_main_deck[main_deck_index].name == current_card:
					tmp_main = cards_missing_from_main_deck[main_deck_index].quantity
					cmm_quantity += cards_missing_from_main_deck[main_deck_index].quantity
					main_deck_index += 1
			if test_collection.cards.get(current_card) >= (test_deck.main_deck[x].quantity+test_deck.sideboard[x].quantity):
				pass
			else:
				self.assertEqual(test_collection.cards.get(current_card)+cmm_quantity,test_deck.main_deck[x].quantity+test_deck.sideboard[x].quantity)






	def test_has_deck(self):
		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		
		main_deck = []
		sideboard =[]
		CARDS_IN_MAIN_DECK = 100
		CARDS_IN_SIDEBOARD = 50
		ARBITRARY_NUMBER = 5 


		for x in range(0,CARDS_IN_MAIN_DECK):
			quantity = random.randint(1,4)
			card = Card("card"+str(x),quantity)
			main_deck.append(card)

		for x in range(CARDS_IN_MAIN_DECK//2,CARDS_IN_SIDEBOARD+CARDS_IN_MAIN_DECK//2):
			quantity = random.randint(1,4)
			card = Card("card"+str(x),quantity)
			sideboard.append(card)

		test_deck = Deck(main_deck,sideboard)

		#assert empty collection doesn't contain deck
		self.assertEqual(test_collection.has_deck(test_deck),False)


		for x in range(0,CARDS_IN_MAIN_DECK//2+CARDS_IN_SIDEBOARD):
			quantity = random.randint(10,10)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)

		self.assertEqual(test_collection.has_deck(test_deck),True)


		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)

		
		for x in range(0,CARDS_IN_MAIN_DECK//2+CARDS_IN_SIDEBOARD):
			quantity = random.randint(4,4)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)

		#assert collection that has less than required number of cards doesnt contain deck
		self.assertEqual(test_collection.has_deck(test_deck),False)



	def test_remove_deck(self):
		
		test_collection = Collection(TEST_COLLECTION_NAME)
		self.assertEqual(test_collection.size(), 0)
		
		main_deck = []
		sideboard =[]
		CARDS_IN_MAIN_DECK = 100
		CARDS_IN_SIDEBOARD = 50
		ARBITRARY_NUMBER = 1000 
		deck_size = 0
		collection_size = 0


		for x in range(0,CARDS_IN_MAIN_DECK):
			quantity = random.randint(1,2)
			card = Card("card"+str(x),quantity)
			main_deck.append(card)
			deck_size+=quantity

		for x in range(CARDS_IN_MAIN_DECK//2,CARDS_IN_SIDEBOARD+CARDS_IN_MAIN_DECK//2):
			quantity = random.randint(1,2)
			card = Card("card"+str(x),quantity)
			sideboard.append(card)
			deck_size+=quantity

		test_deck = Deck(main_deck,sideboard)

		#assert cant remove from empty collection
		self.assertEqual(test_collection.remove_deck(test_deck),None)


		for x in range(0,CARDS_IN_MAIN_DECK//2+CARDS_IN_SIDEBOARD):
			quantity = random.randint(ARBITRARY_NUMBER,ARBITRARY_NUMBER)
			card = Card("card"+str(x),quantity)
			test_collection.add_card(card)
			collection_size += quantity


		self.assertEqual(test_collection.size(), collection_size)
		test_collection.remove_deck(test_deck)

		self.assertEqual(test_collection.size(), collection_size - deck_size)
		collection_size = test_collection.size()

		flag_removed_success = True
		max_loops = ARBITRARY_NUMBER//2 #to break loop incase future implementation breaks something
		loop_num = 0
		while(flag_removed_success and loop_num < max_loops):
			loop_num += 1
			removed_or_not = test_collection.remove_deck(test_deck)
			if removed_or_not is None:
				flag_removed_success = False
			if flag_removed_success:
				collection_size -= deck_size
				self.assertEqual(test_collection.size(), collection_size)
			else:
				self.assertEqual(test_collection.size(), collection_size)



if __name__ == "__main__":
	unittest.main()
"""