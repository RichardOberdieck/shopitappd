from pydantic import BaseModel, validator
import requests
from typing import List, Dict
from time import sleep
from json import dumps
from shopify_header import get_header_for_shopify


class Rating(BaseModel):
    rating: float
    rating_count: int

    class Config:
        allow_mutation = False

    @validator("rating")
    def rating_is_bounded(cls, v):
        if v < 1 or v > 5:
            raise ValueError(f"Rating value {v} is below 1 or above 5")
        return v

    @validator("rating_count")
    def rating_count_positive(cls, v):
        if v < 1:
            raise ValueError(f"Rating count {v} should be positive")
        return v


class Product(BaseModel):
    id: str
    title: str
    tags: str
    rating: Rating

    @validator("tags")
    def tags_length_positive(cls, v):
        if len(v) == 0:
            raise ValueError("Tags cannot be empty")
        return v

    def update_rating(self) -> None:
        rating_dict = self.define_rating_dict()
        self.send_post_request(rating_dict)

        rating_count_dict = self.define_rating_count_dict()
        self.send_post_request(rating_count_dict)
        sleep(1)  # To respect rate limit

    def update_tags(self) -> None:
        list_of_tags = self.tags.split(", ")
        tags_without_rating_classification = ", ".join([t for t in list_of_tags if t != "4+"])

        if self.rating.rating >= 4:
            updated_tags = tags_without_rating_classification + ", 4+"
        else:
            updated_tags = tags_without_rating_classification

        data = {"product": {"id": self.id, "tags": updated_tags}}

        sleep(1)  # To respect rate limit

        requests.put(self.get_product_url(), headers=get_header_for_shopify(), json=data)

    def get_metafields_url(self):
        return f"https://hos-rune.myshopify.com/admin/api/2023-01/products/{self.id}/metafields.json"

    def get_product_url(self):
        return f"https://hos-rune.myshopify.com/admin/api/2023-01/products/{self.id}.json"

    def define_rating_dict(self):
        return {
            "metafield": {
                "namespace": "reviews",
                "key": "rating",
                "value": dumps({"value": self.rating.rating, "scale_min": 1.0, "scale_max": 5.0}),
                "type": "rating",
            }
        }

    def define_rating_count_dict(self):
        return {
            "metafield": {
                "namespace": "reviews",
                "key": "rating_count",
                "value": f"{self.rating.rating_count}",
                "type": "number_integer",
            }
        }

    def send_post_request(self, data: Dict[str, dict]) -> None:
        response = requests.post(self.get_metafields_url(), headers=get_header_for_shopify(), json=data)
        if response.status_code != 201:
            raise ValueError(f"Status code {response.status_code} not 201")
