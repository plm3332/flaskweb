import pymongo

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_CONN = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)

#collection - boardall, boardtype
def conn_board(collection):
    try:
        #MONGO_CONN.admin.command('ismaster')
        db = MONGO_CONN.get_database('board')
        db_c = db.get_collection(collection)
    except:
        #MONGO_CONN = pymongo.MongoClient('mongodb://%s' % MONGO_HOST)
        db = MONGO_CONN.get_database('board')
        db_c = db.get_collection(collection)

    return db_c