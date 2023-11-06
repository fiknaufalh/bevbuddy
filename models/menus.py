from pydantic import BaseModel
from typing import Literal

class Menu(BaseModel):
    id: int
    name: str
    desc: str
    category: Literal["Oleato™", "Hot Coffees", "Hot Drinks", "Hot Teas", "Iced Teas",
                      "Frappuccino® Blended Beverages", "Cold Coffees", "Cold Drinks"]
    url_img: str

    class Config:
        schema_extra = {
            "example": {
                "id": 2123736,
                "name": "Cinnamon Caramel Cream Cold Brew",
                "desc": "Starbucks® Cold Brew is sweetened with Cinnamon Caramel Syrup and topped with a cinnamon caramel cold foam and a dusting of cinnamon dolce topping for a special treat.",
                "category": "Cold Coffees",
                "url_img": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20221014_CinnamonCaramelCreamColdBrew.jpg?impolicy=1by1_wide_topcrop_630"
            }
        }