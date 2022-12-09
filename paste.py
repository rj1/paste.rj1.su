import bottle
from bottle import template, response, request, HTTPError, static_file, redirect
from bottle.ext import sqlite
from hashids import Hashids
import pygments.lexers
from pygments import highlight
from pygments.formatters import HtmlFormatter
from datetime import datetime


app = bottle.Bottle()
app.install(bottle.ext.sqlite.Plugin(dbfile="paste.db"))
hashids = Hashids(salt="", min_length="3")


@app.get("/")
def index():
    return redirect("https://rj1.su/")


@app.get("/style.css")
def stylesheet():
    return static_file("/style.css", root=".")


@app.get("/<hashed>")
def share_paste(hashed, db):
    id = hashids.decrypt(hashed)
    if len(id) == 0:
        return HTTPError(404, "404")

    row = db.execute("select * from paste where docid = ?", (id[0],)).fetchone()
    if not row:
        return HTTPError(404, "404")

    syntax = request.query_string
    if not syntax:
        response.content_type = "text/plain; charset=UTF-8"
        return row[0]

    try:
        lexer = pygments.lexers.get_lexer_by_name(syntax)
    except:
        lexer = pygments.lexers.TextLexer()

    response.content_type = "text/html; charset=UTF-8"
    return highlight(
        row[0],
        lexer,
        HtmlFormatter(
            full=True,
            cssfile="style.css",
            noclobber_cssfile=True,
            lineanchors="n",
            linenos="table",
            encoding="utf-8",
        ),
    )


@app.post("/")
def receive_paste(db):
    response.content_type = "text/plain; charset=UTF-8"
    paste = request.forms.get("paste")
    cur = db.cursor()
    cur.execute("insert into paste values(?,?)", (paste, datetime.now().isoformat()))
    id = cur.lastrowid
    hashed = hashids.encrypt(id)
    return "https://paste.rj1.su/" + hashed + "\n"


# app.run(port=55555, host="0.0.0.0")
