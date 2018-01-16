#coding=utf-8
import pymongo
from bson.objectid import ObjectId
import time
from mongodb_config import HOST,PORT

class MongoAPI(object):
    def __init__(self):
        # print 'init mongo args...'
        # self.host = '127.0.0.1'
        self.host = HOST
        self.port = PORT
        self.db_name = 'MiTao'

    def connnect_db(self):
        client = pymongo.MongoClient(self.host, self.port)
        return client

    def use_db(self):
        client = self.connnect_db()
        mydb = client[self.db_name] # new a database
        return mydb

    def get_db(self):
            db = self.use_db()
            return db
        
    def use_table(self,db,table_name):
            return db[table_name]

    def get_table(self,table_name):
        db = self.get_db()
        table = self.use_table(db,table_name)
        return table


class orderAPI(MongoAPI):
    def __init__(self):
        super(orderAPI,self).__init__()
        self.table_name = 'myorder'
        self.table = self.get_table(self.table_name)


    def add_order_info(self,info):
        self.table.insert(info)


    def get_all_order_info(self):
        data = self.table.find().sort([('order_id',pymongo.DESCENDING)])
        if data:
            return list(data)
        else:
            return []
    def is_exist(self,title):
        data = list(self.table.find({'title':title}))
        if data:
            print data[0].bought_count
            return data[0].bought_count
        else:
            return False
    def update_order_info(self,title,num):
        num += 1
        self.table.update({'title':title},{'$set':{'bought_count':num}},True,False)

    def remove_order_info(self,order_id):
        self.table.remove({'order_id':order_id})

    def remove_all_order(self):
        self.table.drop()



class HotCommodityAPI(MongoAPI):
    def __init__(self):
        super(HotCommodityAPI,self).__init__()
        self.table_name = 'hotgoods'
        self.table = self.get_table(self.table_name)


    def add_commodity_info(self,info):
        print ('insert',info)
        self.table.save(info)


    def get_all_commodity_info(self):
        data = self.table.find().sort([('commodity_id',pymongo.DESCENDING)])
        if data:
            return list(data)
        else:
            return []
    def is_exist(self,title):
        data = list(self.table.find({'title':title}))
        if data:
            print data[0].bought_count
            return data[0].bought_count
        else:
            return False
    def update_commodity_info(self,title,num):
        num += 1
        self.table.update({'title':title},{'$set':{'bought_count':num}},True,False)

    def remove_commodity_info(self,kind):
        print('delete----------------------------------------')
        self.table.remove({'type':kind})

    def remove_all_commodity(self):
        print('delete----------------------------------------')
        self.table.drop()


class CommonCommodityAPI(MongoAPI):
    def __init__(self):
        super(CommonCommodityAPI,self).__init__()
        self.table_name = 'commongoods'
        self.table = self.get_table(self.table_name)


    def add_commodity_info(self,info):
        print ('insert',info)
        self.table.save(info)


    def get_all_commodity_info(self):
        data = self.table.find().sort([('commodity_id',pymongo.DESCENDING)])
        if data:
            return list(data)
        else:
            return []
    def is_exist(self,title):
        data = list(self.table.find({'title':title}))
        if data:
            print data[0].bought_count
            return data[0].bought_count
        else:
            return False
    def update_commodity_info(self,title,num):
        num += 1
        self.table.update({'title':title},{'$set':{'bought_count':num}},True,False)

    def remove_commodity_info(self,kind):
        print('delete----------------------------------------')
        self.table.remove({'type':kind})

    def remove_all_commodity(self):
        print('delete----------------------------------------')
        self.table.drop()