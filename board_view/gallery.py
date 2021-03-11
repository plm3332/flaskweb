from flask import Flask, Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from db_model.mongodb import conn_board
import datetime

gallery_search = Blueprint('gallery', __name__, static_folder='../static')

@gallery_search.route('/<gall_name>')
def gall(gall_name):
    cap_gall_name = gall_name.capitalize()
    collection = conn_board('boardtype')
    result = collection.find_one({'name': cap_gall_name})
    krname = result['krname']

    collection = conn_board('boardall')
    result = collection.find({'gall': gall_name})

    if current_user.is_authenticated:
        return render_template('gallery.html', gname=gall_name, gall_name = krname, userinfo=current_user.user_name, data=result)
    return render_template('gallery.html', gname=gall_name, gall_name = krname, data=result)

@gallery_search.route('/<gall_name>/write')
def write(gall_name):
    if current_user.is_authenticated:
        return render_template('write.html', gname=gall_name, userinfo=current_user.user_name)
    else:
        return redirect(url_for('signup'))

@gallery_search.route('/<gall_name>/save', methods=['POST'])
def save(gall_name):
    collection = conn_board('counters')
    collection.update_one({'collection':'boardall'}, {'$inc':{'c_id':1}})
    counter = collection.find_one({'collection':'boardall'})
    gall_id = counter['c_id']

    collection = conn_board('boardall')

    user_name = current_user.user_name
    gall_title = request.form['gall_title']
    gall_content = request.form['gall_content']
    hit = 0
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

    collection.insert_one({
        'gallid' : int(gall_id),
        'name' : user_name,
        'title': gall_title, 
        'content' : gall_content,
        'hit' : 0,
        'datetime' : nowDatetime,
        'gall' : gall_name
    })

    return redirect(url_for('gallery.gall', gall_name=gall_name))

@gallery_search.route('/<gall_name>/<gall_id>')
def lookup(gall_name, gall_id):
    collection = conn_board('boardall')
    collection.update_one({'gallid': int(gall_id)}, {'$inc': {'hit': 1}})
    result = collection.find_one({'gallid': int(gall_id)})
    return render_template('lookup.html', data=result, gname=gall_name)