import redis
import random
import pandas as pd



def m_addHMSET(r: redis.Redis, keyname: str, indexField: str, records: list) -> list:
    """ Export multiple records from a dataframe to a redis hashset.

    Parameters
    -----
    `r` redis server connection \n
    `keyname` key on which geo records will be indexed on redis \n
    `records` list containing geo records \n
    
    Returns
    -----
    A List describing the number of inserted elements for each record
    """
    # format data
    random.seed(444)
    data = {f"%s:{random.getrandbits(32)}" % keyname : i for i in records}

    # insertion
    with r.pipeline() as pipe:
        try:
            for id, d in data.items():
                pipe.hmset(id, d)               # set hash
                pipe.sadd(d[indexField], id)    # index it by field value
        except redis.exceptions.ResponseError as resp_err:
            print(resp_err)
        finally:
            return pipe.execute()



def addHMSET(r: redis.Redis, keyname: str, mapping: dict) -> int:
    """
    """
    ret = 0
    try:
        ret = r.hmset(keyname, mapping)
    except redis.exceptions.ResponseError as resp_err:
        print(resp_err)
    finally:
        return ret



def addSET(r: redis.Redis, keyname: str, members: list) -> bool:
    """
    """
    ret = 0
    try:
        ret = r.sadd(keyname, *members)
    except redis.exceptions.ResponseError as resp_err:
        print(resp_err)
    finally:
        return ret



def exportToGeo(r: redis.Redis, keyname: str, lat: float, lon: float, place: str) -> int:
    """ Export a single geo record to redis.

    Parameters
    -----
    `r` redis server connection \n
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



def m_exportToGeo(r: redis.Redis, df: pd.DataFrame, keyname: str, long_name: str, lat_name: str, loc_name: str) -> list:
    """ Export multiple geo records from a dataframe to redis.

    Parameters
    -----
    `r` redis server connection \n
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



def getGeoPos(r: redis.Redis, keyname: str, place: str) -> tuple:
    """ Returns the geo-position of a given stored place.

    Parameters
    -----
    `r` redis server connection \n
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
    


def getDist(r: redis.Redis, keyname: str, loc1: str, loc2: str, unit: str) -> float:
    """ Get the distance between two places.
    Resulting value can be either in meter, km, miles or feet.

    Parameters
    -----
    `r` redis server connection \n
    `keyname` key on which geo records will be indexed on redis \n
    `loc1` first location \n
    `loc2` second location \n
    `unit`(m, km, mi, ft) result unit
    """
    return float(r.geodist(keyname, loc1, loc2, unit=unit))



def getInRadiusByMember(r: redis.Redis, keyname: str, member: str, radius: int, unit: str, withdist=False, withcoord=False):
    """ Get the distance between two places.
    Resulting value can be either in meter, km, miles or feet.

    Parameters
    -----
    `r` redis server connection \n
    `keyname` key on which geo records will be indexed on redis \n
    `member` name of place indexed in the same key \n
    `radius` radius defining limits of the area \n
    `unit`(m, km, mi, ft) result unit
    """
    ret = []
    try:
        ret = r.georadiusbymember(keyname, member, radius, unit=unit, withdist=withdist, withcoord=withcoord)
    except KeyError as k_err:
            print(k_err)
    except redis.exceptions.ResponseError as resp_err:
        print(resp_err)
    finally:
        return ret
