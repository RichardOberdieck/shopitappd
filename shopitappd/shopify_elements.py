import requests
from shopitappd.product import Product, Rating
from shopitappd.shopify_header import get_header_for_shopify
from typing import List, Dict


def get_all_products_url(id: int) -> str:
    return f"https://hos-rune.myshopify.com/admin/api/2023-01/products.json?since_id={id}"


def get_products(beer_ratings: Dict[int, Rating]) -> List[Product]:
    products = get_products_from_shopify()

    result = []
    for product in products:
        uid = extract_uid_from_tags(product["tags"])

        if uid not in beer_ratings:
            title = product["title"]
            print(f"{uid} called {title} is not found")
            continue

        result.append(Product(id=product["id"], title=product["title"], tags=product["tags"], rating=beer_ratings[uid]))

    return result


def get_products_from_shopify() -> dict:
    products = []
    products_remaining = True
    last_id = 0
    while products_remaining:
        response = requests.get(get_all_products_url(last_id), headers=get_header_for_shopify())
        current_products = response.json()["products"]
        if len(current_products) == 0:
            products_remaining = False
        else:
            products += current_products
            last_id = current_products[-1]["id"]
    # Finally, we filter out all the products that do not have a uid
    products = [p for p in products if "uid_" in p["tags"] and p["status"] == "active"]
    return products


def extract_uid_from_tags(tags: str) -> int:
    txt = tags
    list_of_tags = txt.split(", ")
    return [int(t[4:]) for t in list_of_tags if t.startswith("uid_")][0]
