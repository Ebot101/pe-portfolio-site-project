import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import folium
from peewee import * 
import datetime
from playhouse.shortcuts import model_to_dict 
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)


if os.getenv('TESTING') == 'true':
    print('Running in testing mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',
                          uri=True)
    
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                host=os.getenv("MYSQL_HOST"),
                port= 3306

)

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])

hobbyImageDir = os.path.join('img')
img = os.path.join('static', 'img')

# Landing page data
landing_data = [

    {
        "name": "Eyob Dagnachew",
        "img": "./static/img/eyob.jpeg",
        "marker_color": "red",
        "style": "pin2",
        "places": [
            {
                "coord": [43.7615, -79.4111],
                "name": "Canada"
            },
            {
                "coord": [9.1450, 40.4897],
                "name": "Ethiopia"
            },
            {
                "coord": [52.3555, -1.1743],
                "name": "England"
            }
        ],
    }
]

def build_map():
    my_map = folium.Map()

    # Add markers for each person
    for person in landing_data:
        for p in person["places"]:
            folium.Marker(p["coord"], popup = p["name"], icon=folium.Icon(color=person["marker_color"], icon="circle", prefix="fa")).add_to(my_map)

    my_map = my_map._repr_html_()
    return my_map

pic_data = {

"Eyob Dagnachew": "./static/img/eyob.jpeg"     

}


about_me= {

    "Eyob Dagnachew": """Why Hello there! My name is Eyob, I'm an incoming junior at 
    Carnegie Mellon University in Pittsburgh! I love trying to find new ways to apply creativity
    to make something new in the world! One of those ways is through coding which is something I've
    been doing for the past couple years through internships, research, and hackathons! other than tech
    I'm usually trying to find some more artistic outlets for my creativity, resulting in me
    having a camera bag, sketchbook and laptop in my backpack almost constantly!  """
}

@app.route('/')
def index():
    my_map = build_map()
    intro_message = "Welcome to my page!"
    map_title = "A map of all the places that I have been to:"
    map_desc = "Eyob (Red)"
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), landing_data=landing_data, intro_message=intro_message, my_map=my_map, map_title=map_title, map_desc=map_desc)

@app.route('/<fellow>')
def fellowPage(fellow):
    full_name = fellow.split()
    image_link = full_name[0]
    
    fellow=request.args.get('fellow', fellow)
    print()
    return render_template('aboutMePage.html', fellow=fellow, name= image_link, data= pic_data, intro= about_me)

@app.route('/<fellow>/experience')
def experiencePage(fellow):
    experience=[{"Company" : "Fluence", "Role": "Data Science Modeling Intern", "JobDescription": ['Re-organized test scripts into implementation tests and behavior tests, and increased coverage of both categories of tests.',
    'Implemented data pipeline for site-specific temperature and dispatch data from two sites.', 'Evaluated existing model performance against site data, and determined if there is site-specific bias in the existing model.', 'Implemented a Long-Short Term Model to improve prediction accuracy for individual sites'], "Date": 'June 2022 - Aug 2022'}]
    data="Eyob Dagnachew"

    return render_template('experiencePage.html', data=data, experience=experience)

@app.route('/<fellow>/hobbies')
def hobbiesPage(fellow):
    hobbyImage1=os.path.join(hobbyImageDir, 'elden_ring.png')
    hobbyImage2=os.path.join(hobbyImageDir, 'pic7.png')
    hikingImage=os.path.join(hobbyImageDir, "hiking.webp")
    bookImage=os.path.join(hobbyImageDir, "books.webp")
    travelImage=os.path.join(hobbyImageDir, "travel.jpg")
    eyobPhotography=os.path.join(hobbyImageDir, "eyobPhotography.webp")
    digitalArt=os.path.join(hobbyImageDir, "digitalArt.webp")
    lightWriting=os.path.join(hobbyImageDir, "lightWriting.avif")


    hobbies=[{"Hobby_Blurb" : "I always enjoy putting something from my imagination and challenging myself into making it as real as possible with the basic theories of art.", "Hobby_Image": digitalArt},
                {"Hobby_Blurb": "I love photography because it challenges me to taking something that already exists that I already like and engage with it in a new way by trying to represent it in a new was through the lens.", "Hobby_Image": eyobPhotography}, {"Hobby_Blurb": "I like writing because it fills the gap of things that i cant bring to life in writing by brining them to life with my words instead, allowing me to delved even further to my imagination.", "Hobby_Image": lightWriting}]
    data="Eyob Dagnachew"

    return render_template('hobbiesPage.html', data=data, hobbies=hobbies)


@app.route('/<fellow>/education')
def education(fellow):

    experience=[{"Company" : "Carnegie Mellon", "Role": "B.S in  Statistics/Machine Learning","JobDescription": ["Relevent Coursework: Data Structures and Algorithms, Fundamentals of Software Engineering , Methods for Statistics and Data Science, Probability and Statistical Inference, Concepts of Mathematics"],

    "Date": 'June 2021 - May 2025'},
            {"Company" : "Annandale High School", "Role": "IB Diploma ","Date" : " August 2017 - May 2021"}]
    data="Eyob Dagnachew"


    return render_template('education.html', data = data, experience = experience)


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    form_data = request.form.to_dict()


    if 'name' not in form_data or form_data['name'] =="":
        return jsonify({'error': 'Invalid name'}), 400


    if ('email' not in form_data) or "@" not in form_data['email'] or ".com" not in form_data['email'] or form_data['email'] =="":
        return jsonify({'error': 'Invalid email'}), 400
    
    
    if 'content' not in form_data or form_data['content'] =="":
        return jsonify({'error': 'Invalid content'}), 400


    timeline_post = TimelinePost.create(name = form_data['name'], email = form_data['email'], content = form_data['content'])
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts' :[
            model_to_dict(p)
            for p in 
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/timeline")
def timeline():
    return render_template('timeline.html', Title = 'Timeline')
