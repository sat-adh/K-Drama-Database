from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')



@app.route('/search',methods = ['POST', 'GET'])
def search():
      kname = request.form['title']
      
      con = sql.connect("ALLDATA.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from kdrama where title like '%'||?||'%'", (kname,))
      
      msg = "Your Search did not Match any K-Dramas"
      msg2 = "Your Search Matches the Following K-Dramas:"

      rows = cur.fetchall()

      if len(rows) == 0:
         return render_template("searchResult.html",msg = msg)
      else:
         return render_template("searchResult.html",rows = rows,msg2 = msg2)

        


@app.route('/getActors',methods = ['POST', 'GET'])
def getActors():
      kd_id = request.form['kd_id']
      
      con = sql.connect("ALLDATA.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select actor.id,actor.name,actor.gender,actor.age from actor join kdrama_actor on actor.id = kdrama_actor.ac_id join kdrama on kdrama.id = kdrama_actor.k_id where kdrama.id=? ",(kd_id,))
      
      rows = cur.fetchall()

      cur2 = con.cursor()
      cur2.execute("select * from kdrama where id=?",(kd_id,))

      kd_title = cur2.fetchone()[1]

      return render_template("actorsResult.html",rows = rows, kd_id=kd_id, kd_title=kd_title)



        
@app.route('/getActorsShows',methods = ['POST', 'GET'])
def getActorsShows():
      ac_id = request.form['ac_id']
      
      con = sql.connect("ALLDATA.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select kdrama.id,kdrama.title,kdrama.year,kdrama.rating,kdrama.numberOfEpisodes,kdrama.avgEpisodeLength from kdrama join kdrama_actor on kdrama.id = kdrama_actor.k_id join actor on actor.id = kdrama_actor.ac_id where actor.id=? ",(ac_id,))

      rows = cur.fetchall()

      cur2 = con.cursor()
      cur2.execute("select * from actor where id=?",(ac_id,))

      ac_name = cur2.fetchone()[1]

      return render_template("actorsShowsResult.html",rows = rows, ac_id=ac_id, ac_name=ac_name)

   

      
@app.route('/listTop20')
def listTop20():
   con = sql.connect("ALLDATA.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from kdrama order by rating desc limit 20")
   
   rows = cur.fetchall(); 
   return render_template("listTop.html",rows = rows)


@app.route('/listNewest20')
def listNewest20():
   con = sql.connect("ALLDATA.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from kdrama order by year desc limit 20")
   
   rows = cur.fetchall(); 
   return render_template("listNewest.html",rows = rows)

        
@app.route('/genreShows',methods = ['POST', 'GET'])
def genreShows():
      selected = request.form['gnr']
      
      con = sql.connect("ALLDATA.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select kdrama.id,kdrama.title,kdrama.year,kdrama.rating,kdrama.numberOfEpisodes,kdrama.avgEpisodeLength from kdrama join kdrama_genre on kdrama.id = kdrama_genre.k_id join genre on genre.id = kdrama_genre.g_id where genre.name=? ",(selected,))

      rows = cur.fetchall()
      return render_template("genreShowsResult.html",rows = rows, selected=selected)
   



if __name__ == '__main__':
   app.run(debug = True)