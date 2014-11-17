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
  guralps_prefix = models.CharField(max_length=50)
  timestamp = models.DateTimeField('date updated')
  status_changed_timestamp = models.DateTimeField('date updated')
  general_status = models.CharField(max_length=50)
  sensor_status  = models.CharField(max_length=50)
  sensor_blocks_rec = models.CharField(max_length=50)
  sensor_timestamp = models.DateTimeField('date updated')
  scream_status  = models.CharField(max_length=50)
  gcf_status = models.CharField(max_length=50)
  ntp_status = models.CharField(max_length=50)
  ntp_estimated_error = models.CharField(max_length=50)
  storage_state = models.CharField(max_length=50)
  storage_last_accessed = models.CharField(max_length=50)
  storage_size = models.CharField(max_length=50)
  system_status = models.CharField(max_length=50)
  system_uptime = models.CharField(max_length=50)
  system_free_space = models.CharField(max_length=50)
  system_free_space_per = models.CharField(max_length=50)
