#!/usr/bin/env python
from flask import Flask, render_template_string, request, make_response, redirect, url_for
from flask import render_template
import json
import goal_based

app = Flask(__name__, template_folder='.')

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
        'index.html', game_goals=goal_based.game_goals.keys(), popular_games=popular_games)
    response = make_response(html)
    return response


@app.route('/create-user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        d = json.loads(request.data.decode())
        fav_games = d["games"]
        goals = d["goals"]
        # print("fav_games", fav_games)
        # print("goals", goals)
        agent = goal_based.Agent(goals)
        return make_response(str(agent.id))


@app.route('/result/<user_id>', methods=['GET'])
def result(user_id):
    if user_id == "None":
        # img not found
        return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404
    if int(user_id) >= len(goal_based.Agent.all_agents):
        # user not found
        return redirect(url_for('index'))
    
    arg_genre = request.args.get('genres')
    arg_platform = request.args.get('platforms')
    arg_rating = request.args.get('rating')
    if arg_genre == "All":
        arg_genre = None
    if arg_platform == "All":
        arg_platform = None
    if arg_rating is not None:
        arg_rating = int(arg_rating)

    agent = goal_based.Agent.all_agents[int(user_id)]
    recommendations = goal_based.get_recommendations(agent)
    data = []
    for r in recommendations:
        if arg_genre and arg_genre not in r.game.features:
            continue
        if arg_platform and arg_platform not in r.game.platforms:
            continue
        if arg_rating and arg_rating > r.game.rating:
            continue

        data.append({
            "title": r.game.name,
            "img": r.game.cover,
            "description": r.game.description,
            "reason": ", ".join(r.reasons),
            "rating": r.game.rating,
            "url": r.game.url,
        })

        if len(data) >= 50:
            break
    html = render_template('result.html', data=data, genres=sorted(goal_based.genres.values()), platforms=sorted(goal_based.platforms.values()), args=[arg_genre, arg_platform, arg_rating])
    response = make_response(html)
    return response
