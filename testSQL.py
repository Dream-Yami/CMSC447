import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("create table database (Name text, Id integer, Points integer)")

def_list = [
    ("Steve Smith", 211, 80),
    ("Jian Wong", 122, 92),
    ("Chris Peterson", 213, 91),
    ("Sai Patel", 524, 94),
    ("Andrew Whitehead", 425, 99),
    ("Lynn Roberts", 626, 90),
    ("Robert Sanders", 287, 75),
]

cursor.executemany("insert into database values (?,?,?)", def_list)

#print the rows
for row in cursor.execute("select * from database"):
    print(row)
    
print("******************")
cursor.execute("select * from database where Name=:c", {"c": "Steve Smith"})
rna_search = cursor.fetchall()
print(rna_search)
    
connection.commit()
connection.close()