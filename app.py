from flask import Flask ,render_template,request,redirect,session
from cs50 import SQL
from random import randint
db=SQL("sqlite:///usersss.db")


app = Flask(__name__)
app.secret_key = 'oq#k^yZeAq7eda7)i8K7(Sdn9WCbU!&%'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet",methods=["GET", "POST"])
def drie():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        tot=0
        for i in password:
            d = (ord(i) / 2) + 3 * ord(i)*ord(i)+23453235452532525
            tot += d
        user=db.execute("select * from users where name=?and password=?", name, tot)
        if user:
            session['name'] = name
            return redirect("/auth")
        else:
            return render_template("fout.html")
@app.route("/auth")
def auth():
    if "name" in session:
        name = session['name']
        user=db.execute("SELECT * FROM users WHERE name = ?", name)
        if user:
            return render_template("tweede.html",user=user)
        else:
            return render_template("fout.html")
    return render_template("index.html")


@app.route("/login" , methods = ["get","Post"])
def login():
    return render_template("login.html")

@app.route("/home",methods=["get","post"])
def home():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        tot = 0
        for i in password:
            d = (ord(i) / 2) + 3 * ord(i)*ord(i)+23453235452532525
            tot += d
        if name and password:
            id= randint(10000000,1000000000)
            idd=int(id)
            balance=randint(1,3000)
            db.execute("Insert into users (idd,name,password,balance) VALUES(?,?,?,?)",idd,name,tot,balance)
            return redirect("/regdon")
        return redirect("/fout")
    return redirect("/login")

@app.route("/regdon")
def appdon():
    return render_template("home.html")

@app.route("/fout")
def fout():
    return render_template("fout.html")
@app.route("/logout")
def logout():
    session.clear()
    return render_template("/index.html")
@app.route("/search")
def search():
    name = session['name']
    user=db.execute("SELECT * FROM users WHERE name = ?", name)
    q=request.args.get("overschrijven")
    show=db.execute("select * from users where name LIKE ? order by name","%"+q+"%")
    return render_template("res.html",show=show,q=q,user=user)
@app.route("/over")
def over():
    name = session['name']
    user=db.execute("SELECT * FROM users WHERE name = ?", name)
    return render_template("over.html",user=user)
@app.route("/overs")
def update_balance():
    nummer = request.args.get("begunstigde")
    bedrag = int(request.args.get("bedrag"))
    name = session['name']

    # Get the current balance of the user
    user = db.execute("SELECT balance FROM users WHERE name = ?", name)
    if not user:
        return "User not found", 404

    current_balance = user[0]["balance"]

    # Calculate the new balance for the user
    new_balance = current_balance - bedrag
    beg = db.execute("SELECT balance FROM users WHERE idd = ?", nummer)
    if not beg:
        return "Beneficiary not found", 404

    # Update the user's balance
    db.execute("UPDATE users SET balance = ? WHERE name = ?", new_balance, name)

    # Get the current balance of the beneficiary


    beneficiary_balance = beg[0]["balance"]

    # Calculate the new balance for the beneficiary
    new_beneficiary_balance = beneficiary_balance + bedrag

    # Update the beneficiary's balance
    db.execute("UPDATE users SET balance = ? WHERE idd = ?", new_beneficiary_balance, nummer)

    # Get the updated user information
    updated_user = db.execute("SELECT * FROM users WHERE name = ?", name)

    return render_template("tweede.html", user=updated_user)
if __name__=='__main__':
    app.run(debug=True)
