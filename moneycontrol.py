import requests
from bs4 import BeautifulSoup
import time
import pymysql.cursors

def get_list():
	file = open('incode.txt','r')
	i = 0
	
	for f in file:
		try:
			code = str(f)
			base_url = 'http://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str=' + str(code)
			print (base_url)
			response = requests.get(base_url)
			html = BeautifulSoup(response.content, 'html.parser')

			h1 = html.find('h1',{'class':'b_42 company_name'})
			if h1:
				company_name = h1.text.strip()
				print (company_name)
				nse = html.find('span',{'id':'Nse_Prc_tick'})
				if nse:
					nse_price =nse.text.strip()
				previous = html.find('div',{'id':'n_prevclose'})
				if previous:
					previous_price = previous.text.strip()
				open_price = html.find('div',{'id':'n_open'})
				if open_price:
					open_p = open_price.text.strip()
				try:
					connection = pymysql.connect(host= "localhost",
			                  user="root",
			                  passwd="Ramesh!197",
			                  db="money_control",
			                  charset='utf8mb4',
		                      cursorclass=pymysql.cursors.DictCursor)
					try:
						with connection.cursor() as cursor:
							sql = 'SELECT * FROM stock_rates WHERE isin_code=%s'
							cursor.execute(sql, (code,))
							result = cursor.fetchone()
							if result:
								cursor.execute ("UPDATE stock_rates SET nse_value=%s, previous_close=%s, open_price=%s WHERE isin_code=%s", (nse_price,previous_price,open_p,code))
								connection.commit()
								print ("Updated")
							else:
								cursor.execute("INSERT INTO stock_rates (company_name,isin_code,nse_value,previous_close,open_price) VALUES (%s,%s,%s,%s,%s)", (company_name,code,nse_price,previous_price,open_p))
								connection.commit()
								print ("Inserted")
					except:
						print ('Failed Query')
					finally:
						connection.close()
				except pymysql.Error as e:
					print ("ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1]))



		except:
			print("Connection refused by the server..")
			print("Let me sleep for 2 seconds")
			print("ZZzzzz...")
			time.sleep(2)
			print("Was a nice sleep, now let me continue...")
			continue

if __name__ == '__main__':
	get_list()