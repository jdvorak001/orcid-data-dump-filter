#!/usr/bin/env python3

import re
import threading
import queue
import subprocess
import os
import sys
from lxml import etree
import time

#dump_file = "/data/ORCID/ORCID-public-profiles-2018-API-2.0_xml.tar.gz"
dump_file = "data/sample/ORCID-public-profiles-2018-API-2.0_xml-sample.tar.gz"
num_worker_threads = 3
queue_length = 200

# expects a match() function to be defined: 
#   given a xml root element, it returns True when the profile matches your condition
import my_orcid_filter

q = queue.Queue( maxsize=queue_length )
closing = False

def worker():
    c = my_orcid_filter.OrcidCondition()
    while True:
        if closing or q.qsize() > num_worker_threads:
            filename = q.get()
            if filename is None: break
            tree = etree.parse( filename )
            xml_root = tree.getroot()
            m = c.match( xml_root )
            if m:
                print( filename )
            else:
                os.remove( filename )
            q.task_done()
        else:
            time.sleep( 0.01 )

re1 = re.compile( "^x\\s+" )
    
threads = []
for i in range( num_worker_threads ):
    t = threading.Thread( target=worker )
    t.start()
    threads.append( t )

# Create the "tar xzvf ${file}" subprocess; redirect the standard output into a pipe
untar_proc = subprocess.Popen( [ "tar", "xzvf", dump_file ], bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
untar_list_stream = untar_proc.stderr if sys.platform == "darwin" else untar_proc.stdout
while True:
    data = untar_list_stream.readline()
    if not data: break
    filename = data.decode( "ascii" ).rstrip()
    filename = re1.sub( "", filename )  # for compatibility with macOS tar
    if filename[-1] != "/":
        q.put( filename )

# block until all tasks are done
closing = True
q.join()

# stop workers
for i in range( num_worker_threads ):
    q.put( None )
for t in threads:
    t.join()

untar_proc.wait()
