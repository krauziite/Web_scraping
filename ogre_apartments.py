"""
This is ss.com web scraping project for Ogre city apartments
The main purpose is to extract data from advertisements such as price, rooms, sqm, street etc.
The result will be saved in a text file apartments_ogre.txt

"""
import re
import requests
from bs4 import BeautifulSoup


dzivokli_ogre = "https://www.ss.com/lv/real-estate/flats/ogre-and-reg/sell/"


def scrape_website():
    """ Main function of module calls all sub-functions"""
    ogre_listing = get_bs_object(dzivokli_ogre)
    listing_nr = find_single_page_urls(ogre_listing)
    print("found " + str(len(listing_nr)) + " listings ...")
    extract_data_from_url(listing_nr, "ogre_apartments.txt")


def extract_data_from_url(nondup_urls: list, dest_file: str) ->None:
    """Iterate over all first page msg urls extract info from each url and write to file """
    msg_url_count = len(nondup_urls)
    for i in range(msg_url_count):
        current_msg_url = nondup_urls[i] + "\n"
        table_opt_names = get_msg_table_info(nondup_urls[i], "ads_opt_name")
        table_opt_values = get_msg_table_info(nondup_urls[i], "ads_opt")
        table_price = get_msg_table_info(nondup_urls[i], "ads_price")

        print("extracting data from url ", i + 1)
        write_line(current_msg_url, dest_file)
        for idx in range(len(table_opt_names) - 1):
            text_line = table_opt_names[idx] + " " + table_opt_values[idx] + "\n"
            write_line(text_line, dest_file)

        # Extract message price field
        price_line = "Price: " + table_price[0] + "\n"
        write_line(price_line, dest_file)


def get_bs_object(page_url: str):
    """ This function loads webpage from url and returns bs4 object"""
    page = requests.get(page_url)
    bs_object = BeautifulSoup(page.content, "html.parser")
    return bs_object


def find_single_page_urls(bs_object) -> list:
    """ This function iterates over all a sections and gets all href lines
    returns:  list of strings with all message URLs
    """
    urls = []
    for a in bs_object.find_all('a', href=True):
        one_link = "https://ss.com" + a['href']
        re_match = re.search("msg", one_link)
        if re_match:
            urls.append(one_link)

    valid_urls = []
    for url in urls:
        if url not in valid_urls:
            valid_urls.append(url)
    return valid_urls


def get_msg_field_info(msg_url: str, span_id: str):
    """ This function finds span id in url and returns value """
    r  = requests.get(msg_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    span = soup.find("span", id=span_id)
    return span.text


def get_msg_table_info(msg_url: str, td_class: str) ->list:
    """ This function parses message page and extracts td_class table fields
    Returns: str list with table field data
    """
    page = requests.get(msg_url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find('table', id="page_main")

    table_fields = []

    table_data = table.findAll('td', {"class": td_class})
    for data in table_data:
        tostr = str(data)
        no_front = tostr.split('">', 1)[1]
        name = no_front.split("</",1)[0]
        table_fields.append(name)
    return table_fields


def write_line(text: str,file_name: str) ->None:
    """ Append text to end of the file"""
    with open(file_name, 'a', encoding="utf-8") as the_file:
        the_file.write(text)


scrape_website()
