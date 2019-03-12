"""
Circuit Wars game server.

@author Krisztian Balog
"""

from flask import Flask, redirect, url_for
import json
from board import Board
from game import Game

app = Flask(__name__)
app.debug = True
app.config["GAME"] = Game()


@app.route("/status")
def status():
    """Returns the status of the game."""
    return json.dumps(app.config["GAME"].get_status())


@app.route("/reg/<team_id>")
def reg(team_id):
    """Registers a new team."""
    game = app.config["GAME"]
    resp = {}
    if team_id and len(team_id) <= 25:
        if game.get_status_code() < 200:
            if game.get_player(team_id) > 0:  # team_id is taken
                resp = {"response": "ERROR", "error_code": 2}
            else:
                player = game.add_player(team_id)
                resp = {"response": "OK", "player": player}

        else:  # game has already started
            resp = {"response": "ERROR", "error_code": 3}
    else:  # invalid team_id
        resp = {"response": "ERROR", "error_code": 1}
    return json.dumps(resp)


@app.route("/move/<team_id>/<move>")
def move(team_id, move):
    """Makes a move by a given team."""
    game = app.config["GAME"]
    valid = True
    # check team_id and if it's the given teams' turn
    player = game.get_player(team_id)
    if player < 1:  # request was not made by any of the teams; we just ignore it
        return "Unrecognized request. Correct syntax: /move/&lt;team_id&gt;/&lt;move&gt;"
    else:
        valid = (player == game.get_next_player())

    try:
        if valid:
            x_, y_, border = move.split(",")  # parse move
            x = int(x_)
            y = int(y_)
            if (x in range(game.BOARD_SIZE)) or (
                            y in range(game.BOARD_SIZE) or (border in ["top", "right", "bottom", "left"])):
                game.move(x, y, border)
            else:
                valid = False
    except:
        valid = False  # parse error => raise invalid move error

    if not valid:
        game.invalid_move(player)

    return redirect(url_for("status"))


@app.route("/restart")
def restart():
    """Restarts the game."""
    app.config["GAME"] = Game()
    return redirect(url_for("status"))


@app.route("/")
def game_monitor():
    """Loads the game monitor."""
    return app.send_static_file("monitor.html")


if __name__ == "__main__":
    app.run()
