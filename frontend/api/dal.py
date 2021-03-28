import threading


from db.mongo_client import MyMongoClient


__LOCK = threading.Lock()
__MONGO_CLIENT = None


def get_mongo_client_dal():
    global __MONGO_CLIENT, __LOCK
    if not __MONGO_CLIENT:
        try:
            __LOCK.acquire()
            if not __MONGO_CLIENT:
                __MONGO_CLIENT = MyMongoClient()
        finally:
            __LOCK.release()
    return __MONGO_CLIENT
