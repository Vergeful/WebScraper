from bs4 import BeautifulSoup #html parser
import requests #obtains webpage
import re #regex expressions for obtaining patterns

webpage = "https://www.newegg.ca/p/pl?d=graphics+cards&N=601408872%20100007708" 
webpage_data = requests.get(webpage)

document = BeautifulSoup(webpage_data.text, "html.parser")

sample = document.find_all("div", {"class":"item-container"})[0]
f  = open("sample_container.html", "w")
f.write(sample.prettify())