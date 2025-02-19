from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config= {  "apiKey": "AIzaSyBTD1_WQUBJ5t7UWfFc9xHJLCHG_o0oIhU",
  "authDomain": "fir-a0dbe.firebaseapp.com",
  "projectId": "fir-a0dbe",
  "storageBucket": "fir-a0dbe.appspot.com",
  "messagingSenderId": "958079824524",
  "appId": "1:958079824524:web:cbe0f305dc58bd756141a9",
  "measurementId": "G-EY4EWX8E62",
  "databaseURL": "https://fir-a0dbe-default-rtdb.firebaseio.com/"
}


firebase=pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            user = {"name": "Fouad", "email": "f@h.com"}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        try:
            tweet = {"name": request.form['name'],"content": request.form['content'], "uid": login_session['user']['localId']}
            db.child("tweet").push(tweet)
        except:
            print(" sorry Couldn't add tweet , try again ")
    return render_template("add_tweet.html")




@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweet():
    tweet=db.child("tweet").get().val()
    return render_template("all_tweet.html")





if __name__ == '__main__':
    app.run(debug=True)