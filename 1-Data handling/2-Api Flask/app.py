from flask import Flask,jsonify,abort,request
import mysql.connector
#user:root
#password=ziadziad

db=mysql.connector.connect(host='localhost',user='root',password='ziadziad',database='sakila')

app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello Al ZoZ</h1>'


@app.get('/actors')
def actors():
    query='SELECT actor_id,first_name ,last_name FROM actor'
    results=get_results(query)
    return results

@app.get('/actors/<int:actor_id>')


def actor(actor_id):
    query='SELECT * FROM actor WHERE actor_id =%s'
    result=get_one_result(query,(actor_id,))
    return result #jsonify:in case of returning null


@app.get('/films')
#the shape of the request like :http://127.0.0.1:5000/films?rating=PG,G
def get_film_by_rating():
    ratings=request.args['rating'].split(',')
    query_placeholders=','.join(['%s'] * len(ratings)) #will return number of symploes %s equal number of ratings i send 
    #to the request ,note i need to send varibles in %s to protect my database
    query=f'SELECT film_id ,description,release_year,length,rental_rate, rating FROM film WHERE rating IN ({query_placeholders})' 
    results=get_results(query,tuple(ratings))
    return results




def get_results(query,*argus):
    cursor=db.cursor(dictionary=True)#dictionary=True :will make the results comes with it is keys
    cursor.execute(query,*argus)
    results=cursor.fetchall()
    cursor.close()
    #jsonify:in case of returning null
    return jsonify(results) if results else abort(404)

def get_one_result(query,*argus):
    cursor=db.cursor(dictionary=True)
    cursor.execute(query,*argus)
    result=cursor.fetchone()
    cursor.close()
    return jsonify(result) if result else abort(404)

if __name__=='__main__':
    app.run(debug=True)
