from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
import json

app = FastAPI()

class myResponse():
    status: str
    message: str
    response: str

class Cereal(BaseModel):
    id_cereal: int
    cereal_name: str
    type: str
    number_of_calories: int
    price: float
    id_store: int
    id_manufacturer: int
    ingredients: list[int]

@app.get("/all")
def get_all(response: Response):
    #my_query = query_db("select * from allcereals")
    my_query = query_db("select * from cereal")
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data fetched successfully"
    the_response.response = my_query
    return {the_response}

@app.get("/one")
async def get_one(response: Response, id: int | None = None):
    if id == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        the_response = myResponse()
        the_response.status = "Bad requset"
        the_response.message = "No ID input given"
        the_response.response = None
        return the_response
    my_query = query_db("select * from cereal where id_cereal= %s limit %s", (id, 1), one=True)
    if my_query == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        the_response = myResponse()
        the_response.status = "Not found"
        the_response.message = "No cereal with requested ID"
        the_response.response = None
        return the_response
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data fetched successfully"
    the_response.response = my_query
    return {the_response}

@app.get("/calories")
def n1(response: Response):
    my_query = query_db("select cereal_name, number_of_calories from cereal ORDER BY number_of_calories ASC")
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data fetched successfully"
    the_response.response = my_query
    return {the_response}

@app.get("/price")
def n2(response: Response):
    my_query = query_db("select cereal_name, price from cereal ORDER BY price ASC")
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data fetched successfully"
    the_response.response = my_query
    return {the_response}

@app.get("/country")
def n3(response: Response, country: str | None = None):
    if country == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        the_response = myResponse()
        the_response.status = "Bad requset"
        the_response.message = "No country input given"
        the_response.response = None
        return the_response
    my_query = query_db("select * from cereal NATURAL JOIN store WHERE store_country_iso = %s ORDER BY id_cereal ASC", [country])
    print(my_query)
    if my_query == False:
        response.status_code = status.HTTP_404_NOT_FOUND
        the_response = myResponse()
        the_response.status = "Bad request"
        the_response.message = "Bad request"
        the_response.response = None
        return the_response
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data fetched successfully"
    the_response.response = my_query
    return {the_response}

@app.get("/specification")
def get_specification(response: Response):
    f = open('openapi.json')
    data = json.load(f)
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data fetched successfully"
    the_response.response = data
    return {the_response}

@app.post("/postone")
async def post_one(cereal: Cereal, response: Response):
    invalid_names = check_column_names(cereal)
    if invalid_names != []:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        the_response = myResponse()
        the_response.status = "Not acceptable"
        the_response.message = "Missing valid attribute names"
        the_response.response = None
        return the_response
    my_query = insert_db("INSERT INTO cereal (id_cereal, cereal_name, type, number_of_calories, price, id_store, id_manufacturer, ingredients) values (%s,%s,%s,%s,%s,%s,%s,%s)", (cereal.id_cereal, cereal.cereal_name, cereal.type, cereal.number_of_calories, cereal.price, cereal.id_store, cereal.id_manufacturer, cereal.ingredients))
    if my_query == True:
        response.status_code = status.HTTP_201_CREATED
        the_response = myResponse()
        the_response.status = "Created"
        the_response.message = "Insert successfull"
        the_response.response = cereal
        return the_response
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        the_response = myResponse()
        the_response.status = "Forbidden"
        the_response.message = "Cereal with this ID already exist"
        the_response.response = None
        return the_response

@app.put("/putone")
def update_one(response: Response, cereal: Cereal, id: int | None = None):
    if id == None:
        id = cereal.id_cereal
    invalid_names = check_column_names(cereal)
    if invalid_names != []:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        the_response = myResponse()
        the_response.status = "Not acceptable"
        the_response.message = "Missing valid attribute names"
        the_response.response = None
        return the_response
    my_query = query_db("select * from cereal where id_cereal= %s limit %s", (id, 1), one=True)
    if my_query == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        the_response = myResponse()
        the_response.status = "Not found"
        the_response.message = "No cereal with given ID"
        the_response.response = None
        return the_response
    my_query = insert_db("UPDATE cereal SET cereal_name = %s, type = %s, number_of_calories = %s, price = %s, id_store = %s, id_manufacturer = %s, ingredients = %s WHERE id_cereal = %s", (cereal.cereal_name, cereal.type, cereal.number_of_calories, cereal.price, cereal.id_store, cereal.id_manufacturer, cereal.ingredients, id))
    response.status_code = status.HTTP_201_CREATED
    the_response = myResponse()
    the_response.status = "Created"
    the_response.message = "Update successfull"
    the_response.response = cereal
    return the_response


@app.delete("/deleteone")
def delete_one(response: Response, id: int | None = None):
    if id == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        the_response = myResponse()
        the_response.status = "Bad requset"
        the_response.message = "No ID input given"
        the_response.response = None
        return the_response
    my_query = query_db("select * from cereal where id_cereal= %s limit %s", (id, 1), one=True)
    if my_query == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        the_response = myResponse()
        the_response.status = "Not found"
        the_response.message = "No cereal with given ID"
        the_response.response = None
        return the_response
    my_query = insert_db("DELETE FROM cereal WHERE id_cereal = %s", [id])
    response.status_code = status.HTTP_200_OK
    the_response = myResponse()
    the_response.status = "Status OK"
    the_response.message = "Data deleted successfully"
    the_response.response = None
    return {the_response}

def db():
    return psycopg2.connect(database="pahuljice", user='postgres', password='5478963210', host='127.0.0.1', port= '5432')

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

def insert_db(query, args):
    succes = True
    try:
        connection = db()
        cur = connection.cursor()
        cur.execute(query, args)
        connection.commit()
        count = cur.rowcount
    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)
        succes = False
    finally:
        if connection:
            cur.close()
            connection.close()
    return succes

def check_column_names(payload):
    invalid_names = []
    for i in payload:
        if i[0] not in ["id_cereal", "cereal_name", "type", "number_of_calories", "price", "id_store", "id_manufacturer", "ingredients"]:
            invalid_names.append(i)
    return invalid_names