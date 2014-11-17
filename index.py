import pycurl
from datetime import datetime
from io import BytesIO
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guralps.settings")

# your imports, e.g. Django models
from guralp.models import guralp, NTP,sensor, gcf, scream, Storage

guralps = guralp.objects.all()
guralp = guralp()

gps = NTP()
sensor = sensor()
gcf = gcf()
scream = scream()
storage = Storage()

for gur in guralps:
  print gur.ip
  if gur.prefix != "":
    print "Parsing "+gur.prefix
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+gur.ip+'/cgi-bin/xmlstatus.cgi?download_xml=true')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    import xml.etree.ElementTree as ET
    root = ET.fromstring(body)

    gps.guralp_prefix = gur.prefix
    sensor.guralp_prefix = gur.prefix
    scream.guralp_prefix = gur.prefix
    gcf.guralp_prefix = gur.prefix
    storage.guralp_prefix = gur.prefix



    print "parsing sensor"
    #get sensor status
    for child in root:
      if child.attrib.get("path") == "gcf-in-brp.PortA" :
        for children in child:
          if children.attrib.get("title") == "Total number of blocks received" :
            sensor.blocks_received = children.text
          if children.attrib.get("title") == "Number of bytes received in last 5 minutes" :
            sensor.last_5_minutes = children.text
          if children.attrib.get("title") == "Time of last event" :
            sensor.last_event = children.text

    print "parsing GPS"
    #get GPS status
    for child in root:
      if child.attrib.get("title") == "NTP" :
        for children in child:
          if children.attrib.get("title") == "Clock locked" :
            gps.clock_locked = children.text
          if children.attrib.get("title") == "Estimated error" :
            gps.estimated_error = children.text

    print "parsing scream"
    #scream
    for child in root:
      if child.attrib.get("path") == "gcf-out-scream.default" :
        for children in child:
          if children.attrib.get("title") == "Total number of blocks sent" :
            scream.blocks_received = children.text
          if children.attrib.get("title") == "Number of blocks sent in last 5 minutes" :
            scream.last_5_minutes = children.text

    print "parsing storage"
    #get storage status
    for child in root:
      if child.attrib.get("title") == "Storage" :
        for children in child:
          if children.attrib.get("title") == "State" :
            storage.state = children.text
            print children.text
          if children.attrib.get("title") == "Last accessed" :
            storage.last_accessed = children.text
          if children.attrib.get("title") == "Free space" :
            storage.free_space = children.text
          if children.attrib.get("title") == "Storage size" :
            storage.size = children.text

    print "parsing gcf"
    #get gcf
    for child in root:
      if child.attrib.get("path") == "gdi2gcf.default" :
        for children in child:
            if children.attrib.get("title") == "Total number of samples in" :
              gcf.blocks_received = children.text
            if children.attrib.get("title") == "Number of samples in in last 5 minutes" :
              gcf.last_5_minutes = children.text

sensor.blocks_received_status = 0
scream.blocks_received_status = 0
gcf.blocks_received_status = 0
guralp.last_update = datetime.now()
sensor.last_update = datetime.now()
scream.last_update = datetime.now()
gcf.last_event = datetime.now()
sensor.last_event = datetime.now()
scream.last_event = datetime.now()
gcf.last_update = datetime.now()
gps.last_update = datetime.now()
storage.last_update = datetime.now()

print "saving parsing"
guralp.save()
sensor.save()
scream.save()
gcf.save()
gps.save()
storage.save()

print "=============== success ================"


html_file = open("index.html", "w")
html_file.write(body)
html_file.close()
