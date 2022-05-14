#Imports
from pydoc import render_doc
from unittest import result
from flask import Flask, flash, request, render_template, session
from markupsafe import escape
import pymongo
from pymongo import MongoClient
import uuid

#Init change values here
signup_pw="signingup!!!"
connection_id="mongodb://localhost:27017"
cluster = MongoClient(connection_id)
db = cluster["tickets"]
collection = db["tickets"]
app = Flask(__name__)

#Routes
#Hosts the actual part of the ticket. 
@app.route('/ticket/<id>')
def ticket(id):
    try:
        tickets=collection.find({"_id": id})
        for ticket in tickets:
            print(ticket["ticket_id"])
            return render_template("ticket.html", id=ticket["ticket_id"])
        else:
            return render_template("naticket.html")
    except:
        return render_template("error.html")

#Signup, make sure to set your password correctly.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        password=request.form.get('passw')
        if password == signup_pw:
            email=request.form.get('email').lower()
            name=request.form.get('name').lower()
            post={"_id": str(uuid.uuid4()), "email": email, "ticket_id": str(uuid.uuid4().hex[:5]), "name": name, "arrived": False}
            collection.insert_one(post)
            print(post)
            return str(post)
        else:
            return render_template("error.html")
    else:
        return render_template("signup.html")

#This part hosts the ticket checking service, we set the ticket as arrived after the user arrives. 
@app.route('/chktick', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        id=request.form.get('id')
        try:
            tickets=collection.find_one({"ticket_id": id})
            if tickets["arrived"] == False:
                result = collection.update_one({"ticket_id": id}, {"$set":{"arrived":True}})
                return render_template("signed_in.html")
                
                
            else:
                return render_template("already_signed_in.html")
        except:
            return render_template("error.html")
    else:
        return render_template("chktick.html")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)