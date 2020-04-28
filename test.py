import redis
import json
import random
import pandas as pd

import pubsub.utils.redis_utils as rutils

HOST = '127.0.0.1'
PORT = 6379
r = redis.Redis(host=HOST, port=PORT)



if __name__ == "__main__":
    
    key = 'France'
    req = {
        'member': 'Amiens',
        'radius': 35,
        'unit': 'km',
        'withdist': True,
        'withcoord': True
    }
    str_req = "Cities around {} {} from {} : ".format(req['radius'], req['unit'], req['member'])

    # IMPORTING DATA
    cities = pd.read_csv('data/cities.csv', sep=',', encoding='utf-8')
    jobs   = pd.read_csv('data/jobs.csv', sep=',', encoding='utf-8')
    cit_h  = sorted(list(cities.columns))

    # REDIS OPERATIONS
    res_jobs  = rutils.m_addHMSET(r, 'jobs', 'ville', jobs.to_dict('records'))
    res_exptr = rutils.m_exportToGeo(r, cities, key, *cit_h)    # exporting geo records to redis
    res_rad   = rutils.getInRadiusByMember(r, key, **req)       # get cities within a radius

    # PRINTS
    print("Insertion of jobs : ", res_jobs)
    print("Insertion of geo records : ", res_exptr , '\n')    
    print(str_req, '\n', res_rad)
    
    