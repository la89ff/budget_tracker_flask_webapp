#import dependencies
from flask import Flask, render_template, request, Response
import csv

#set container for running flask
app = Flask(__name__)

data = []
with open("./transactions.csv", mode="r") as transactions_file:
    reader = csv.reader(transactions_file)
    next(reader)
    for row in reader:
        date = row[0]
        i_or_e = row[1]
        amount = row[2]
        desc = row[3]
        data.append({'date': date, 'income or expense': i_or_e, 'amount': amount, 'description': desc})

#index to greet the viewer
@app.route("/") #default 'GET' method
def home():
    return render_template("index.html", data=data)

#view all of the items in the csv
@app.route("/view") #default 'GET' method
def view():
    return render_template("view.html", data=data)

#view a user defined item from the data
@app.route("/view/<id>")
def view_id(id):
    #conterting id into int and minusing 1 from the id value to account for python 0 list indexing
    id = int(id)-1
    #not allowing negative number input
    if id < 0:
        id = 'not allowed'
    #render template or deal with exception
    try:
        return render_template("view_id.html", data=data[id])
    except:
        return 'the data requested does not exist in the dataset'

#route to allow user to input their data to add in a form
@app.route("/add") #default of GET method
def add():
    return render_template("add.html")

#route that handles the POST request to allow user to push into dataset
@app.route("/add", methods=['POST'])
def add_post():
    if request.method == 'POST':
        #create receiver for post data
        new_data = {}
        #store the post data
        new_data['date'] = request.form["date"]
        new_data['income or expense'] = request.form["i_or_e"]
        new_data['amount'] = request.form["amount"]
        new_data['description'] = request.form["description"]
        #open the csv file and append the post data into it
        with open('transactions.csv', 'a') as append_file:
            append_file.write(f"{new_data['date']},{new_data['income or expense']},{new_data['amount']},{new_data['description']}\n")
        #append the post data into the list of dict db
        data.append(new_data)
        return render_template("add_success.html")
        
#serve the app
if __name__ == '__main__':
    app.run(debug=True)