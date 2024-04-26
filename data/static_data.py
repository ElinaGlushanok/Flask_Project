import sqlite3

keyword = 'qwerty'
con = sqlite3.connect("db/canteen.db")
cur = con.cursor()
menu = list(cur.execute(f'''select * from menu''').fetchall())
meals_available = [x[1] for x in menu]
prices = {x[1]: x[2] for x in menu}