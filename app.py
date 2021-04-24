from BBWebFw import webApp
from BBWebFw.FileRenderer import Template
import os
import random
import firebase_admin
from firebase_admin import db, storage

cred_obj = firebase_admin.credentials.Certificate('pwastore-c1ed2-firebase-adminsdk-s9p9l-77ba9c52d5.json')
fb = firebase_admin.initialize_app(cred_obj,{"databaseURL": "https://pwastore-c1ed2-default-rtdb.firebaseio.com/",})
rootRef = db.reference("/")



#App Defination
app = webApp("app", "gunicorn", os.path.dirname(os.path.abspath(__file__)))
app.staticCache = 60 * 60 * 24 * 365

#Jinja Templater
template = Template()

@app.catchURL('/')
@app.catchURL('/home')
def index(request,response):
    apps = rootRef.child("apps").get()
    response.text = template("index.html", {"key": random.random()*100000, "apps": apps})

@app.catchURL('/sitemap')
def sitemap(request,response):
    response.text = open('sitemap.xml', "rb").read().decode()
    response.content_type = "text/xml"

@app.catchURL('/github')
def github(request,response):
    response.body = b'<script>window.location.replace("https://github.com/Black-Blaze/");</script>'
    
@app.catchURL('/merch/dlsl')
def merchDLSL(request,response):
    response.body = b'<script>window.location.replace("https://teeshopper.in/products/Rookie-tee-dev")</script>'