import sqlite3
#import random
from flask import Flask, session, render_template, request, g
app = Flask(__name__)
app.secret_key = "dreaming_City"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form['retType'] == "CREATE":
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            
            name = request.form['Name']
            id = request.form['Id']
            points = request.form['Points']
            def_list = [(name, id, points)]
            #Check to see if name already exsists
            cursor.execute("select * from database where Name=:c", {"c": name})
            exists = cursor.fetchall()
            print(exists)
            if len(exists) > 0:
                rows = pull_db()
                return render_template('base.html', message = name + " already exists in database", rows = rows)
            cursor.executemany("insert into database values (?,?,?)", def_list)
            message = "Inserted " + name + " to Database!"
            connection.commit()
            connection.close()
            
            rows = pull_db()
            return render_template('base.html', message = message, rows = rows)
    
        elif request.form['retType'] == "SEARCH":
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            
            name = request.form['Name']
            #Check to see if name already exsists
            cursor.execute("select * from database where Name=:c", {"c": name})
            exists = cursor.fetchall()
            print(exists)
            if len(exists) == 0:
                rows = pull_db()
                return render_template('base.html', message = name + " doesn't exist on database", rows = rows)

            connection.commit()
            connection.close()
            rows = pull_db()
            return render_template('base.html', message = name + " found! ID: " + str(exists[0][1]) + " Points: " + str(exists[0][2]), rows = rows)
    
        elif request.form['retType'] == "DELETE":
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            
            name = request.form['Name']
            #Check to see if name already exsists
            cursor.execute("select * from database where Name=:c", {"c": name})
            exists = cursor.fetchall()
            print(exists)
            if len(exists) == 0:
                rows = pull_db()
                return render_template('base.html', message = name + " doesn't exist on database", rows = rows)

            cursor.execute("delete from database where Name=:c", {"c": name})
            connection.commit()
            connection.close()
            rows = pull_db()
            return render_template('base.html', message = "Deleted " + name + " from Database", rows = rows)
        
        elif request.form['retType'] == "UPDATE":
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            
            name = request.form['Name']
            id = request.form['Id']
            points = request.form['Points']
            #Check to see if name already exsists
            cursor.execute("select * from database where Name=:c", {"c": name})
            exists = cursor.fetchall()
            print(exists)
            if len(exists) == 0:
                rows = pull_db()
                print("Catch test")
                return render_template('base.html', message = name + " doesn't exist on database", rows = rows)
            
            toExec = "update database set ID = ? , Points = ? where Name = ?"
            cursor.execute(toExec, (id, points, name))
            message = "Updated " + name + " on the database!"
            connection.commit()
            connection.close()
            
            rows = pull_db()
            return render_template('base.html', message = message, rows = rows)
        
    rows = pull_db()
    return render_template('base.html', message = 'Please Select An Option', rows = rows)

def pull_db():
    db = getattr(g, '_database', None)
    if db == None:
        db = g._database = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("select * from database")
    toRet = cursor.fetchall()
    #print(toRet)
    return toRet
        
@app.teardown_appcontext
def close_conn(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()