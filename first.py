from flask import Flask, request, render_template, json, g, redirect, url_for
from bs4 import BeautifulSoup as bs
import urllib3
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismysupersecrectkey'
app.debug = True

listRegions = {'Rivne':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D1%96%D0%B2%D0%BD%D0%B5%D0%BD%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Volyn':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D0%BE%D0%BB%D0%B8%D0%BD%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Zhtomyr':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D0%B8%D1%82%D0%BE%D0%BC%D0%B8%D1%80%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Zakarpatia':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D0%B0%D0%BA%D0%B0%D1%80%D0%BF%D0%B0%D1%82%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'IfFrankivsk':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D1%80%D0%B0%D0%BD%D0%BA%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Lvivska':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Ternopil':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D0%B5%D1%80%D0%BD%D0%BE%D0%BF%D1%96%D0%BB%D1%8C%D1%81%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Khmelinytski':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number=',
'Chenivtsi':'http://www.msp.gov.ua/children/search.php?form=%D0%9D%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B5+%D1%83%D1%81%D0%B8%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F&male=%D0%96%D1%96%D0%BD%D0%BE%D1%87%D0%B0&age_from=1&age_to=5&region=%D0%B5%D1%80%D0%BD%D1%96%D0%B2%D0%B5%D1%86%D1%8C%D0%BA%D0%B0&brothers=no&needs=no&number='}

@app.route("/baby")
def main():
	myDict = {}
	for key in listRegions:
		mySubList = scrape(listRegions[key]);
		print(key)
		myDict[key]=mySubList;
	
	#return 'hello world'
	return render_template("baby.html",dict = myDict);
	
	
def scrape(parURL):
	http = urllib3.PoolManager()

	r = http.request('GET', parURL)
	if r.status != 200:
		return False

	soup = bs(r.data)
	myList = []
	
	for anchor in soup.findAll('div', {'class': 'child__item-img'}):
		anchor = str(anchor)
		anchor = anchor.replace("'","");
		pos1 = anchor.find("url(..")+6
		pos2 = anchor.find(".jpeg")+5
		anchor = anchor[pos1:pos2]
		myList.append(anchor)

	return myList
	
if __name__ == '__main__':
	url = 'http://127.0.0.1:5000/baby'
	webbrowser.open_new(url)
	app.run(debug=True)
	
