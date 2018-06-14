from config import Config
import pymysql
import json


class PDBC:

    @staticmethod
    def open_db():
        return pymysql.connect(Config.db_address,
                               Config.db_user,
                               Config.db_passwd,
                               Config.db_database,
                               charset='utf8')

    @staticmethod
    def open_cs(db):
        return db.cursor

    @staticmethod
    def get_class(db):
        data = []

        cursor = db.cursor()
        sql = "SELECT distinct species FROM catalog;"
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            pet = {'index': 0, 'species': item[0], 'variety':[]}
            sql = "SELECT distinct cid,variety FROM catalog WHERE species = '{}';".format(item[0])
            cursor.execute(sql)
            results = cursor.fetchall()
            for it in results:
                pet['variety'].append({
                    'cid': it[0],
                    'name': it[1]})
            data.append(pet)

        return data

    @staticmethod
    def get_list(db, cid):
        data = []

        cursor = db.cursor()
        sql = "SELECT pid,title,price,photo FROM pets WHERE cid = {};".format(cid)
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            pet = {
                'img_link': item[3],
                'title': item[1],
                'price': item[2],
                'pid': item[0]
            }
            data.append(pet)
        return data

    @staticmethod
    def get_animal(db, pid):
        data = []

        cursor = db.cursor()
        sql = "SELECT title,price,photo,intro,num FROM pets WHERE pid = {};".format(pid)
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            pet = {
                'img_link': item[2],
                'title': item[0],
                'intro': item[3],
                'price': item[1],
                'num': item[4]
            }
            data.append(pet)
        return data

    @staticmethod
    def get_order(db, uid):
        data = []

        cursor = db.cursor()
        sql = "SELECT distinct lid FROM user_list WHERE uid = {};".format(uid)
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            it = {
                'lid': item[0],
                'time': '',
                'list': []
            }
            data.append(it)

        for itema in data:
            sql = "SELECT title,price,num,time FROM user_list WHERE lid = {}".format(itema['lid'])
            cursor.execute(sql)
            results = cursor.fetchall()

            for itemb in results:
                it = {
                    'title': itemb[0],
                    'price': itemb[1],
                    'num': itemb[2]
                }
                itema['time'] = itemb[3]
                itema['list'].append(it)
        return data

    @staticmethod
    def get_user(db, uid):
        data = {
            'user_name': '',
            'user_phone': '',
            'user_area': [],
            'user_address': ''
        }
        if int(uid) < 1:
            return data
        cursor = db.cursor()
        sql = "SELECT name,phone,province,area,city,address FROM user_info WHERE uid = {};".format(uid)
        cursor.execute(sql)
        results = cursor.fetchone()
        data = {
            'user_name': results[0],
            'user_phone': results[1],
            'user_area': [results[2], results[3], results[4]],
            'user_address': results[5]
        }
        return data

    @staticmethod
    def pick_pet(db, uid, data):
        result = "error"
        cursor = db.cursor()
        sql = "START TRANSACTION;"
        cursor.execute(sql)

        sql = "SELECT max(lid) as max FROM user_list;"
        cursor.execute(sql)
        lid = cursor.fetchone()
        if lid[0] is None:
            lid = 1
        else:
            lid = int(lid[0])+1

        for item in data:
            line = json.loads(item)
            sql = "INSERT INTO user_list (uid,lid,title,price,num) VALUES ({},{},'{}',{},{});"\
                .format(uid, lid, line['title'], line['price'], line['num'])
            cursor.execute(sql)

        sql = "COMMIT;"
        cursor.execute(sql)
        result = 'success'
        return result

    @staticmethod
    def login(db, username, password):
        cursor = db.cursor()
        sql = "SELECT uid,password FROM user WHERE username = '{}';".format(username)
        cursor.execute(sql)
        results = cursor.fetchall()

        for item in results:
            if password == item[1]:
                return item[0]
        return -1

    @staticmethod
    def sure_user(db, uid, data):
        cursor = db.cursor()
        sql = "UPDATE user_info SET name='{}'," \
              "phone='{}',province='{}',area='{}'," \
              "city='{}',address='{}' WHERE uid = '{}';"\
            .format(data[0], data[1], data[2], data[3], data[4], data[5], uid)
        cursor.execute(sql)
        return {'status': 'success'}

