#!/usr/bin/python

import pycurl
from datetime import datetime
from StringIO import StringIO
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guralps.settings")
import django
django.setup()
from guralp.models import guralp, log, history, logging


#guralps_out = guralp.objects.filter(status="Unreachable").order_by('prefix')
#for gur in guralps_out:
#	print gur.prefix+" "+gur.ip+" "+str(gur.url)
#
#sys.exit(0)

guralps = guralp.objects.exclude(status="Unreachable").order_by('station_code')

guralp = guralp()

logging_entry = logging()
logging_entry.timestamp = datetime.now().replace(microsecond=0)

for gur in guralps:
  log_entry = log()
  history_entry = history()

  print "=============="
  print "Beginning Parsing of:"+gur.station_code+" "+gur.ip+" "+str(gur.url)
  print "=============="

  if gur.station_code != "":
    try:
      print "Forming URL..."
      c = pycurl.Curl()
      if gur.url == "https":
         c.setopt(pycurl.URL, 'https://'+gur.ip.encode("ascii")+'/cgi-bin/xmlstatus.cgi?download_xml=true')
         c.setopt(pycurl.SSL_VERIFYPEER, 0)
         c.setopt(pycurl.SSL_VERIFYHOST, 0)
      else:
         c.setopt(pycurl.URL, 'http://'+gur.ip.encode("ascii")+'/cgi-bin/xmlstatus.cgi?download_xml=true')

      print c.getinfo(pycurl.EFFECTIVE_URL)

      print "Getting XML..."
      buffer = StringIO()
      c.setopt(pycurl.WRITEFUNCTION, buffer.write)
      c.perform()
      c.close()

      print "Reading XML..."
      body = buffer.getvalue()
      # Body is a byte string.
      # We have to know the encoding in order to print it to a text file
      # such as standard output.
      import xml.etree.ElementTree as ET
      root = ET.fromstring(body)

      log_entry.station_code = gur.station_code
      history_entry.staton_code = gur.station_code


      print "parsing sensor"
      #get sensor status
      for child in root:
        if child.attrib.get("path") == "gcf-in-brp.PortA" :
          for children in child:
            if children.attrib.get("title") == "Timestamp of last packet received" :
              log_entry.sensor_last_packet_received = children.text
              history_entry.sensor_last_packet_received = children.text
            if children.attrib.get("title") == "Time of last event" :
              log_entry.sensor_last_event = children.text
              history_entry.sensor_last_event = children.text
            if children.attrib.get("title") == "Number of blocks received in last 5 minutes" :
              log_entry.sensor_blocks_rec = children.text
              history_entry.sensor_blocks_rec = children.text
            if children.attrib.get("title") == "Number of blocks output in last 5 minutes" :
              log_entry.sensor_blocks_out = children.text
              history_entry.sensor_blocks_out = children.text

      print "parsing GPS"
      #get GPS status
      for child in root:
        if child.attrib.get("title") == "NTP" :
          for children in child:
            if children.attrib.get("title") == "Clock locked" :
              log_entry.ntp_status = children.text
              history_entry.ntp_status = children.text
            if children.attrib.get("title") == "Estimated error" :
              log_entry.ntp_estimated_error = children.text
              history_entry.ntp_estimated_error = children.text

      print "parsing scream"
      #scream
      for child in root:
        if child.attrib.get("path") == "gcf-out-scream.default" :
          for children in child:
            if children.attrib.get("title") == "Number of clients connected" :
              log_entry.scream_clients_connected = children.text
              history_entry.scream_clients_connected = children.text
            if children.attrib.get("title") == "Number of blocks sent in last 5 minutes" :
              log_entry.scream_blocks_5 = children.text
              history_entry.scream_blocks_5 = children.text

      print "parsing storage"
      #get storage status
      for child in root:
        if child.attrib.get("title") == "Storage" :
          for children in child:
            if children.attrib.get("title") == "State" :
              log_entry.storage_state = children.text
              history_entry.storage_state = children.text
            if children.attrib.get("title") == "Last accessed" :
              log_entry.storage_last_accessed = children.text
              history_entry.storage_last_accessed = children.text
            if children.attrib.get("title") == "Free space" :
              log_entry.storage_free_space = children.text
              history_entry.storage_free_space = children.text
            if children.attrib.get("title") == "Storage size" :
              log_entry.storage_size = children.text
              history_entry.storage_size = children.text

      print "parsing system"
      #get storage status
      for child in root:
        if child.attrib.get("title") == "Linux system" :
          for children in child:
            if children.attrib.get("title") == "System uptime" :
              uptime = (float(children.text) / 3600 )/ 24
              uptime = "%.2f" % uptime
              log_entry.system_uptime = uptime
              history_entry.system_uptime = uptime
            if children.attrib.get("title") == "Load Average" :
              log_entry.system_load = children.text
              history_entry.system_load = children.text
            if children.attrib.get("title") == "Root filesystem percentage space free" :
              log_entry.root_free_filesystem = children.text
              history_entry.root_free_filesystem = children.text
            if children.attrib.get("title") == "Software repository label" :
              log_entry.system_repo = children.text
              history_entry.system_repo = children.text
            if children.attrib.get("title") == "Software build number" :
              log_entry.system_build_number = children.text
              history_entry.system_build_number = children.text
            if children.attrib.get("title") == "Build machine" :
              log_entry.system_build_machine = children.text
              history_entry.system_build_machine = children.text

      print "parsing gcf"
      #get gcf
      for child in root:
        if child.attrib.get("path") == "gdi2gcf.default" :
          for children in child:
              if children.attrib.get("title") == "Number of samples in in last 5 minutes" :
                log_entry.gcf_last_samples_5_minutes = children.text
                history_entry.gcf_last_samples_5_minutes = children.text
              if children.attrib.get("title") == "Number of blocks out in last 5 minutes" :
                log_entry.gcf_last_blocks_5_minutes = children.text
                history_entry.gcf_last_blocks_5_minutes = children.text
              if children.attrib.get("title") == "Total number of blocks out" :
                log_entry.gcf_blocks_out = children.text
                history_entry.gcf_blocks_out = children.text
      guralp.last_update = datetime.now().replace(microsecond=0)
      log_entry.timestamp = datetime.now().replace(microsecond=0)
      history_entry.timestamp = datetime.now().replace(microsecond=0)
      #print guralp.last_update


      logging_entry.succeed=gur.station_code+","+str(logging_entry.succeed)
      logging_entry.save()

      print "- parsing saved for: "+gur.station_code

      try:
          same_entry = log.objects.filter(station_code=gur.station_code)
          same_entry.delete()
          log_entry.save()
      except:
          log_entry.save()

      try:
          same_status = history.objects.filter(station_code=gur.station_code)
          latest_status = same_status.latest('timestamp')


          if latest_status.sensor_blocks_out == status_entry.sensor_blocks_out:
              print "foo1"
              if latest_status.sensor_blocks_rec == status_entry.sensor_blocks_rec:
                  print "foo2"
                  if latest_status.scream_clients_connected == status_entry.scream_clients_connected:
                      print "foo3"
                      if latest_status.scream_blocks_5 == status_entry.scream_blocks_5:
                          print "foo4"
                          if latest_status.gcf_last_blocks_5_minutes == status_entry.gcf_last_blocks_5_minutes:
                              print "foo5"
                              if latest_status.gcf_last_samples_5_minutes == status_entry.gcf_last_samples_5_minutes:
                                  print "foo6"
                                  if latest_status.ntp_status == status_entry.ntp_status:
                                      print "foo7"
                                      if latest_status.storage_state == status_entry.storage_state:
                                          print "foo8"
                                          if latest_status.storage_size == status_entry.storage_size:
                                              print "foo9"
                                              latest_status.delete()
                                              status_entry.save()

          else:
              status_entry.save()
      except:
          status_entry.save()





      print "=========== script succeed ============"


    except:
      print "----Fetching failed ---- "+gur.station_code
      logging_entry.failed=gur.station_code+","+str(logging_entry.failed)
      logging_entry.save()
