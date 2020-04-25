import redis
import json
import random
import pandas as pd

HOST = '127.0.0.1'
PORT = 6379
r = redis.Redis(host=HOST, port=PORT)



def m_addHMSET(keyname: str, df: pd.DataFrame) -> list:
    """ Export multiple records from a dataframe to a redis hashset.

    Parameters
    -----
    `keyname` key on which geo records will be indexed on redis \n
    `df` dataframe containing geo records \n
    
    Returns
    -----
    A List describing the number of inserted elements for each record
    """
    # format data
    df = df.to_dict('records')
    random.seed(444)
    data = {f"%s:{random.getrandbits(32)}" % keyname : i for i in df}

    # insertion
    with r.pipeline() as pipe:
        try:
            for id, d in data.items():
                pipe.hmset(id, d)
        except redis.exceptions.ResponseError as resp_err:
            print(resp_err)
        finally:
            return pipe.execute()



def exportToGeo(keyname: str, lat: float, lon: float, place: str) -> bool:
    """ Export a single geo record to redis.

    Parameters
    -----
    `keyname` key on which geo records will be indexed on redis \n
    `lon` longitude \n
    `lat` atitude \n
    `place` location name

    Returns
    -----
    Number of inserted elements. Should be 1 if the element got successfuly inserted, 0 else.
    """
    ret = 0
    try:
        ret = r.geoadd(keyname, lon, lat, place)   # add geo record
    except redis.exceptions.ResponseError as resp_err:
        print(resp_err)
    finally:
        return ret 



def m_exportToGeo(df: pd.DataFrame, keyname: str, long_name: str, lat_name: str, loc_name: str) -> list:
    """ Export multiple geo records from a dataframe to redis.

    Parameters
    -----
    `df` dataframe containing geo records \n
    `keyname` key on which geo records will be indexed on redis \n
    `long_name` colname of longitude in df \n
    `lat_name` colname of latitude in df \n
    `loc_name` colname of location name in df

    Returns
    -----
    A List describing the number of inserted elements for each record
    """
    with r.pipeline() as pipe:
        try:
            for id, row in df.iterrows():
                pipe.geoadd(keyname, row[long_name], row[lat_name], row[loc_name])  # add geo row
        except KeyError as k_err:
            print(k_err)
        except redis.exceptions.ResponseError as resp_err:
            print(resp_err)
        finally:
            return pipe.execute()



def getGeoPos(keyname: str, place: str) -> tuple:
    """ Returns the geo-position of a given stored place.

    Parameters
    -----
    `keyname` key on which geo records will be indexed on redis \n
    `place` location name

    Returns
    -----
    Tuple (longitude, latitude)
    """
    ret = ()
    try:
        resp = r.geopos(keyname, place)[0]  # get pos
        ret = resp if resp else ()
    except redis.exceptions.ResponseError as resp_err:
        print(resp_err)
    finally:
        return ret
    


def getDist(keyname: str, loc1: str, loc2: str, unit: str) -> float:
    """ Get the distance between two places.
    Resulting value can be either in meter, km, miles or feet.

    Parameters
    -----
    `keyname` key on which geo records will be indexed on redis \n
    `loc1` first location \n
    `loc2` second location \n
    `unit`(m, km, mi, ft) result unit
    """
    return float(r.geodist(keyname, loc1, loc2, unit=unit))



def getInRadius(keyname: str, member: str, radius: int, unit: str):
    """
    """
    ret = []
    try:
        # get members in radius with their distance and coords
        result = r.georadiusbymember(keyname, member, radius, unit=unit, withdist=True, withcoord=True)
        if result :
            for res in result:
                tmp = {'member': res[0].decode("utf-8") , 'distance': res[1], "coords": res[2]}
                ret.append(tmp)
    except KeyError as k_err:
            print(k_err)
    except redis.exceptions.ResponseError as resp_err:
        print(resp_err)
    finally:
        return ret