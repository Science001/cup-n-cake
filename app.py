from flask import Flask, render_template, request, session, abort, redirect, url_for
from passlib.hash import sha256_crypt
from varieties import varieties
from users import users
import json

app = Flask('__name__')
app.secret_key = "sdhubvclSHDBvlcshIDBvluSBDvlhuLSDJvlKJ"

@app.route('/')
def home():
    if session:
        return render_template("index.html", varieties=varieties, jsonVarieties=json.dumps(varieties), loggedIn=True, user=session['user'])
    else:
        return render_template("index.html", varieties=varieties, jsonVarieties=json.dumps(varieties), loggedIn=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        for user in users:
            if(user["email"] == email):
                if(sha256_crypt.verify(password, user["password"])):
                    session['user'] = user
                    return redirect(url_for("home"))
                    break
                else:
                    return render_template("login.html", error=True)
        else:
            return render_template("login.html", error=True)
    elif(session):
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        for user in users:
            if(user["email"] == email):
                return render_template("login.html", signup=True, error=True)
        user = {
            "email": email,
            "password": sha256_crypt.hash(password),
            "address": address,
        }
        users.append(user)
        session['user'] = user
        return redirect(url_for("home"))
    elif(session):
        return redirect(url_for("home"))
    else:
        return render_template("login.html", signup=True)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)