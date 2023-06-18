from shopify_elements import get_products
from untappd_elements import get_beer_ratings_from_untappd
from time import sleep
from tqdm import tqdm


def main():
    ratings = get_beer_ratings_from_untappd()
    products = get_products(ratings)

    for product in tqdm(products):
        product.update_rating()

        sleep(1)  # For rate-limit purposes
        product.update_tags()


if __name__ == "__main__":
    main()
