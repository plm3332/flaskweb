from flask import Flask, Blueprint, request, render_template
from db_model.mongodb import conn_board

board_search = Blueprint('boardsearch', __name__, static_folder='../static')

@board_search.route('/search', methods=['get'])
def search():
    search_name = request.args.get('search_name')
    mongo_conn = conn_board('boardtype')
    result = mongo_conn.find_one({'krname':search_name})
    if result:
        return render_template('search_result.html', search_result = result)
    else:
        return render_template('search_result.html', search_result = None)
        