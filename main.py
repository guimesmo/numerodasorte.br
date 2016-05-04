import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')
setup_vars = {
    "NDS_DBUSER": os.environ["NDS_DBUSER"],
    "NDS_DBPWD": os.environ["NDS_DBPWD"],
    "NDS_DBHOST": os.environ["NDS_DBHOST"],
    "NDS_DBNAME": os.environ["NDS_DBNAME"],
}
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{NDS_DBUSER}:{NDS_DBPWD}@{NDS_DBHOST}/{NDS_DBNAME}".format(**setup_vars)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')
def main_page():
    from registrador_de_numero import get_latest_number, generate_data_table, generate_number
    generate_number()
    latest_number = get_latest_number()
    latest_number = "</span> <span>".join(latest_number.split("-"))
    latest_number = "<span>%s</span>" % latest_number
    data_table = generate_data_table()
    return render_template('index.html', latest_number=latest_number, data_table=data_table)

if __name__ == '__main__':
    app.run()
