
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, Response
from createJson import getJsonCereal
import psycopg2
import json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/profil")
def profil():
    if (session.get("user") != None):
        return render_template(
            "profil.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
    else:
        return redirect("/")

@app.route("/preslike")
def preslike():
    if (session.get("user") != None):
        return render_template(
            "preslike.html",
        )
    else:
        return redirect("/")

@app.route("/csvdownload")
def csvdownload():
    if (session.get("user") != None):
        conn = psycopg2.connect(database="pahuljice", user='postgres', password='5478963210', host='127.0.0.1', port= '5432')
        cur = conn.cursor()
        sql = "COPY (SELECT cereal_name, type, number_of_calories, price, store_name, store_country_iso, manufacturer_name, manufacture_country_iso, ingredient_name, is_vegan, is_gluten_free, is_allergens_free FROM public.cereal JOIN public.store using (id_store) join public.manufacturer using (id_manufacturer) NATURAL JOIN public.cerealingredients NATURAL JOIN public.ingredients ORDER BY id_cereal ASC) TO STDOUT WITH CSV DELIMITER ';'"
        with open("D:/Nastava/FER 3/OR/Pahuljice/OR_pahuljice/__pycache__/mnt/table.csv", "w") as file:
            cur.copy_expert(sql, file)
        return Response(
            open("D:/Nastava/FER 3/OR/Pahuljice/OR_pahuljice/__pycache__/mnt/table.csv", "r"),
            mimetype="text/csv",
            headers={"Content-disposition":
                    "attachment; filename=myplot.csv"})
    else:
        return redirect("/")

@app.route("/jsondownload")
def jsondownload():
    if (session.get("user") != None):
        getJsonCereal()
        return Response(
            open("D:/Nastava/FER 3/OR/Pahuljice/OR_pahuljice/sample.json", "r"),
            mimetype="text/json",
            headers={"Content-disposition":
                    "attachment; filename=myplot.json"})
    else:
        return redirect("/")

def db():
    return psycopg2.connect(database="pahuljice", user='postgres', password='5478963210', host='127.0.0.1', port= '5432')

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
