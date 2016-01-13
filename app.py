from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, redirect, request
from flask import Flask
from flask.ext.mysqldb import MySQL
import MySQLdb
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
    try:
        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="qwerty123",  # your password
                             db="db1")        # name of the data base
        cur = db.cursor()
        # Use all the SQL you like
        cur.execute("INSERT into crawldata(url,title,metadesc)VALUES (%s,%s,%s)",(url.encode('utf-8'),edited_title.encode('utf-8'),edited_metadesc.encode('utf-8')))
        db.commit()
        cur.execute("SELECT * FROM crawldata")
        # print all the first cell of all the rows
        for row in cur.fetchall():
            print row
        db.close()

    except Exception as e:
        print 'E: ', e
    return redirect('/')


if __name__ == "__main__":
    app.run()
                                                                                                                                                      1,1           Top
