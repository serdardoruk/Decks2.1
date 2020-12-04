from bs4 import BeautifulSoup
import requests
import os, os.path
import time
import traceback
import xlwt
import urllib.parse as urlparse
from py.models.deck import Deck
from py.models.database import db

base_url = "http://www.mtgtop8.com/"
sample_deck_url = "http://www.mtgtop8.com/event?e=19012&d=319616&f=MO"
headers  = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



class Mtgtop8_Scraper:
	def get_soup_from_url(self, url):
		response = requests.get(url, headers = headers)
		soup = BeautifulSoup(str(response.content), 'html.parser')
		return soup


	def get_deck_urls_from_archetype_page(self, archetype_url):
		"""
		: Given an archetype url such as 
		: "http://www.mtgtop8.com/archetype?a=183&f=MO"
		: returns the a list of urls of the first 20 decks
		"""
		soup = self.get_soup_from_url(archetype_url)
		deck_list_table = soup.find_all("table", {"class": "Stable"})
		deck_rows = deck_list_table[1].find_all("tr", {"class" : "hover_tr"})
		output_urls = []
		for deck in deck_rows:
			deck_cols = deck.find_all("td")
			deck_link = deck_cols[1].find("a")
			if deck_link:
				output_urls.append(base_url + deck_link['href'])
		return output_urls


	def get_archetype_urls_from_main_page(self, main_page_url):
		"""
		: Given the format summary page for a url such as 
		: "http://www.mtgtop8.com/format?f=MO"
		: returns the a list of urls of the first 20 decks
		"""
		soup = self.get_soup_from_url(main_page_url)
		deck_type_table = soup.find_all("table", {"class": "Stable"})[0]
		deck_type_rows = deck_type_table.find_all("tr", {"class" : "hover_tr"})
		archetype_links = []
		for row in deck_type_rows:
			link = row.find("td").find("a")
			archetype_links.append((base_url + link['href'], link.text))
		return archetype_links

	def save_deck_list(self, deck_url):
		

		try:
			parsed = urlparse.urlparse(deck_url)
			event_id = urlparse.parse_qs(parsed.query)['e'][0]
			deck_id = urlparse.parse_qs(parsed.query)['d'][0]
			url = deck_url
			soup = self.get_soup_from_url(deck_url)
			#scrape tournament data about the deck
			tourney_soup = soup.find_all("div", {"class": "w_title"})

			# find the archetype
			archetype_table = soup.find_all("table", {"border" : "0", "width": "100%"})[2].find_all("td")[2]
			# .find("table")
			# .find_all("td")[2]

			archetype = archetype_table.text
			# print(archetype_table.findChildren())

			tourney_soup = tourney_soup[0].find_all("td")
			tourney_info = {}
			temp = soup.find_all("table", {"class": "Stable"})
			temp = temp[0].find_all("div")
			mtg_format = temp[1].parent.contents[0]
			players_tag = temp[1].parent.contents[2]
			mtg_format = mtg_format[4:]
			index = players_tag.find(" - ")
			if index != -1:
				num_players = players_tag[:index]
				tourney_date = players_tag[index + 2:]
			else:
				num_players = None
				tourney_date = players_tag
			tourney_info['url'] = deck_url
			tourney_info['event_format'] = mtg_format
			tourney_info['event_name'] = tourney_soup[0].text
			tourney_info['num_players'] = num_players
			tourney_info['event_date'] = tourney_date
			tourney_info['deck_id'] = deck_id
			tourney_info['event_id'] = event_id

			# tourney_info['archetype'] = archetype
			# ex: tourney_soup[1].text = #2Humans - bernardocssa
			# get the deck name and the archetype
			deck_summary  = tourney_soup[1]

			tourney_info['event_placing'] = deck_summary.contents[0].split(" ")[0]
			tourney_info['deck_name'] = "".join(deck_summary.contents[0].split(" ")[1:])

			tourney_info['player'] = deck_summary.find("a").text
			tourney_info['archetype'] = "".join(archetype.split(" ")[:-1])
			

			# scrape decklist data - maindeck and sideboard
			test = soup.find_all("table", {"class": "Stable"})
			test1 = test[1].find_all("div", {"class": "hover_tr"})
			result = []
			for x in test1:
				card_and_num = []
				card_and_num.append(x.text[0])
				#because sideboard cards have a leading whitespace i am checking for it and offsetting by 1
				maindeck = 1
				if(x.text[2] is " "):
					maindeck = 0
				card_and_num.append(x.text[3 - maindeck:])
				card_and_num.append(maindeck)
				result.append(card_and_num)
			book = xlwt.Workbook()
			sh = book.add_sheet("TODO-info on deck")
			column = 0
			count = 0
			for key, item in tourney_info.items():
				sh.write(count, 0, key)
				sh.write(count, 1, item)
				count += 1
			sh.write(count,0,"Quantity")
			sh.write(count,1,"Card Name")
			sh.write(count,2,"Main Deck")
			count += 1
			for x in result:
				sh.write(count,0,x[0])
				sh.write(count,1,x[1])
				sh.write(count,2,x[2])
				count += 1
			path = "./py/data/deck_data"
			# num_decks = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
			# deck_name = str(num_decks+1)
			book.save(path + "/" + deck_id + ".xls")
			return 1
		except Exception as e:
			traceback.print_exc()
			return -1

	def save_modern_decks(self):
		self.save_modern_deck_urls()
		self.save_modern_decks_fast()


	def save_modern_deck_urls(self, LIMIT = None):
		main_page_url = "http://www.mtgtop8.com/format?f=MO"
		archetype_links = self.get_archetype_urls_from_main_page(main_page_url)
		all_deck_links = []
		i = 0
		print(i)
		for archetype_link in archetype_links:
			deck_links = self.get_deck_urls_from_archetype_page(archetype_link[0])
			for deck_link in deck_links:
				all_deck_links.append((deck_link, archetype_link[1]))
				i += 1
				print(i)
			if i > limit:
				break

		with open("./py/logs/deck_links.log", "w") as f:
			for link in all_deck_links:
				f.write(link[0] + "\n")



	def save_modern_decks_fast(self, LIMIT = None):
		"""
		: Needs deck_links.log to be filled out to
		: to save the decks 
		"""
		print('save_modern_decks_fast')
		with open("./py/logs/deck_links.log", "r") as f:
			links = f.read().split("\n")

		print('next...')
		if LIMIT:
			print('limit')
			for x in links[0:LIMIT]:
				print('saving...')
				self.save_deck_list(x)
		else:
			for x in links[0: len(links)-1]:
				print('why we here...')
				self.save_deck_list(x)


if __name__ == "__main__":
	
	scraper = Mtgtop8_Scraper()
	time_0 = time.time()
	# scraper.save_modern_deck_urls()
	# scraper.save_modern_decks()
	scraper.save_modern_decks_fast()
	print(time.time() - time_0)


