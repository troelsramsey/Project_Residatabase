from flask import Flask, render_template
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'
# set your own database name, user name and password
db = "dbname='postgres' user='postgres' host='localhost' password='1519'" #potentially wrong password
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from bank.indskrivning.routes import Indskrivning
app.register_blueprint(Indskrivning)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#from bank import routes
