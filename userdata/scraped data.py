import requests
from bs4 import BeautifulSoup 
import pandas as pd



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


url = input("Enter Hamariweb Qouites Web Link Here: ")

r = requests.get(url , headers=headers)

soup = BeautifulSoup(r.content , "html.parser")

Title = soup.find('h1')
print(Title.get_text())
quotestitle=Title.get_text()

# for https://hamariweb.com/mobiles/good_morning_sms_messages20/ datascrape

quotes = soup.find_all(class_= "quote_text")    

# for https://www.brainyquote.com/topics/life-quotes qoutes scrape

# quotes = soup.find_all(class_= "grid-item qb clearfix bqQt")

# for https://www.goodreads.com/quotes quotes scrape

# quotes = soup.find_all(class_= "quoteText")



# for https://www.fluentin3months.com/chinese-proverbs/ quotes scrape

# quotes = soup.find_all(class_= "wp-block-heading")

# for https://www.goodhousekeeping.com/life/g5080/life-quotes/ quotes scrape
# quotes = soup.find_all(class_= "css-18vfmjb et3p2gv0")

# for https://www.143greetings.com/goodluck/messages.html?utm_content=expand_article quotes scrape
# quotes = soup.find_all(class_= "message")




# for https://blog.rescuetime.com/time-management-quotes/ quotes scrape
# quotes = soup.find_all(class_ = "wp-block-quote")

# for https://www.fi.edu/en/benjamin-franklin/famous-quotes quotes scrape
# quotes = soup.find_all(dir="ltr")


# for https://www.berries.com/blog/positive-quotes quotes scrape
# quotes = soup.find_all(class_="has-text-align-center filter-box-quote")

# for https://www.keepinspiring.me/famous-quotes/ quotes scrape
# quotes = soup.find_all(class_="wp-block-quote is-style-large")
data = {quotestitle:[]}

for quote in quotes:
    # print(quote.get_text())
    if not quote.get_text() == '':
        para = quote.get_text()
        data[quotestitle].append(para)

df = pd.DataFrame.from_dict(data)
df.to_excel("data.xlsx",index=False)

# print(soup.get_text())
 
# print(soup.prettify())
# print(soup.get_text())
# title = soup.title
# print(title.get_text())
# paras = soup.find_all('p')
# print(paras)

# para = soup.find('p')
# print(para)


# Find all the elements with class lead 
# print(soup.find_all("p" , class_="lead"))

# Get the txext from the tags/soup
# print(soup.find('p').get_text())

# anchors = soup.find_all('a')
# all_links = set()
# print(anchors)


# for link in anchors:
#     if(link.get('href') != '#'):
#         linktext = "https://codewithharry.com" + link.get('href')
#         all_links.add(linktext)
#         print(linktext)


    # print(link.get('href'))  

# Comment 

# markup = "<p><!-- this is comment --></p>"
# soup2 = BeautifulSoup(markup)
# print(type(soup2.p.string))



# navbarsupportedcontent = soup.find(id ='imgpreview2' )
# for item in navbarsupportedcontent.contents:
#     print(item.name)

# for item in navbarsupportedcontent.strings:
#     print(item)

# print(navbarsupportedcontent.parent)
# print(navbarsupportedcontent.parents)

# for item in navbarsupportedcontent.parents:
#     print(item)

# for elem in navbarsupportedcontent.contents:
#     print(elem)


# print(navbarsupportedcontent.next_sibling)
# print(navbarsupportedcontent.previous_sibling)


# workin with css selector 
# elem = soup.select('.modal-footer')
# print(elem)