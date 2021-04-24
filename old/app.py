from BBWebFw import webApp
from BBWebFw.FileRenderer import Template
import os

config = {
  "apiKey": "AIzaSyDBd6hR8JH3Gfi5i_bgkcHao0gtid1UQyY",
  "authDomain": "sushantshahml.firebaseapp.com",
  "databaseURL": "https://sushantshahml-default-rtdb.firebaseio.com/",
  "storageBucket": "sushantshahml.appspot.com"
}

#firebase = pyrebase.initialize_app(config)
#db = firebase.database()

#App Defination
app = webApp("app", "GUNICORN", os.path.dirname(os.path.abspath(__file__)))
app.staticCache = 60 * 60 * 24 * 365

#Jinja Templater
template = Template()

#Static Files
#currDir = os.path.dirname(os.path.abspath(__file__))
#app.setStaticDir("static/")
#print(app.staticDir)

#Error Handeling
#app.setError(404, "I Have Never Made That Thing")


@app.catchURL('/')
def index(response):
    response.text = template("index.html")

@app.catchURL('/home')
def home(response):
    response.text = template("templates/index.html")

@app.catchURL('/hi/{halo}')
class hi:
    def get(self, response, halo):
            response.text = "hello" + " " + halo

@app.catchURL('/sitemap')
def sitemap(response):
    response.text = open('sitemap.xml', "rb").read().decode()
    response.content_type = "text/xml"
        

@app.catchURL('/project')
@app.catchURL('/Project')
@app.catchURL('/projects')
@app.catchURL('/Projects')
def projects(response,):
    #projectsL = db.child("projects").get().val()
    print("""""""""""""""""""""""""""""""""""""""""""")
    proj=[
            {
                'href'        : "/hi1",
                'img'         : "../images/image1.png",
                'title'       : "Title1",
                'description' : "This Is description1"
            },
            {
                'href'        : "/hi2",
                'img'         : "../images/image2.png",
                'title'       : "Title2",
                'description' : "This Is description2"
            },
            {
                'href'        : "/hi3",
                'img'         : "../images/image3.png",
                'title'       : "Title3",
                'description' : "This Is description3"
            }
        ]

    for project in proj:
        print(project["href"])
        print(project["img"])
        print(project["title"])
        print(project["description"])
    response.text = template("projects.html", data={"projects": proj})
    #response.text = projectsL

@app.catchURL('/project/{name}')
@app.catchURL('/Project/{name}')
@app.catchURL('/projects/{name}')
@app.catchURL('/Projects/{name}')
def project(response,name):
    #projectsL = db.child("projects").get().val()
    response.text = template("projects.html")
    #response.text = projectsL

@app.catchURL('/material-components-web@latest/dist/material-components-web.min.css')
def material(response):
    app.return_external(response, "https://unpkg.com", "/material-components-web@latest/dist/material-components-web.min.css")

@app.catchURL('/material-components-web@latest/dist/material-components-web.min.css.map')
def material_map(response):
    app.return_external(response, "https://unpkg.com", "/material-components-web@latest/dist/material-components-web.min.css.map")

@app.catchURL('/social')
def social(response):
    response.text = "<center>This Link leads To</br><h1>NOWHERE</h1></center>"

@app.catchURL('/github')
def github(response):
    response.body = b'<script>window.location.replace("https://github.com/Black-Blaze/");</script>'
    
@app.catchURL('/merch/dlsl')
def merchDLSL(response):
    response.body = b'<script>window.location.replace("https://teeshopper.in/products/Rookie-tee-dev")</script>'