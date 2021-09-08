from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:rootpassword@localhost/db1'
db = SQLAlchemy(app)


class blog_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    blog = db.Column(db.String(200), unique=False, nullable=False)


@app.route("/")
def home():
    return render_template('adduser.html')


@app.route("/GET")
def get_user():

    user = blog_table.query.all()
    l1=[]
    for e in user:
        user_dict= {"name" : e.username, "email" : e.email,'blog': e.blog}
        l1.append(user_dict)
    return {"UserInfo": l1}


@app.route("/POST", methods=['POST'])
def post_user():
    name = request.form['uname']
    email = request.form['email']
    blog = request.form['blog']
    s1 = blog_table(username=name, email=email, blog=blog)
    db.session.add(s1)
    db.session.commit()
    return {
            "status" : 200,
            }


@app.route("/DELETE/<string:name>")
def delete_user(name):
    blog_table.query.filter_by(username=name).delete()
    db.session.commit()

    return {"Status": 200
            }


if __name__=="__main__":
    app.run(debug=True)
