from application import app, db
from application.auth.models import User
from application.tasks.models import Thread

def idSort(e):
    return e.id
    
def dateSort(e):
    return e.date_modified

def __removeDups__(duplicate): 
    palautus = [] 
    for i in duplicate: 
        if i not in palautus: 
            palautus.append(i) 
    return palautus 

def __listActives__():
    
    
    t = Thread.query.all()
    t.sort(key=dateSort,reverse=True)
    ids = []
    for x in t:
        ids.append(x.account_id)
    
    return __removeDups__(ids)

def actives():
    t = __listActives__()
    users = []
    for x in t:
        users.append(User.query.filter_by(id=x).first())
        
    return users
    
def inactives():
    u = User.query.all()
    ac = actives()
    inac = []
    for x in u:
        if x not in ac:
            inac.append(x)
    return inac
    

        
