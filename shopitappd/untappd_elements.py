import requests
from product import Rating
import os


def get_beer_ratings_from_untappd():
    url = "https://business.untappd.com/api/v1/menus/134834"
    headers = {"Authorization": os.environ["UNTAPPD_ACCESS_TOKEN"]}

    response = requests.get(url, headers=headers, params={"full": "true"})

    sections = response.json()["menu"]["sections"]

    return {
        int(item["untappd_id"]): Rating(rating=float(item["rating"]), rating_count=int(item["rating_count"]))
        for s in sections
        for item in s["items"]
        if int(item["rating_count"]) > 0 and float(item["rating"]) > 0
    }
