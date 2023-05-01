#!/usr/bin/env python
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
import json

app = Flask(__name__, template_folder='.')

game_goals = {
    'play with friends': ['MMO', 'FPS', 'sports'],
    'building skills': ['puzzle', 'simulation', 'strategy'],
    'storytelling': ['RPG', 'adventure', 'visual novel'],
    'exploration': ['sandbox', 'open-world', 'platformer'],
    'competition': ['fighting', 'racing', 'sports'],
    'relaxation': ['casual', 'simulation', 'music'],
    'creativity': ['sandbox', 'construction', 'artistic'],
    'immersion': ['RPG', 'adventure', 'horror'],
    'problem-solving': ['puzzle', 'adventure', 'strategy'],
    'collection-building': ['RPG', 'card game', 'gacha'],
    'role-playing': ['RPG', 'simulation', 'strategy'],
    'community-building': ['MMO', 'simulation', 'city-building'],
    'skill-building': ['simulation', 'sports', 'puzzle'],
    'experimentation': ['sandbox', 'simulation', 'strategy'],
    'strategy': ['RTS', 'tactics', 'simulation'],
    'mystery-solving': ['adventure', 'puzzle', 'visual novel'],
    'action': ['FPS', 'fighting', 'platformer'],
    'science-fiction': ['RPG', 'FPS', 'strategy'],
    'fantasy': ['RPG', 'strategy', 'visual novel'],
    'horror': ['survival', 'adventure', 'visual novel']
}
popular_games = [
    'Grand Theft Auto V',
    'Minecraft',
    'Fortnite',
    'League of Legends',
    'Among Us',
    'Apex Legends',
    'Valorant',
    'World of Warcraft',
    'Cyberpunk 2077',
    'Animal Crossing: New Horizons',
    'The Legend of Zelda: Breath of the Wild',
    'Red Dead Redemption 2',
    'Call of Duty: Warzone',
    'Rocket League',
    'Counter-Strike: Global Offensive',
    'FIFA 21',
    'NBA 2K21',
    'Assassin\'s Creed Valhalla',
    'Hades',
    'Death Stranding'
]


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template(
        'index.html', game_goals=game_goals.keys(), popular_games=popular_games)
    response = make_response(html)
    return response


@app.route('/create-user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        d = json.loads(request.data.decode())
        fav_games = d["games"]
        goals = d["goals"]
        print("fav_games", fav_games)
        print("goals", goals)
    return make_response("0")


@app.route('/result/<user_id>', methods=['GET'])
def result(user_id):

    data = [
        {
            "title": "Apple",
            "img": "https://www.apple.com/ac/structured-data/images/knowledge_graph_logo.png?201606271147",
            "description": "Apple is awesome",
            "reason": "You use iPhone",
            "rating": 4,
        },
        {
            "title": "Banana",
            "img": "https://media.istockphoto.com/id/1400057530/photo/bananas-isolated.jpg?b=1&s=170667a&w=0&k=20&c=uiSdjIQkTr7S4gEdW_oB_5zfFYhpfe0LP-CryQl49w4=",
            "description": "Banana is bwesome",
            "reason": "You are Asian",
            "rating": 3,
        },
    ]
    html = render_template('result.html', length=len(data), data=data)
    response = make_response(html)
    return response
