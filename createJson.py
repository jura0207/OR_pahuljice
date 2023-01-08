import psycopg2

class Cereal():
    id_cereal: int
    cereal_name: str
    type: str
    number_of_calories: int
    price: float
    id_store: int
    id_manufacturer: int
    ingredients: list[int]

class Manufacturer():
    id_manufacturer: int
    manufacturer_name: str
    manufacture_country_iso: str

class Store():
    id_store: int
    store_name: str
    store_country_iso: str

class Ingredients():
    id_ingredients: int
    ingredient_name: str
    is_vegan: bool
    is_gluten_free: bool
    is_allergens_free: bool


def db():
    return psycopg2.connect(database="pahuljice", user='postgres', password='5478963210', host='127.0.0.1', port= '5432')

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


def getJsonCereal():
    jsonString = "{\n\"@context\": \"http://schema.org\",\n\"cereal\": [\n"

    my_queryCereal = query_db("select * from cereal")
    my_queryManufacturer = query_db("select * from manufacturer")
    my_queryStore = query_db("select * from store")
    my_queryIngredients = query_db("select * from ingredients")

    for i in my_queryCereal:
        jsonString = jsonString + "{\n"
        jsonString = jsonString + "\"cereal_name\": " + "\"" + i.get("cereal_name") + "\",\n"
        jsonString = jsonString + "\"type\": " + "\"" + i.get("type") + "\",\n"
        jsonString = jsonString + "\"price\": " + str(i.get("price")) + ",\n"

        store_id = i.get("id_store")
        for store in my_queryStore:
            if store.get("id_store") == store_id:
                jsonString = jsonString + "\"store\": {\n" + "\"store_name\": " + "\"" + store.get("store_name") + "\",\n"
                jsonString = jsonString + "\"country\": {\n"
                jsonString = jsonString + "\"@type\": \"Country\",\n"
                jsonString = jsonString + "\"addressCountry\": " + "\"" + store.get("store_country_iso") + "\"\n"
                jsonString = jsonString + "}\n"
                jsonString = jsonString + "},\n"

        manufacturer_id = i.get("id_manufacturer")
        for manufacturer in my_queryManufacturer:
            if manufacturer.get("id_manufacturer") == manufacturer_id:
                jsonString = jsonString + "\"manufacturer\": {\n" + "\"manufacturer_name\": " + "\"" + manufacturer.get("manufacturer_name") + "\",\n"
                jsonString = jsonString + "\"country\": {\n"
                jsonString = jsonString + "\"@type\": \"Country\",\n"
                jsonString = jsonString + "\"addressCountry\": " + "\"" + manufacturer.get("manufacture_country_iso") + "\"\n"
                jsonString = jsonString + "}\n"
                jsonString = jsonString + "},\n"

        jsonString = jsonString + "\"nutrition\": {\n"
        jsonString = jsonString + "\"@type\": \"NutritionInformation\",\n"
        jsonString = jsonString + "\"calories\": " + str(i.get("number_of_calories")) + "\n"
        jsonString = jsonString + "},\n"

        ingredients = i.get("ingredients")
        jsonString = jsonString + "\"ingredients\": ["
        for ingredient in my_queryIngredients:
            if ingredient.get("id_ingredients") in ingredients:
                jsonString = jsonString + "{\n"
                jsonString = jsonString + "\"ingredient_name\": " + "\"" + ingredient.get("ingredient_name") + "\",\n"
                jsonString = jsonString + "\"is_vegan\": " + str(ingredient.get("is_vegan")).lower() + ",\n"
                jsonString = jsonString + "\"is_gluten_free\": " + str(ingredient.get("is_gluten_free")).lower() + ",\n"
                jsonString = jsonString + "\"is_allergens_free\": " + str(ingredient.get("is_allergens_free")).lower() + "\n"
                jsonString = jsonString + "},\n"
        jsonString = jsonString[:-2] 
        jsonString = jsonString + "]},\n"
    jsonString = jsonString[:-2]
    jsonString = jsonString + "]\n}"

    with open("sample.json", "w") as outfile:
                outfile.write(str(jsonString))