// set class for board game//

class BoggleGameBoard {
  constructor(boardID, secs = 60) {
    this.secs = secs; // game length
    this.showTimer();

    this.score = 0; // sets the score to 0 in a new game
    this.words = new Set(); // contains the words that we put into the form
    this.board = $("#" + boardID); // grabs the id of board from the html

    this.timer = setInterval(this.tick.bind(this), 1000); // sets the timer and reduces it by 1 sec

    // grabs the "add-word" class from the HTML when submit action is made and calls the submit function from the app.py
    $(".add-word", this.board).on("submit", this.submit.bind(this));
  }

  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
    // grabs the words class from this.board and creates a new Li and appends the text as the word passed into the function
  }

  showMessage(msg, cls) {
    // grabs the msg class from this.board and sets the text = to the msg passed in, removes the class and adds the class "msg {class name}"
    $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  async submit(evt) {
    evt.preventDefault(); // stops the page from reloading
    const $word = $(".word", this.board); // sets the varaible = to the words class from this.board
    let word = $word.val(); // sets the word variable = the value inputted onto the word class
    if (!word) return; // if it is not a word, return nothing

    if (this.words.has(word)) {
      // if the set already has the word being inputted, show the message
      this.showMessage(`Already Submitted ${word}`, "err");
      return;
    }
    const resp = await axios.get("/check-word", { params: { word: word } });

    // use axios to wait for /check-word to load and provide the word inputted

    if (resp.data.result === "not-word") {
      // if the word is equal to the "not-word" result located in our boggle.py, show the message that it is not a valid word
      this.showMessage(`${word} is not a valid English word`, "err");
    } else if (resp.data.result === "not-on-board") {
      // if it is not on the board, show the message below
      this.showMessage(`${word} is not a valid word on this board`, "err");
    } else {
      // if it is successful and it is a word
      this.showWord(word); // pass the word through show word function to show it on the page
      this.score += word.length; // add the length of the word to our score
      this.words.add(word); // add the word to the set of words
      this.showMessage(`Added: ${word}`, "ok"); // show a message ot indicate success
    }

    $word.val("").focus();
  }

  showTimer() {
    $(".timer", this.board).text(this.secs);
  }

  /* Tick: handle a second passing in game */

  async tick() {
    this.secs -= 1; // subtracts 1 from the sec = 60
    this.showTimer(); // shows the timer fucntion created above

    if (this.secs === 0) {
      clearInterval(this.timer); // when timer reaches 0, clear the ticks and wait for scoregame function to run
      await this.scoreGame();
    }
  }

  /* end of game: score and update message. */

  async scoreGame() {
    $(".add-word", this.board).hide(); // hide the form
    const resp = await axios.post("/post-score", { score: this.score }); // wait for /post score function to run from the app.py and set score = this.score from the class.
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, "ok"); // if brokeRecord varaible is ran, show this message, else the the bottom one
    } else {
      this.showMessage(`Final score: ${this.score}`, "ok");
    }
  }
}
