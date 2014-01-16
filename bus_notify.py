#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2, urllib
import json
import datetime, time
import logging
import os, errno

import xxutils

APPDIR = "/home/chenyang/opt/bus" #Linux
#APPDIR = "E:/source" #Windows


# bus info
CITY = u"北京"

# test station
STATION = "31"

# test line
linename = u"运通113(来广营北-吴庄)"

def main():
    encode_linename = urllib2.quote(linename.encode("utf8"))
    encode_city = urllib2.quote(CITY.encode("utf8"))
    url = "http://bjgj.aibang.com:8899/bjgj.php?city=" + encode_city + "&linename=" + encode_linename + "&stationNo=" + STATION + "&datatype=json&type=0"
    logger.debug("url : " + url)

    request = urllib2.Request(url, headers={"Accept" : "text/html"})
    contents = urllib2.urlopen(request).read()
    data = json.loads(contents)
    
    # Only getting data will 200, other condition will 502.
    if data["root"]["status"] == "200" :
        logger.debug("data is got.")
        
        # iteration every bus in this line.
        for line_id in range(1, int(data["root"]["busnum"])):
            busobj = data["root"]["dataList"]["bus"][line_id]
            # ignore the bus pass by.
            if busobj["stationDistince"] == "-1":
                continue
            logger.debug("[%s] : Next station is : %s", busobj["busid"], busobj["nextStation"])
            logger.debug("[%s] : Distance is : %s", busobj["busid"], busobj["stationDistince"])
            
            if int(busobj["stationDistince"]) < 3000:
                xxutils.notify()
    
    elif data["root"]["status"] == "502":
        logger.debug("[%s] : Message : %s", linename, data["root"]["message"])
        logger.debug("[%s] : Reason : Night or line not exist", linename)
    else:
        logger.debug("Unkown error!")

if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig(APPDIR + '/bus/conf/bus_notify.conf')

    logger = logging.getLogger(__name__)
    logger.debug('start...')

    main()