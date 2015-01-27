from django.db import models

# Create your models here.

class guralp(models.Model):
  def __str__(self):              # __unicode__ on Python 2
        return self.prefix
  prefix = models.CharField(max_length=5)
  seira_episkepsis = models.CharField(max_length=30, null=True)

  last_update = models.DateTimeField('date updated')
  ip = models.CharField(max_length=30)
  url = models.CharField(max_length=50)
  subnet_mask = models.CharField(max_length=30, null=True)
  gateway = models.CharField(max_length=30, null=True)
  internal_ip = models.CharField(max_length=30, null=True)
  syvzexis_ip = models.CharField(max_length=30, null=True)
  syvzexis = models.CharField(max_length=10, null=True)
  technician = models.CharField(max_length=60, null=True)
  technician_crew = models.CharField(max_length=80, null=True)
  technicians_phone = models.CharField(max_length=30, null=True)
  region = models.CharField(max_length=70, null=True)
  building = models.CharField(max_length=70, null=True)
  address = models.CharField(max_length=120, null=True)
  installed = models.CharField(max_length=30, null=True)
  status = models.CharField(max_length=30, null=True)
  status_details = models.CharField(max_length=30, null=True)
  firmware_update_status  = models.CharField(max_length=30, null=True)
  cords  = models.CharField(max_length=30, null=True)


class status(models.Model):
  def __str__(self):              # __unicode__ on Python 2
        return self.guralp_prefix
  guralp_prefix = models.CharField(max_length=50 ,null=True)
  timestamp = models.CharField(max_length=50 ,null=True)
  status_changed_timestamp = models.CharField(max_length=50 ,null=True)
  general_status = models.CharField(max_length=50 ,null=True)

  sensor_blocks_out  = models.CharField(max_length=50 ,null=True)
  sensor_blocks_rec = models.CharField(max_length=50 ,null=True)
  sensor_last_event = models.CharField(max_length=50 ,null=True)
  sensor_last_packet_received = models.CharField(max_length=50 ,null=True)

  scream_clients_connected  = models.CharField(max_length=50 ,null=True)
  scream_blocks_5 =  models.CharField(max_length=50 ,null=True)

  gcf_blocks_out = models.CharField(max_length=50 ,null=True)
  gcf_last_blocks_5_minutes = models.CharField(max_length=50 ,null=True)
  gcf_last_samples_5_minutes = models.CharField(max_length=50 ,null=True)

  ntp_status = models.CharField(max_length=50 ,null=True)
  ntp_estimated_error = models.CharField(max_length=50 ,null=True)
  storage_state = models.CharField(max_length=50 ,null=True)
  storage_last_accessed = models.CharField(max_length=50 ,null=True)
  storage_size = models.CharField(max_length=50 ,null=True)
  storage_free_space = models.CharField(max_length=50 ,null=True)

  system_build_machine  = models.CharField(max_length=50,null=True)
  system_build_number = models.CharField(max_length=50,null=True)
  system_repo = models.CharField(max_length=50,null=True)
  root_free_filesystem = models.CharField(max_length=50,null=True)
  system_load = models.CharField(max_length=50,null=True)
  system_uptime = models.CharField(max_length=50,null=True)

class log(models.Model):
  def __str__(self):              # __unicode__ on Python 2
        return self.guralp_prefix
  guralp_prefix = models.CharField(max_length=50 ,null=True)
  timestamp = models.CharField(max_length=50 ,null=True)
  status_changed_timestamp = models.CharField(max_length=50 ,null=True)
  general_status = models.CharField(max_length=50 ,null=True)

  sensor_blocks_out  = models.CharField(max_length=50 ,null=True)
  sensor_blocks_rec = models.CharField(max_length=50 ,null=True)
  sensor_last_event = models.CharField(max_length=50 ,null=True)
  sensor_last_packet_received = models.CharField(max_length=50 ,null=True)

  scream_clients_connected  = models.CharField(max_length=50 ,null=True)
  scream_blocks_5 =  models.CharField(max_length=50 ,null=True)

  gcf_blocks_out = models.CharField(max_length=50 ,null=True)
  gcf_last_blocks_5_minutes = models.CharField(max_length=50 ,null=True)
  gcf_last_samples_5_minutes = models.CharField(max_length=50 ,null=True)

  ntp_status = models.CharField(max_length=50 ,null=True)
  ntp_estimated_error = models.CharField(max_length=50 ,null=True)
  storage_state = models.CharField(max_length=50 ,null=True)
  storage_last_accessed = models.CharField(max_length=50 ,null=True)
  storage_size = models.CharField(max_length=50 ,null=True)
  storage_free_space = models.CharField(max_length=50 ,null=True)

  system_build_machine  = models.CharField(max_length=50,null=True)
  system_build_number = models.CharField(max_length=50,null=True)
  system_repo = models.CharField(max_length=50,null=True)
  root_free_filesystem = models.CharField(max_length=50,null=True)
  system_load = models.CharField(max_length=50,null=True)
  system_uptime = models.CharField(max_length=50,null=True)

class logging(models.Model):
  def __str__(self):
      return self.timestamp

  timestamp = models.CharField(max_length=50 ,null=True)
  failed = models.CharField(max_length=1000 ,null=True)
  succeed = models.CharField(max_length=1000 ,null=True)
