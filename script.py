from bs4 import BeautifulSoup #html parser
import requests #obtains webpage

url = "https://www.newegg.ca/p/pl?d=graphics+cards&N=601408872%20100007708" 
webpage= requests.get(url)
document = BeautifulSoup(webpage.text, "html.parser")

# Find how many pages there are:
pages = document.find(class_="list-tool-pagination-text").strong #<strong>1<!-- -->/<!-- -->6</strong>

#Split string to obtain: <strong>1<!-- --> , <!-- -->6<, strong>
# [1] obtains <!-- -->6<
# split(">")[-1][:-1] obtains 6
number_of_pages = int(str(pages).split("/")[1].split(">")[-1][:-1])


#Begin writing to csv file:
stats = "stats.csv"
f = open(stats, "a")
categories = "Brand, Description, Cost, Rating\n"
f.write(categories)

def record_gpus(gpus):
    for gpu in gpus:
       # Some brands are not listed:
       try:
           brand = (gpu.find_all(class_="item-brand"))[0].img["title"]
       except:
           brand = "N/A"
       
       description = (gpu.find_all(class_="item-title"))[0].text

       price_dollars = (gpu.find_all(class_="price-current"))[0].strong.text
       price_cents = (gpu.find_all(class_="price-current"))[0].sup.text 
       price = "$" + price_dollars + price_cents
       
       # Some ratings are not listed
       try:
           rating= gpu.find_all(class_="item-rating")[0]["title"].split("+")[-1].strip()
       except:
           rating = "N/A"
       
       gpu_stats = brand.replace(",", " ") + "," + description.replace(",", " ") + "," + price.replace(",", " ") + "," + rating + "\n"
       f.write(gpu_stats)
    
           
for page in range(1, number_of_pages+1):
    url = f'https://www.newegg.ca/p/pl?d=graphics+cards&N=601408872%20100007708&page={page}'
    webpage= requests.get(url)
    document = BeautifulSoup(webpage.text, "html.parser")

    gpus = document.find_all(class_="item-container")

    record_gpus(gpus)

f.close()