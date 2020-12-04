from bs4 import BeautifulSoup
import requests
import xlwt
import os, os.path
import time

base_url = "http://www.mtgtop8.com/"
deck_url = "http://www.mtgtop8.com/event?e=19012&d=319616&f=MO"
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
			url = deck_url
			soup = self.get_soup_from_url(deck_url)
			#scrape tournament data about the deck
			tourney_soup = soup.find_all("div", {"class": "w_title"})
			tourney_soup = tourney_soup[0].find_all("td")
			tourney_info = []
			temp = soup.find_all("table", {"class": "Stable"})
			temp = temp[0].find_all("div")
			mtg_format = temp[1].parent.contents[0]
			num_players = temp[1].parent.contents[2]
			mtg_format = mtg_format[4:]
			index = num_players.find(" - ")
			num_players = num_players[:index]
			tourney_info.append(mtg_format)
			for x in tourney_soup:
				tourney_info.append(x.text)
			tourney_info.append(num_players)
			#scrape decklist data - maindeck and sideboard
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
			for info in tourney_info:
				sh.write(count,column,info)
				column += 1
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
			path = "./deck_data"
			num_decks = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
			deck_name = str(num_decks+1)
			book.save(path+"/"+deck_name+".xls")
			return 1
		except Exception as e:
			print(e)
			return -1

	def save_modern_decks(self):
		main_page_url = "http://www.mtgtop8.com/format?f=MO"
		archetype_links = self.get_archetype_urls_from_main_page(main_page_url)
		all_deck_links = []
		for archetype_link in archetype_links:
			deck_links = self.get_deck_urls_from_archetype_page(archetype_link[0])
			for deck_link in deck_links:
				all_deck_links.append((deck_link, archetype_link[1]))
		for deck_link in all_deck_links:
			x = self.save_deck_list(deck_link[0])

	def save_modern_decks_fast(self):
		with open("./logs/deck_links.log", "r") as f:
			links = f.read().split("\n")
		for x in links:
			self.save_deck_list(x)





if __name__ == "__main__":
	
	scraper = Mtgtop8_Scraper()
	time_0 = time.time()
	scraper.save_modern_decks()
	print(time.time() - time_0)


