import redis
import threading
import pandas as pd

import utils.redis_utils as rutils

HOST = '127.0.0.1'
PORT = 6379
r = redis.Redis(host=HOST, port=PORT)



def getSubCities(keyname: str, location: str, radius: int, unit: str) -> list:
    """
    """
    return [member.decode('utf-8') for member in rutils.getInRadiusByMember(r, keyname, location, radius, unit)]



class StreamListener(threading.Thread):
    """
    """

    def __init__(self, keyname: str, location: str, radius: int, unit: str) -> None:
        # ATTRIBUTES
        threading.Thread.__init__(self)     # calling parent init
        self.redis = r
        self.subscr_cities = getSubCities(keyname, location, radius, unit)
        # PUBSUB
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.subscr_cities)   # subscribe to cities within the given radius


    def showAd(self, item: dict) -> None:
        print(item['channel'], ": ", item['data'])

    
    def run(self):
        for item in self.pubsub.listen():
            self.showAd(item)



    
if __name__ == "__main__":

    key = 'France'

    # IMPORTING SOME GEO DATA
    cities = pd.read_csv('data/cities.csv', sep=',', encoding='utf-8')
    cit_h  = sorted(list(cities.columns))
    print("Insertion of geo records : ", rutils.m_exportToGeo(r, cities, key, *cit_h) , '\n')
    
    #============================================
    #   RECEIVER
    #============================================
    req = {
    'keyname': key,
    'location': 'Amiens',
    'radius': 35,
    'unit': 'km'
    }
    receiver = StreamListener(**req)
    receiver.start()

    #============================================
    #   SENDER
    #============================================
    jobs = pd.read_csv('data/jobs.csv', sep=',', encoding='utf-8')
    for id, row in jobs.iterrows():
        r.publish(row['ville'], row['offre'])