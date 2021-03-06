import os
import csv
import xmlrpclib
import time
#import paramiko
import re
import ftplib
import oerphelper
import logging
import array
import string
import sys
from datetime import datetime, timedelta, date
from random import randint


# FILE PATHS

# OERP Constants
USERNAME = 'fedexapi'
PWD = 'fedexapi'
DBNAME = 'ao_1213'
ERP_WWW = 'http://develerp.alephobjects.com:8069'


def connect_oerp():
    '''
    Function that will make a connection to OpenERP using XML-RPC.
    @return1: socket that is connected to OpenERP
    @return2: An id that shows that you have been validated
    '''	
    #sock_common = xmlrpclib.ServerProxy('/xmlrpc/common' % ERP_WWW)
    #sock_common = xmlrpclib.ServerProxy(ERP_WWW+ '/xmlrpc/common')
    #uid = sock_common.login(DBNAME, USERNAME, PWD)
    sock = xmlrpclib.ServerProxy(ERP_WWW +'/xmlrpc/object') 
    sock_common = xmlrpclib.ServerProxy(ERP_WWW + '/xmlrpc/common')
    uid = sock_common.login(DBNAME, USERNAME, PWD)

    print "INFO: ***** SUCCESS - SERVER HAS AUTHENTICATED A LOGIN *****"
    
    return sock, uid
def search_outgoing(sock, uid, do_names):

    ids = sock.execute(DBNAME, uid, PWD, 'stock.picking.out', 'search', do_names)
    
    try:
        os_ids = ids
    except Exception:
        "There are no outgoing shipments to process"
        pass
    return os_ids

def fedex_put_tracking_nums(sock, uid, ids, tracking_nums):

    result = sock.execute(DBNAME, uid, PWD, 'delivery.tracking.numbers', 'add_tracking_num', tracking_nums)
    try:
        os_ids = ids
    except Exception:
        "There are no outgoing shipments to process"
        pass
    return result
      


    #except Exception:
    #    "cannot update these records"
    #    pass
    return tracking_id
    
def main():
    #Connect to OpenERP
    sock, uid = connect_oerp()
    do_names = [('name', '=', 'OUT/6919')] 
    do_ids = search_outgoing(sock, uid, do_names)

    print do_ids
    
    # test input
    tracking_nums={'delivery_id':do_ids[0], 'tracking_no':'asdfasw3423', 'tracking_desc':'asdfasdgasdg253267235'}

    print tracking_nums
    
    msg = fedex_put_tracking_nums(sock, uid, do_ids, tracking_nums)
    print msg
    
if __name__ == '__main__':
    print 'Starting'
    main()
    print 'Sleeping'
