# %%
import json
from typing import List

# %%
genres_raw = json.load(open('genres_dict.json', encoding='utf-8'))
themes_raw = json.load(open('themes_dict.json', encoding='utf-8'))
modes_raw = json.load(open('game_modes.json', encoding='utf-8'))
keywords_raw = json.load(open('keywords_dict.json', encoding='utf-8'))
platforms_raw = json.load(open('platforms_dict.json', encoding='utf-8'))

# %%
genres = {k: v['name'] for k,v in genres_raw.items()}
themes = {k: v['name'] for k,v in themes_raw.items()}
modes = {k: v['name'] for k,v in modes_raw.items()}
keywords = {k: v['name'] for k,v in keywords_raw.items()}
platforms = {k: v['name'] for k,v in platforms_raw.items()}

# %%
covers_raw = json.load(open('covers_dict.json', encoding='utf-8'))
games_raw = json.load(open('good_games.json', encoding='utf-8'))

# %%
class Game:
    all_games = {}
    count = 0
    
    def __init__(self, name: str, features: List[str], description: str, cover: str, rating: float, platforms: List[str], url: str):
        if name not in Game.all_games:
            Game.count += 1
        
        self.name = name
        self.features = features
        self.description = description
        self.cover = cover
        self.rating = round(rating / 100 * 5)
        self.platforms = platforms
        self.url = url
        self.count = Game.count - 1
        
        Game.all_games[name] = self
        

    def __str__(self):
        return f"<Game ({self.count}): {self.name}>"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.rating < other.rating

    def print(self):
        print(self.name)
        print(self.description)
        print(self.features)
        print(self.rating)
        print(self.platforms)
        print(self.url)
        print(self.cover)

# %%
# build games db
for game in games_raw.values():
    name = game['name']
    features = []
    if 'genres' in game:
        for genre in game['genres']:
            features.append(genres[str(genre)])
    if 'themes' in game:
        for theme in game['themes']:
            features.append(themes[str(theme)])
    if 'game_modes' in game:
        for mode in game['game_modes']:
            features.append(modes[str(mode)])
    if 'keywords' in game:
        for keyword in game['keywords']:
            features.append(keywords[str(keyword)])
    description = game['summary'] if 'summary' in game else None
    image_id = covers_raw[str(game['cover'])]['image_id'] if 'cover' in game and str(game['cover']) in covers_raw else None
    cover = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.png" if image_id else None
    rating = game['rating']
    platforms_ = []
    if 'platforms' in game:
        for platform in game['platforms']:
            platforms_.append(platforms[str(platform)])
    url = game['url']
    Game(name, features, description, cover, rating, platforms_, url)


# %%
game_goals = {
  'play with friends': ['shooter', 'sports', 'party', 'MMO', 'co-operative', 'split screen', 'Battle Royale'],
  'building skills': ['puzzle', 'simulation', 'strategy', 'educational'],
  'storytelling': ['RPG', 'adventure', 'visual novel', 'drama'],
  'exploration': ['open-world', 'sandbox', 'adventure'],
  'competition': ['shooter', 'sports', 'fighting', 'racing'],
  'relaxation': ['casual', 'simulation', 'music'],
  'creativity': ['sandbox', 'construction', 'artistic'],
  'immersion': ['RPG', 'adventure', 'horror'],
  'problem-solving': ['puzzle', 'adventure', 'strategy', 'simulation'],
  'collection-building': ['RPG', 'card game', 'gacha'],
  'role-playing': ['RPG', 'simulation', 'strategy'],
  'community-building': ['MMO', 'simulation', 'city-building'],
  'skill-building': ['simulation', 'sports', 'puzzle', 'strategy'],
  'experimentation': ['sandbox', 'simulation', 'strategy', 'educational'],
  'strategy': ['RTS', 'tactics', 'simulation'],
  'mystery-solving': ['adventure', 'puzzle', 'visual novel', 'thriller'],
  'action': ['shooter', 'fighting', 'platform', 'hack and slash', 'beat em up'],
  'science-fiction': ['RPG', 'shooter', 'strategy'],
  'fantasy': ['RPG', 'strategy', 'visual novel'],
  'horror': ['survival', 'adventure', 'visual novel'],
  'historical': ['simulation', 'strategy'],
  'stealth': ['stealth'],
  'comedy': ['comedy'],
  'business': ['simulation'],
  'non-fiction': ['educational'],
  'kids': ['casual', 'educational'],
  'warfare': ['shooter', 'strategy'],
  '4X (explore, expand, exploit, and exterminate)': ['4X'],
  'romance': ['visual novel', 'erotic']
}


# %%
class Agent:
    count = 0
    all_agents = []

    def __init__(self, goals: List[str]):
        self.goals = goals
        self.id = Agent.count
        Agent.count += 1
        Agent.all_agents.append(self)

    def __str__(self):
        return f"<Agent ({Agent.count}): {self.goals}>"

    def __eq__(self, other):
        return self.goals == other.goals

    def add_goal(self, goal: str):
        self.goals.append(goal)

    def build_features(self):
        result = {}
        for goal in self.goals:
            for feature in game_goals[goal]:
                if feature not in result:
                    result[feature] = [goal]
                else:
                    result[feature].append(goal)
        return result

# %%
class Recommendation:
    def __init__(self, game: Game, score: float, reasons: List[str]):
        self.game = game
        self.score = score
        self.reasons = reasons

    def __lt__(self, other):
        if self.score != other.score:
            return self.score < other.score
        return self.game.rating < other.game.rating


# %%
def get_recommendations(agent: Agent):
    my_features = agent.build_features()
    recommendations = []
    for game in Game.all_games.values():
        game_score = 0
        reasons = []
        # for my_f in my_features:
        for my_f,my_gs in my_features.items():
            if my_f in game.features:
                game_score += len(my_gs)
                reasons.extend(my_gs)
        if game_score > 0:
            recommendations.append(Recommendation(game, game_score, list(set(reasons))))
    recommendations.sort(reverse=True)
    return recommendations
