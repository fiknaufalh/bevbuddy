# Starbucks Menu Web Scraping

## Perizinan Web Scraping

Data menu dan nutrisi diperoleh dengan melakukan _web scraping_ pada [Starbucks Menu](https://www.starbucks.com/menu) dengan tetap memperhatikan etika pengaksesan data secara publik. Pada prinsipnya, _web scraping_ dilakukan untuk tujuan pengetahuan dan analisis, dan dilakukan dengan penuh kehati-hatian untuk memastikan pengambilan data yang sah dan aman. Pengaksesan dilakukan sesuai dengan aturan yang ditetapkan oleh situs web target dan menjauhi praktik-praktik yang dapat mengganggu operasional normal situs tersebut.

## Tools Penggunaan

_Web scraping_ dilakukan dengan menggunakan [Selenium](https://www.selenium.dev/), sebuah alat pengujian otomatis untuk aplikasi web. Selenium memungkinkan pengendalian otomatis dari browser untuk menavigasi dan mengekstrak data dari halaman web. Penggunaan Selenium membutuhkan tanggung jawab dan kepatuhan terhadap kebijakan penggunaan situs web target.

## Sampel Data

### Menu

```json
{
    "id": 1062,
    "name": "Caramel Ribbon Crunch Crème Frappuccino® Blended Beverage",
    "description": "Buttery caramel syrup is blended with milk and ice, then topped with a layer of dark caramel sauce, whipped cream, caramel drizzle and a crunchy caramel-sugar topping—oh-so-beautifully delicious.",
    "category": "Frappuccino® Blended Beverages",
    "url_img": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20190528_CaramelRibbonCrunchFrappCreme.jpg?impolicy=1by1_wide_topcrop_630"
},
{
    "id": 2123674,
    "name": "Paradise Drink Starbucks Refreshers\u00ae Beverage",
    "description": "Tropical flavors of pineapple and passionfruit combine with diced pineapple and creamy coconutmilk to create a delicious island escape.",
    "category": "Cold Drinks",
    "url_img": "https://globalassets.starbucks.com/digitalassets/products/bev/SBX20211217_ParadiseDrink.jpg?impolicy=1by1_wide_topcrop_630"
}
```

### Nutrisi

```json
{
    "id_menu": 1062,
    "calories": 420.0,
    "protein": 5.0,
    "fats": 22.0,
    "carbs": 50.0,
    "sugar": 50.0
},
{
    "id_menu": 2123674,
    "calories": 140.0,
    "protein": 1.0,
    "fats": 2.5,
    "carbs": 27.0,
    "sugar": 27.0
}
```
