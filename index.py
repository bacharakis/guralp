import pycurl
from datetime import datetime
from StringIO import StringIO
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guralps.settings")

# your imports, e.g. Django models
from guralp.models import guralp, log

guralps = guralp.objects.all()
guralp = guralp()
log = log()


for gur in guralps:
  print gur.ip
  if gur.prefix != "":
    print "Parsing "+gur.prefix
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+gur.ip.encode("ascii")+'/cgi-bin/xmlstatus.cgi?download_xml=true')
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    import xml.etree.ElementTree as ET
    root = ET.fromstring(body)

    log.guralp_prefix = gur.prefix



    print "parsing sensor"
    #get sensor status
    for child in root:
      if child.attrib.get("path") == "gcf-in-brp.PortA" :
        for children in child:
          if children.attrib.get("title") == "Timestamp of last packet received" :
            log.sensor_last_packet_received = children.text
          if children.attrib.get("title") == "Time of last event" :
            log.sensor_last_event = children.text
          if children.attrib.get("title") == "Number of blocks received in last 5 minutes" :
            log.sensor_blocks_rec = children.text
          if children.attrib.get("title") == "Number of blocks output in last 5 minutes" :
            log.sensor_blocks_out = children.text

    print "parsing GPS"
    #get GPS status
    for child in root:
      if child.attrib.get("title") == "NTP" :
        for children in child:
          if children.attrib.get("title") == "Clock locked" :
            log.ntp_status = children.text
          if children.attrib.get("title") == "Estimated error" :
            log.ntp_estimated_error = children.text

    print "parsing scream"
    #scream
    for child in root:
      if child.attrib.get("path") == "gcf-out-scream.default" :
        for children in child:
          if children.attrib.get("title") == "Number of clients connected" :
            log.scream_clients_connected = children.text
          if children.attrib.get("title") == "Number of blocks sent in last 5 minutes" :
            log.scream_blocks_5 = children.text

    print "parsing storage"
    #get storage status
    for child in root:
      if child.attrib.get("title") == "Storage" :
        for children in child:
          if children.attrib.get("title") == "State" :
            log.storage_state = children.text
          if children.attrib.get("title") == "Last accessed" :
            log.storage_last_accessed = children.text
          if children.attrib.get("title") == "Free space" :
            log.storage_free_space = children.text
          if children.attrib.get("title") == "Storage size" :
            log.storage_size = children.text

    print "parsing system"
    #get storage status
    for child in root:
      if child.attrib.get("title") == "Linux system" :
        for children in child:
          if children.attrib.get("title") == "System uptime" :
            log.system_uptime = children.text
          if children.attrib.get("title") == "Load Average" :
            log.system_load = children.text
          if children.attrib.get("title") == "Root filesystem percentage space free" :
            log.root_free_filesystem = children.text
          if children.attrib.get("title") == "Software repository label" :
            log.system_repo = children.text
          if children.attrib.get("title") == "Software build number" :
            log.system_build_number = children.text
          if children.attrib.get("title") == "Build machine" :
            log.system_build_machine = children.text

    print "parsing gcf"
    #get gcf
    for child in root:
      if child.attrib.get("path") == "gdi2gcf.default" :
        for children in child:
            if children.attrib.get("title") == "Number of samples in in last 5 minutes" :
              log.gcf_last_samples_5_minutes = children.text
            if children.attrib.get("title") == "Number of blocks out in last 5 minutes" :
              log.gcf_last_blocks_5_minutes = children.text
            if children.attrib.get("title") == "Total number of blocks out" :
              log.gcf_blocks_out = children.text

guralp.last_update = datetime.now()
log.timestamp = datetime.now()
#print guralp.last_update
print "saving parsing"
log.save()
guralp.save()


print "=============== success ================"


html_file = open("index.html", "w")
html_file.write(body)
html_file.close()
