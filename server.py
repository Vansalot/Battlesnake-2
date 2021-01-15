import os, random
import classes

import cherrypy
"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

dummyData = {'game': {'id': '1910a35c-923e-41cd-84b5-45fc6a296246', 'ruleset': {'name': 'solo', 'version': 'v1.0.15'}, 'timeout': 500}, 'turn': 0, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_C7pp6MPKJp7DRmTwMth7Wf7T', 'name': 'Python_replit_starter_snake_test', 'latency': '', 'health': 100, 'body': [{'x': 9, 'y': 9}, {'x': 9, 'y': 9}, {'x': 9, 'y': 9}], 'head': {'x': 9, 'y': 9}, 'length': 3, 'shout': ''}], 'food': [{'x': 8, 'y': 10}, {'x': 5, 'y': 5}], 'hazards': []}, 'you': {'id': 'gs_C7pp6MPKJp7DRmTwMth7Wf7T', 'name': 'Python_replit_starter_snake_test', 'latency': '', 'health': 100, 'body': [{'x': 9, 'y': 9}, {'x': 9, 'y': 9}, {'x': 9, 'y': 9}], 'head': {'x': 9, 'y': 9}, 'length': 3, 'shout': ''}}

GAMEBOARD = None
COSTMATRIX = {
    # costmatrix is representing the 'cost' for moving onto a tile. 
    # If the tile is occupied or on one of the edges, 
    # the cost for moving there is high, to indicate that we do not want to move there. 
    "ownsnakehead": 0,
	"empty": 1,
	"food": 5,
	"edge": 200,
	"corner": 300,
	"snakeheadclose": 799,
	"snakehead": 9999,
	"snakebody": 9999,
    "snaketail": 699,
    }

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "vansalot",  # TODO: Your Battlesnake Username
            "color": "#f780a1",
            "head": "evil",
            "tail": "hook",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        global GAMEBOARD
        GAMEBOARD = classes.Gameboard(COSTMATRIX, data)
        print("hello")

        print(data)
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        print(data)
        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port":
        int(os.environ.get("PORT", "8080")),
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
