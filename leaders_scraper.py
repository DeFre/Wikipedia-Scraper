import requests
from bs4 import BeautifulSoup
import re
import json

def get_leaders():
    """This function retrieves a dictionary of leaders from country-leaders.onrender.com inlcuding all leaders and all their information."""
    #define the urls
    root_url = "https://country-leaders.onrender.com/"
    status_url = root_url + "status"
    countries_url = root_url + "countries"
    cookie_url = root_url + "cookie"
    #get the cookies
    cookies = requests.get(cookie_url).cookies
    #get the countries
    countries = requests.get(countries_url, cookies=cookies).json()
    #loop over them and save their leaders in a dictionary
    for country in countries: 
        leaders_per_country.update({country:requests.get(leaders_url, params = {"country": country }, cookies=requests.get(cookie_url).cookies).json()})
    print(leaders_per_country)
    for country in leaders_per_country:
        for leader in leaders_per_country[country]:
            wikipedia_url = leader["wikipedia_url"]
            get_first_paragraph(wikipedia_url)
            leader.update({"first_paragraph": first_paragraph})
    return leaders_per_country

def get_first_paragraph(wikipedia_url):
    print(wikipedia_url) # keep this for the rest of the notebook
    leader_info = requests.get(wikipedia_url)
    #print(leader_info.text)
    soup = BeautifulSoup(leader_info.content, "html")
    #print(soup.prettify())
    paragraphs = soup.find_all("p")
    #print(paragraphs)
    global first_paragraph
    first_paragraph = "PLEASE CHECK: This string is displayed if no first_paragraph is found in the article. "
    for paragraph in paragraphs:
        if re.match("<p><b>", str(paragraph)):
            #first_paragraph = paragraph.text
            first_paragraph = re.sub("\[.\]", "", str(paragraph.text))
            #print("before breaking",first_paragraph)
            break
    #print("after breaking",first_paragraph)
    return first_paragraph



def save(leaders_per_country):
    with open('leaders.json', 'w') as output_file:
        json.dump(leaders_per_country, output_file)

get_leaders()
save(leaders_per_country)