from flask import Flask, render_template, request, jsonify
import psycopg2
import json
from pprint import pprint

app = Flask(__name__)
def connect_db():
    try:
        sql = psycopg2.connect(user = "postgres",
                                        password="abcd1234",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="eecs341")
        return sql
    except:
        print("Unable connect to the database") 

def getQ(input="select * from player"):
    cursor = connect_db().cursor()
    postgreSQL_select_Query = input

    cursor.execute(postgreSQL_select_Query)
    row_headers =[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

@app.route('/player', methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        query =  "SELECT player_name FROM player, game WHERE game.game_id = '{}'".format(request.form.get('gameID'))
        return '<h1>{}<h1>'.format(getQ(query))
    return render_template('add_food.html')

if __name__ == '__main__':
    app.run(debug=True)
