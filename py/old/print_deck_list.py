from bs4 import BeautifulSoup
import requests
import xlwt
import os, os.path

def get_deck_list(deck_url):
	
	try:
		url = deck_url

		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		r = requests.get(url, headers=headers)

		soup = BeautifulSoup(str(r.content), 'html.parser')

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

		path = "./decks"
		num_decks = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
		deck_name = str(num_decks+1)
		book.save(path+"/"+deck_name+".xls")

		return 1

	
	except:
		return -1