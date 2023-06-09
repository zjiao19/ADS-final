#!/usr/bin/env python
from flask import Flask, render_template_string, request, make_response, redirect, url_for
from flask import render_template
import json
import goal_based
from goal_based import Game
from cb_filter import get_recommendations2
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
        agent = goal_based.Agent(goals,fav_games[0])
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
    # select top 50 recomendation in the array
    if len(recommendations) > 100:
        recommendations = recommendations[:100]
    # initiliaze a dictionary, key is the name of the game, value is recommendation object
    first_rec = {r.game.name: r for r in recommendations}
    first_rec_arr = [[r.game.name, r.game.description] for r in recommendations]
    fav_game_obj = Game.all_games[agent.fav_game]
    print(type(fav_game_obj))
    first_rec_arr.append([agent.fav_game,fav_game_obj.description])
    name_list = get_recommendations2(first_rec_arr,agent.fav_game)
    # find all values corresponding to the name in the first_rec dictionary, they key is from name_list
    recommendations = [first_rec[name] for name in name_list]
    print(type(recommendations[0]))
    data = []
    for r in recommendations:
        if arg_genre and arg_genre not in r.game.features:
            continue
        if arg_platform and arg_platform not in r.game.platforms:
            continue
        if arg_rating and arg_rating > r.game.rating:
            continue
        
        reasons = r.reason_match_features()
        reasonstr = ""
        for reason, features in reasons.items():
            reasonstr += f"You like {reason} and this game is about {', '.join(features)}. "
        resonstr2 = f"It is also similar to the game you like, {agent.fav_game}"
        reasonstr += resonstr2
        data.append({
            "title": r.game.name,
            "img": r.game.cover,
            "description": r.game.description,
            "reason": reasonstr,
            "rating": r.game.rating,
            "url": r.game.url,
        })

        if len(data) >= 50:
            break
    html = render_template('result.html', data=data, genres=sorted(goal_based.genres.values()), platforms=sorted(goal_based.platforms.values()), args=[arg_genre, arg_platform, arg_rating])
    response = make_response(html)
    return response
