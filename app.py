from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "numy_secret"

# -------------------------
# GLOBAL DATA
# -------------------------

visitors = 0
battles = 0

ratings = {
    "RCB":1500,
    "SRH":1500
}

clicks = {
    "RCB":0,
    "SRH":0
}

# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():

    global visitors

    # count visitor only once
    if not session.get("visited"):
        visitors += 1
        session["visited"] = True

    return render_template(
        "IPL-1.html",
        visitors=visitors,
        battles=battles,
        ratings=ratings
    )


# -------------------------
# VOTE SYSTEM
# -------------------------

@app.route("/vote", methods=["POST"])
def vote():

    global battles

    if session.get("voted"):
        return jsonify({
            "status":"already_voted",
            "ratings":ratings,
            "clicks":clicks
        })

    data = request.get_json()
    winner = data["team"]

    if winner == "RCB":
        loser = "SRH"
    else:
        loser = "RCB"

    clicks[winner] += 1

    Ra = ratings[winner]
    Rb = ratings[loser]

    K = 32

    Ea = 1/(1+10**((Rb-Ra)/400))
    Eb = 1/(1+10**((Ra-Rb)/400))

    ratings[winner] = round(Ra + K*(1-Ea))
    ratings[loser] = round(Rb + K*(0-Eb))

    session["voted"] = True
    battles += 1

    return jsonify({
    "status": "success",
    "ratings": ratings,
    "clicks": clicks
})
# -------------------------
# ADMIN REFRESH
# -------------------------

@app.route("/refresh/<secret>")
def refresh(secret):

    if secret == "numyadmin123":   # your secret key

        session.pop("voted", None)
        session.pop("team", None)

        return redirect(url_for("home"))

    else:
        return "Access Denied 🚫"


# -------------------------
# OTHER PAGES
# -------------------------

@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/feedback.html")
def feedback():
    return render_template("feedback.html")


@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/idea.html")
def idea():
    return render_template("idea.html")


# -------------------------
# SECRET STATS PAGE
# -------------------------

@app.route("/numy-pie-stats")
def stats():

    return f"""
    <h1>📊 NUMY PIE STATS</h1>

    <h2>Total Visitors 👀 : {visitors}</h2>
    <h2>Total Battles Played 🎮 : {battles}</h2>

    <h3>RCB Votes 🔴 : {clicks["RCB"]}</h3>
    <h3>SRH Votes 🟠 : {clicks["SRH"]}</h3>

    """
    

# CEO RESET SYSTEM
@app.route("/ceo-reset")
def ceo_reset():

    global ratings
    global battles
    global visitors

    # reset ratings
    ratings = {
        "RCB":1500,
        "SRH":1500
    }

    # reset stats
    battles = 0
    visitors = 0

    # reset votes
    session.clear()

    return "System Reset Successful ✅"    


# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
