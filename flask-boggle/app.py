from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
boggle_game = Boggle()


app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"


""" Home page route"""
@app.route("/")
def home():
    return render_template("home.html")


""" Board Game Route"""
@app.route("/board", methods = ["POST"])
def homepage():
    """Show board."""
    """Set board game up using the function given in boggle.py"""
    board = boggle_game.make_board()
    
    """set cookies session name to "board" and set that equal to the board game"""
    session['board'] = board
    
    """ resets the high score and number of times played to 0 from our session["board"] which created our board page """
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    print(session["board"])
    return render_template("board.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


""" Check Validility of word in the check-word route"""

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    """ The word variable is set to the request sent to our html under the NAME word """
    
    word = request.args["word"]
    
    """ Setting board = to session["board"] again to use in this route and update our cookies"""
    board = session["board"]
    
    """the response is = to our booggle.py page, calling the function check_valid_word and putting the parameters of our board date and the word recived from the input"""
    
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})





"""Post scores route used for scoring"""


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    """score varaible is = to the json which we recieved from the check-word route. """

    score = request.json["score"]
    
    """the highscore and num of plays is recieved from the session and starts at 0"""
    
    highscore = session.get("highscore", 0)
    
    nplays = session.get("nplays", 0)


    """ number of plays goes up by 1 evverytime this function is called"""
    session['nplays'] = nplays + 1
    
    """ the highscore displays the max number contained in the sesssion and sets it as the highscore, it places the max number to it, wheter its the score now or a previous highscore"""
    session['highscore'] = max(score, highscore)



    return jsonify(brokeRecord=score > highscore)
