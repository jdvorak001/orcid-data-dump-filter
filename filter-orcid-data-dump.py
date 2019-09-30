#!/usr/bin/env python3

import threading
import queue
import subprocess
import asyncio
import os
import sys
import xml.etree.ElementTree as ET

dump_file = "sample-data/ORCID-public-profiles-2018-API-2.0_xml-sample.tar.gz"
num_worker_threads = 10

if sys.platform == "win32":
    asyncio.set_event_loop_policy( asyncio.WindowsProactorEventLoopPolicy() )

ns = {
    "activities": "http://www.orcid.org/ns/activities",
    "address": "http://www.orcid.org/ns/address",
    "bulk": "http://www.orcid.org/ns/bulk",
    "common": "http://www.orcid.org/ns/common",
    "deprecated": "http://www.orcid.org/ns/deprecated",
    "education": "http://www.orcid.org/ns/education",
    "email": "http://www.orcid.org/ns/email",
    "employment": "http://www.orcid.org/ns/employment",
    "error": "http://www.orcid.org/ns/error",
    "external-identifier": "http://www.orcid.org/ns/external-identifier",
    "funding": "http://www.orcid.org/ns/funding",
    "history": "http://www.orcid.org/ns/history",
    "internal": "http://www.orcid.org/ns/internal",
    "keyword": "http://www.orcid.org/ns/keyword",
    "other-name": "http://www.orcid.org/ns/other-name",
    "peer-review": "http://www.orcid.org/ns/peer-review",
    "person": "http://www.orcid.org/ns/person",
    "personal-details": "http://www.orcid.org/ns/personal-details",
    "preferences": "http://www.orcid.org/ns/preferences",
    "record": "http://www.orcid.org/ns/record",
    "researcher-url": "http://www.orcid.org/ns/researcher-url",
    "work": "http://www.orcid.org/ns/work"
}

q = queue.Queue( maxsize=20 )

def worker():
    while True:
        filename = q.get()
        if filename is None: break
        tree = ET.parse( filename )
        root = tree.getroot()
        x1 = root.findall( 'person:person/address:addresses/address:address/address:country[ . = "CZ" ]', ns )
        x2 = root.findall( 'activities:activities-summary/activities:educations/education:education-summary/education:organization/common:address/common:country[ . = "CZ" ]', ns )
        x3 = root.findall( 'activities:activities-summary/activities:employments/employment:employment-summary/employment:organization/common:address/common:country[ . = "CZ" ]', ns )
        if x1 or x2 or x3:
            print( filename )
        else:
            os.remove( filename )
        q.task_done()

async def process( dump_file ):
    # Create the "tar xzvf ${file}" subprocess; redirect the standard output into a pipe
    untar_proc = await asyncio.create_subprocess_exec( "tar", "xzvf", dump_file, stderr=asyncio.subprocess.PIPE )
    while True:
        data = await untar_proc.stderr.readline()
        if not data: break
        ( operation, filename ) = data.decode( "ascii" ).rstrip().split()
        if filename[-1] != "/":
            q.put( filename )
    
    # Wait for the subprocess exit
    await untar_proc.wait()

threads = []
for i in range( num_worker_threads ):
    t = threading.Thread( target=worker )
    t.start()
    threads.append( t )

asyncio.run( process( dump_file ) )

# block until all tasks are done
q.join()

# stop workers
for i in range( num_worker_threads ):
    q.put( None )
for t in threads:
    t.join()
