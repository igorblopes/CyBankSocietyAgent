import os
from tinydb import TinyDB, Query
from entity import start_dispositives_entity
from datetime import datetime

db = TinyDB(os.getenv("DB_NAME"))
db_search = Query()


def insert(dispositives):
    find = db.search((db_search.type == dispositives.type) & (db_search.name == dispositives.name))
    
    if len(find) == 0:
        db.insert(dispositives.toSave())
    
 
def get_dispositives():
    find = db.search(db_search.type == db_search.type == 'start_dispositive')
        
    return find
    