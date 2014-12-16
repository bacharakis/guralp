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


for gur in guralps:
  log_entry = log()

  print gur.ip
  if gur.prefix != "":
    print "Parsing "+gur.prefix
    buffer = StringIO()
    try:
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

      log_entry.guralp_prefix = gur.prefix



      print "parsing sensor"
      #get sensor status
      for child in root:
        if child.attrib.get("path") == "gcf-in-brp.PortA" :
          for children in child:
            if children.attrib.get("title") == "Timestamp of last packet received" :
              log_entry.sensor_last_packet_received = children.text
            if children.attrib.get("title") == "Time of last event" :
              log_entry.sensor_last_event = children.text
            if children.attrib.get("title") == "Number of blocks received in last 5 minutes" :
              log_entry.sensor_blocks_rec = children.text
            if children.attrib.get("title") == "Number of blocks output in last 5 minutes" :
              log_entry.sensor_blocks_out = children.text

      print "parsing GPS"
      #get GPS status
      for child in root:
        if child.attrib.get("title") == "NTP" :
          for children in child:
            if children.attrib.get("title") == "Clock locked" :
              log_entry.ntp_status = children.text
            if children.attrib.get("title") == "Estimated error" :
              log_entry.ntp_estimated_error = children.text

      print "parsing scream"
      #scream
      for child in root:
        if child.attrib.get("path") == "gcf-out-scream.default" :
          for children in child:
            if children.attrib.get("title") == "Number of clients connected" :
              log_entry.scream_clients_connected = children.text
            if children.attrib.get("title") == "Number of blocks sent in last 5 minutes" :
              log_entry.scream_blocks_5 = children.text

      print "parsing storage"
      #get storage status
      for child in root:
        if child.attrib.get("title") == "Storage" :
          for children in child:
            if children.attrib.get("title") == "State" :
              log_entry.storage_state = children.text
            if children.attrib.get("title") == "Last accessed" :
              log_entry.storage_last_accessed = children.text
            if children.attrib.get("title") == "Free space" :
              log_entry.storage_free_space = children.text
            if children.attrib.get("title") == "Storage size" :
              log_entry.storage_size = children.text

      print "parsing system"
      #get storage status
      for child in root:
        if child.attrib.get("title") == "Linux system" :
          for children in child:
            if children.attrib.get("title") == "System uptime" :
              log_entry.system_uptime = children.text
            if children.attrib.get("title") == "Load Average" :
              log_entry.system_load = children.text
            if children.attrib.get("title") == "Root filesystem percentage space free" :
              log_entry.root_free_filesystem = children.text
            if children.attrib.get("title") == "Software repository label" :
              log_entry.system_repo = children.text
            if children.attrib.get("title") == "Software build number" :
              log_entry.system_build_number = children.text
            if children.attrib.get("title") == "Build machine" :
              log_entry.system_build_machine = children.text

      print "parsing gcf"
      #get gcf
      for child in root:
        if child.attrib.get("path") == "gdi2gcf.default" :
          for children in child:
              if children.attrib.get("title") == "Number of samples in in last 5 minutes" :
                log_entry.gcf_last_samples_5_minutes = children.text
              if children.attrib.get("title") == "Number of blocks out in last 5 minutes" :
                log_entry.gcf_last_blocks_5_minutes = children.text
              if children.attrib.get("title") == "Total number of blocks out" :
                log_entry.gcf_blocks_out = children.text

      guralp.last_update = datetime.now()
      log_entry.timestamp = datetime.now()
      status.timestamp = datetime.now()
      #print guralp.last_update
      print "------------------"
      print "saving parsing"
      print "------------------"

      log_entry.save()




    except:
      print "Fetching failed"

print "=============== success ================"
