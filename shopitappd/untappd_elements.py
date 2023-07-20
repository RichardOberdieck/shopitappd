import requests
from shopitappd.product import Rating
from shopitappd.constants import UNTAPPD_MENU_ID
import os
from bs4 import BeautifulSoup


def get_href(result):
    return result.find("a").get("href")


def extract_uid_from_href(href):
    return int(href.split("/")[-1])


def get_beer_specific_tag(href):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    response = requests.get(f"https://untappd.com{href}", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find("div", class_="details")


def get_rating_info_from_tag(beer_tag):
    rating = float(beer_tag.find("div", class_="caps").get("data-rating"))
    rating_text = beer_tag.find("p", class_="raters").text
    rating_text_list = rating_text.split()
    rating_count = int(rating_text_list[0].replace(",", ""))
    return rating, rating_count


def get_beer_ratings_from_untappd():
    untappd_ratings = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    response = requests.get("https://untappd.com/v/hos-rune-bottleshop/11402369", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all("li", class_="menu-item", id="beer")
    for result in results:
        href = get_href(result)
        uid = extract_uid_from_href(href)

        beer_tag = get_beer_specific_tag(href)
        rating, rating_count = get_rating_info_from_tag(beer_tag)

        # Skip if no rating yet
        if rating < 1 or rating_count < 1:
            continue

        untappd_ratings[uid] = Rating(rating=rating, rating_count=rating_count)

    return untappd_ratings
