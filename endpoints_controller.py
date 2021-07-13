from db import get_db
import random, string, json


def get_all_endpoints():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, endpoint, hits, createdTime FROM endpoints WHERE isActive = ?"
    cursor.execute(query, [True])
    return cursor.fetchall()

def get_by_id(id):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT endpoint FROM endpoints WHERE id = ? AND isActive = ?"
    cursor.execute(query, [id, True])
    if(cursor.fetchone() is not None):
        # query = "SELECT endpoint FROM endpoints WHERE endpoint_id = id"
        query = "SELECT headers, data, queryParameter FROM payloads WHERE endpoint_id = ?"
        cursor.execute(query, [id])
        return cursor.fetchall()
    else:
        return -1


def generate_endpoint():
    db = get_db()
    cursor = db.cursor()
    endpoint = generate_random_endpoint()
    query = "INSERT INTO endpoints(endpoint, hits, isActive, createdTime) VALUES (?, ?, ?, datetime('now', 'localtime'))"
    cursor.execute(query, [endpoint, 0, True])
    db.commit()
    return endpoint
    
def generate_random_endpoint():
    w = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    y = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    z = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    
    return '-'.join([w, z, y, z])

def store_succesfull_hit(id, request):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id FROM endpoints WHERE endpoint = ? AND isActive = ?"
    cursor.execute(query, [id, True])
    endpoint_id = cursor.fetchone()
    if(endpoint_id != None and len(endpoint_id) != 0):
        print(endpoint_id[0])
        query = "INSERT INTO payloads(endpoint_id, headers, data, queryParameter) VALUES (?, ?, ?, ?)"
        cursor.execute(query, [endpoint_id[0], str(request.headers), str(request.data), json.dumps(request.args)])
        query = "UPDATE endpoints SET hits = (SELECT COUNT(*) FROM payloads WHERE endpoint_id = ?) WHERE id = ?"
        cursor.execute(query, [endpoint_id[0], endpoint_id[0]])
        db.commit()
        return True
    else:
        return False
    
def end_api(id):
    db = get_db()
    cursor = db.cursor()
    query = "UPDATE endpoints SET isActive = ? WHERE id = ?"
    cursor.execute(query, [False, id])
    db.commit()
    return True
