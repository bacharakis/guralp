from django.db import models

# Create your models here.

class guralp(models.Model):
  prefix = models.CharField(max_length=5)
  last_update = models.DateTimeField('date updated')
  ip = models.CharField(max_length=30)
  general_status = models.CharField(max_length=3)
  sensor_status = models.CharField(max_length=3)
  system_status = models.CharField(max_length=3)

class log(models.Model):
  guralp_prefix = models.CharField(max_length=50)
  timestamp = models.CharField(max_length=50)
  status_changed_timestamp = models.CharField(max_length=50)
  general_status = models.CharField(max_length=50)

  sensor_blocks_out  = models.CharField(max_length=50)
  sensor_blocks_rec = models.CharField(max_length=50)
  sensor_last_event = models.CharField(max_length=50)
  sensor_last_packet_received = models.CharField(max_length=50)

  scream_clients_connected  = models.CharField(max_length=50)
  scream_blocks_5 =  models.CharField(max_length=50)

  gcf_blocks_out = models.CharField(max_length=50)
  gcf_last_blocks_5_minutes = models.CharField(max_length=50)
  gcf_last_samples_5_minutes = models.CharField(max_length=50)

  ntp_status = models.CharField(max_length=50)
  ntp_estimated_error = models.CharField(max_length=50)
  storage_state = models.CharField(max_length=50)
  storage_last_accessed = models.CharField(max_length=50)
  storage_size = models.CharField(max_length=50)
  storage_free_space = models.CharField(max_length=50)

  system_build_machine  = models.CharField(max_length=50)
  system_build_number = models.CharField(max_length=50)
  system_repo = models.CharField(max_length=50)
  root_free_filesystem = models.CharField(max_length=50)
  system_load = models.CharField(max_length=50)
  system_uptime = models.CharField(max_length=50)
