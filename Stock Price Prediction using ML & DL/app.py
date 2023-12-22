from flask import Flask, render_template, request
from model import search, stockpredict
import sqlite3


app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    
    
    name = request.args.get('username','')
    number = request.args.get('number','')
    email = request.args.get('email','')
    password = request.args.get('password','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `detail` (`name`,`number`,`email`, `password`) VALUES (?, ?, ?, ?)",(name,number,email,password))
    con.commit()
    con.close()

    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from detail where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("home.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/requestStock', methods=['POST'])
def requestStock():
    text = request.form['sname']
    stockName = text.upper()
    print(stockName)
    if(search(stockName)):
        return displayStock(stockName)
    else:
        return predictStock(stockName)

def displayStock(stockName):
    stockData = []
    with open('static/stocks/'+stockName+'/'+stockName+'.txt', 'r') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            stockData.append(currentPlace)
    return render_template("stockdetail.html", stockName = stockName, stockData=stockData)

def predictStock(stockName):
    stockData=stockpredict(stockName)
    return render_template("stockdetail.html", stockName = stockName, stockData=stockData)

@app.route('/signout')
def signout():
	return render_template('signin.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/about')
def about():
	return render_template('about.html')

    
if __name__ == "__main__":
    app.run(debug=False)
