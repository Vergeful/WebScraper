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
        try:
            brand = (((gpu.a).next_sibling).div.a.img)["title"]
        except:
            try:
                brand = (((((gpu.a).next_sibling).div).next_sibling).a.img)["title"]
            except:
                pass
        
        
        description = (((gpu.a).next_sibling).div).next_sibling.text
        if(len(description) <= 7):
            description = ((((gpu.a).next_sibling).div).next_sibling).next_sibling.text

        price_dollar = (((((gpu.a).next_sibling).next_sibling).ul.li).next_sibling).next_sibling.strong.text
        price_cents = (((((gpu.a).next_sibling).next_sibling).ul.li).next_sibling).next_sibling.sup.text
        price = "$" + price_dollar + price_cents


        try:
            rating = ((((((gpu.a).next_sibling).div).next_sibling).a).next_sibling)["title"].split("+")[-1].strip()
        except:
            try:
                rating = (((((gpu.a).next_sibling).div).a).next_sibling)["title"].split("+")[-1].strip()
            except:
                pass
        
        try:
            gpu_stats = brand.replace(",", " ") + "," + description.replace(",", " ") + "," + price.replace(",", " ") + "," + rating + "\n"
            f.write(gpu_stats)
        except:
            pass
   
           
for page in range(1, number_of_pages+1):
    url = f'https://www.newegg.ca/p/pl?d=graphics+cards&N=601408872%20100007708&page={page}'
    webpage= requests.get(url)
    document = BeautifulSoup(webpage.text, "html.parser")

    gpus = document.find_all(class_="item-container")

    record_gpus(gpus)

f.close()





# gpu = document.find_all(class_="item-container")[5]
# f = open("stats.csv", "a")

#Brand: 
# Try except block used if container has lowest price div:
# try:
#     brand_name = ((gpu.a).next_sibling).div.a.img
#     f.write(brand_name["title"])
# except:
#     brand_name = ((((gpu.a).next_sibling).div).next_sibling).a.img
#     f.write(brand_name["title"])

# Item description:

# If the container has the lowest price div, the description is number of ratings i.e. (22).
# Assume that this string is <= 7 characters
# description = (((gpu.a).next_sibling).div).next_sibling.text
# if(len(description) <= 7):
#     description = ((((gpu.a).next_sibling).div).next_sibling).next_sibling.text


# print(description)

#Price:
# price_dollar = (((((gpu.a).next_sibling).next_sibling).ul.li).next_sibling).next_sibling.strong.text
# price_cents = (((((gpu.a).next_sibling).next_sibling).ul.li).next_sibling).next_sibling.sup.text
# print("$" + price_dollar + price_cents)

#Rating:
# try:
#     rating = ((((((gpu.a).next_sibling).div).next_sibling).a).next_sibling)["title"].split("+")[-1].strip()
#     print(rating)
# except:
#     rating = (((((gpu.a).next_sibling).div).a).next_sibling)["title"].split("+")[-1].strip()
#     print(rating)