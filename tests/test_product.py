from pytest import raises
from shopitappd.product import Rating, Product


def test_rating_generation():
    with raises(ValueError):
        Rating(rating=-1, rating_count=1)

    with raises(ValueError):
        Rating(rating=5.01, rating_count=1)

    with raises(ValueError):
        Rating(rating=1, rating_count=-1)


# We need to add more tests here, but I first want to get the GH actions to work
