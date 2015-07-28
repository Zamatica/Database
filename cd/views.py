__author__ = 'Zamatica'

# Python modules

# Third-party modules
from flask import render_template, escape, request

# Custom modules
from cd import app, get_db


TABLE = ' Clients '

@app.route('/')
# Defining Search Page
def index():
    return render_template('search.html')


@app.route('/search_houses/')
def search_houses():

    # Saving Search Tags
    id_user = request.args.get('ID')
    name = request.args.get('NAME')
    qbv = request.args.get('QBV')
    qbu = request.args.get('QBU')
    cse = request.args.get('CSE')

    var_range = (id_user, name, qbv, qbu, cse)

    base_op = "base LIKE 'base'"

    if id_user == '':
        id_user_op = ""
    else:
        id_user = "'" + id_user + "'"
        id_user_op = " and ID LIKE " + id_user

    if name == '':
        name_op = ""
    else:
        name = "'" + name + "'"
        name_op = " and Name LIKE " + name

    if qbv == '':
        qbv_op = ""
    else:
        qbv = "'" + qbv + "'"
        qbv_op = " and QBV LIKE " + qbv

    if qbu == '':
        qbu_op = ""
    else:
        qbu = "'" + qbu + "'"
        qbu_op = " and QBU LIKE " + qbu

    if cse == '':
        cse_op = ""
    else:
        cse = "'" + cse.upper() + "'"
        cse_op = " and CSE LIKE " + cse

    # Connect to Database
    conn = get_db()
    c = conn.cursor()

    #  SQL Statements
    if not any(var_range):
        c.execute("SELECT * From " + TABLE)
    else:
        sql = "SELECT * From" + TABLE + "WHERE " + base_op + id_user_op + name_op + qbv_op + qbu_op + cse_op + ";"
        print(sql)
        c.execute(sql)

    # Printing Data Found
    result = []
    for row in c.fetchall():
        #  Print As a Table in HTML with CSS
        text = '<div class="row"><input type="radio" name="expand">' \
               '<span class="cell primary" data-label="ID">%s</span> ' \
               '<span class="cell" data-label="Name">%s</span> ' \
               '<span class="cell" data-label="QB Version">%s</span> ' \
               '<span class="cell" data-label="QB User">%s</span> ' \
               '<span class="cell" data-label="QB Password"><span class="hide">%s</span></span> ' \
               '<span class="cell" data-label="CSE">%s</span> ' \
               '</div>' \
               % (row[0], row[1], row[2], row[3], row[4], row[5])

        result.append(text)

    # Testing if any results found, and printing none found
    if len(result) == 0:
        return "<h1 style='font-size:100px'>There are no listings that match your search.</h1>"

    # Table Style
    style = 'body{background:#cacaca;margin:0;padding:12px;font-family:"HelveticaNeue-Light","Helvetica Neue Light","Helvetica Neue",Helvetica,Arial,"Lucida Grande",sans-serif;font-weight:300}#table{display:table;width:100%;background:#fff;margin:0;box-sizing:border-box}.caption{display:block;width:100%;background:#64e0ef;height:55px;padding-left:10px;color:#fff;font-size:20px;line-height:55px;text-shadow:1px 1px 1px rgba(0,0,0,.3);box-sizing:border-box}.header-row{background:#8b8b8b;color:#fff}.row{display:table-row}.cell{display:table-cell;padding:6px;border-bottom:1px solid #e5e5e5;text-align:center}.primary{text-align:left}input[type="radio"],input[type="checkbox"]{display:none}@media only screen and (max-width: 760px){body{padding:0}#table{display:block;margin:44px 0 0}.caption{position:fixed;top:0;text-align:center;height:44px;line-height:44px;z-index:5;border-bottom:2px solid #999}.row{position:relative;display:block;border-bottom:1px solid #ccc}.header-row{display:none}.cell{display:block;border:none;position:relative;height:45px;line-height:45px;text-align:left}.primary:after{content:"";display:block;position:absolute;right:20px;top:18px;z-index:2;width:0;height:0;border-top:10px solid transparent;border-bottom:10px solid transparent;border-right:10px solid #ccc}.cell:nth-of-type(n+2){display:none}input[type="radio"],input[type="checkbox"]{display:block;position:absolute;z-index:1;width:99%;height:100%;opacity:0}input[type="radio"]:checked,input[type="checkbox"]:checked{z-index:-1}input[type="radio"]:checked ~ .cell,input[type="checkbox"]:checked ~ .cell{display:block;border-bottom:1px solid #eee}input[type="radio"]:checked ~ .cell:nth-of-type(n+2),input[type="checkbox"]:checked ~ .cell:nth-of-type(n+2){background:#e0e0e0}input[type="radio"]:checked ~ .cell:nth-of-type(n+2):before,input[type="checkbox"]:checked ~ .cell:nth-of-type(n+2):before{content:attr(data-label);display:inline-block;width:60px;background:#999;border-radius:10px;height:20px;margin-right:10px;font-size:12px;line-height:20px;text-align:center;color:#fff}input[type="radio"]:checked ~ .primary,input[type="checkbox"]:checked ~ .primary{border-bottom:2px solid #999}input[type="radio"]:checked ~ .primary:after,input[type="checkbox"]:checked ~ .primary:after{position:absolute;right:18px;top:22px;border-right:10px solid transparent;border-left:10px solid transparent;border-top:10px solid #ccc;z-index:2}}'

    # Finalizing the Print
    return '<head>' \
           ' <style>' \
           + style + \
           '</style></head> <body>'\
           '<div class="caption">Database - Clients</div>'\
           '<div id="table"><div class="header-row row">' \
           '<span class="cell primary">ID</span>' \
           '<span class="cell">Name</span>'\
           '<span class="cell">QB Version</span>' \
           '<span class="cell">QB User</span>' \
           '<span class="cell">QB Password</span>' \
           '<span class="cell">CSE</span></div>' \
           + ''.join(result) + '</div></body>'


@app.route('/all')
def all_houses():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * From Clients")
    result = []
    for row in c.fetchall():
        text = '%d - %s' % (row[0], row[1])
        result.append(text)
    return '<br>'.join(result)
