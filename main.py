import redis
import json
import random
import pandas as pd

import redis_utils as rutils





if __name__ == "__main__":
    
    key = 'France'
    req = {
        'member': 'Amiens',
        'radius': 35,
        'unit': 'km',
    }
    str_req = "Cities around {} {} from {} : ".format(req['radius'], req['unit'], req['member'])

    # IMPORTING DATA
    cities = pd.read_csv('data/cities.csv', sep=',', encoding='utf-8')
    jobs   = pd.read_csv('data/jobs.csv', sep=',', encoding='utf-8')
    cit_h  = sorted(list(cities.columns))

    # REDIS OPERATIONS
    res_jobs  = rutils.m_addHMSET('jobs', jobs)
    res_exptr = rutils.m_exportToGeo(cities, key, *cit_h)  # exporting geo records to redis
    res_rad   = rutils.getInRadius(key, **req)               # get cities within a radius

    # PRINTS
    print("Insertion of jobs : ", res_jobs)
    print("Insertion of geo records : ", res_exptr , '\n')    
    print(str_req, json.dumps(res_rad, indent=4))
    
    