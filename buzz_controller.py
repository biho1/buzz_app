from flask import Flask, render_template_string, request, redirect, session, url_for, jsonify
import pyautogui
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key'

KEY_MAPPING = {
    1: {'big': '1', 'blue': 'q', 'orange': 'w', 'green': 'e', 'yellow': 'r'},
    2: {'big': '2', 'blue': 'a', 'orange': 's', 'green': 'd', 'yellow': 'f'},
    3: {'big': '3', 'blue': 'z', 'orange': 'x', 'green': 'c', 'yellow': 'v'},
    4: {'big': '4', 'blue': 'u', 'orange': 'i', 'green': 'o', 'yellow': 'p'},
}

# HTML for selecting player
SELECT_PLAYER_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Select Player</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <style>
    body { font-family: sans-serif; text-align: center; padding: 2em; }
    select, button { font-size: 18px; padding: 12px; margin: 10px; }
  </style>
</head>
<body>
  <h1>Select Your Player</h1>
  <form method="POST" action="/set_player">
    <select name="player">
      {% for p in range(1, 5) %}
        <option value="{{ p }}">Player {{ p }}</option>
      {% endfor %}
    </select>
    <br>
    <button type="submit">Start</button>
  </form>
</body>
</html>
"""

# HTML for buzzer UI
CONTROLLER_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Buzz Controller – Player {{ player }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
  <style>
    body {
      font-family: sans-serif;
      text-align: center;
      background-color: #111;
      color: white;
      margin: 0;
      padding: 0;
    }
    h1 {
      margin: 1em 0 0.5em;
    }
    .controller {
      margin: auto;
      padding: 1em;
    }
    .big-button {
      width: 70vw;
      max-width: 250px;
      height: 70vw;
      max-height: 250px;
      background-color: red;
      border: none;
      border-radius: 50%;
      font-size: 24px;
      color: white;
      margin-bottom: 20px;
    }
    .button-stack {
      display: flex;
      flex-direction: column;
      gap: 12px;
      align-items: center;
    }
    .color-button {
      width: 70vw;
      max-width: 250px;
      height: 50px;
      font-size: 18px;
      color: white;
      border: none;
      border-radius: 10px;
    }
    .blue { background-color: #007bff; }
    .orange { background-color: orange; }
    .green { background-color: green; }
    .yellow { background-color: gold; color: black; }
    .switch {
      margin-top: 2em;
    }
    button:active {
      transform: scale(0.96);
    }
    html, body {
  touch-action: manipulation;
  -webkit-text-size-adjust: 100%;
  font-size: 18px; /* Minimum tap size for iOS */
  }
  </style>
</head>
<body>
  <h1>Buzz! – Player {{ player }}</h1>
  <div class="controller">
  <form method="POST" action="/press" class="controller">
    <input type="hidden" name="player" value="{{ player }}">
    <button name="button" value="big" class="big-button">BUZZ</button>
    <div class="button-stack">
      <button name="button" value="blue" class="color-button blue">Blue</button>
      <button name="button" value="orange" class="color-button orange">Orange</button>
      <button name="button" value="green" class="color-button green">Green</button>
      <button name="button" value="yellow" class="color-button yellow">Yellow</button>
    </div>
  </form>
    <div class="switch">
      <form method="GET" action="/logout">
        <button>Switch Player</button>
      </form>
    </div>
  </div>
  <script>
    function press(button) {
      fetch("/press", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ player: {{ player }}, button })
      }).then(res => res.json()).then(data => {
        console.log(data.status);
      });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    if 'player' not in session:
        return render_template_string(SELECT_PLAYER_HTML)
    return render_template_string(CONTROLLER_HTML, player=session['player'])

@app.route('/set_player', methods=['POST'])
def set_player():
    session['player'] = int(request.form['player'])
    return redirect(url_for('index'))

#@app.route('/press', methods=['POST'])
# def press_key():
#     data = request.get_json()
#     player = data.get('player')
#     button = data.get('button')
#     if player not in KEY_MAPPING or button not in KEY_MAPPING[player]:
#         return jsonify({"status": "error"}), 400
#     key = KEY_MAPPING[player][button]
#     threading.Thread(target=pyautogui.press, args=(key,)).start()
#     return jsonify({"status": f"Player {player} pressed {button} ({key})"})

@app.route('/press', methods=['POST'])
def press_key():
    if 'player' not in request.form or 'button' not in request.form:
        return "Missing form data", 400

    try:
        player = int(request.form['player'])
        button = request.form['button']
        key = KEY_MAPPING[player][button]
    except Exception as e:
        print("Error:", e)
        return "Invalid input", 400

    def hold_key():
        pyautogui.keyDown(key)
        time.sleep(0.1)
        pyautogui.keyUp(key)

    threading.Thread(target=hold_key).start()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    import webbrowser
    import threading
    threading.Timer(1.0, lambda: webbrowser.open("http://localhost:80")).start()
    app.run(host="0.0.0.0", port=80)
