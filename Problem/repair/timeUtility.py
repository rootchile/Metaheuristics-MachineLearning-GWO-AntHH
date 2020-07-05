__author__ = 'INVESTIGACION'
import datetime, time

def obtieneTime():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
    return st

def minusSet(x,y):
    x_y = list(set(x) - set(y))
    return x_y