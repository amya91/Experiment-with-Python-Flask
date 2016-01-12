from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, redirect, request
#from flaskext.mysql import MySQL
app = Flask(__name__)

url = ""
page_title = ""
meta_desc = ""

@app.route('/')
def form_basic():
    return render_template('index.html')

@app.route('/formfill', methods = ['POST'])
def formfill():
    global page_title,meta_desc,url
    url = request.form['input']
    html = requests.get(url, headers={'Accept-Encoding': None}).text
    soup = BeautifulSoup(html,"html.parser")
    global page_title,meta_desc
    if soup.find("title") is not None:
        page_title = soup.find("title").getText()
    else:
        page_title = "Not Available"
    if soup.findAll(attrs={"name":"description"})!=[]:
        meta_desc = soup.findAll(attrs={"name":"description"})[0]['content']
    else:
        meta_desc = "Not Available"
    return redirect('/formout')

@app.route('/formout')
def formout():
    return render_template('index2.html',pagetitle=page_title,metadesc=meta_desc)

@app.route('/formfinal', methods = ['POST'])
def formfinal():
    edited_title = request.form['editedtitle']
    edited_metadesc = request.form['editedmetadesc']
    print url
    print edited_title
    print edited_metadesc
    return redirect('/')

"""mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)"""

if __name__ == "__main__":
    app.run()
