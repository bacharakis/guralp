from django.db import models


class stations(models.Model):
    def __str__(self):              # __unicode__ on Python 2
          return self.station_code
    station_code = models.CharField(max_length=5)
    station_name = models.CharField(max_length=80, null=True)
    site  = models.CharField(max_length=80, null=True)
    fi  = models.CharField(max_length=30, null=True)
    lamda = models.CharField(max_length=30, null=True)
    height = models.CharField(max_length=30, null=True)
    typeof_building = models.CharField(max_length=30, null=True)
    placeof_installation = models.CharField(max_length=30, null=True)
    site_class =models.CharField(max_length=30, null=True)
    geo_reference = models.CharField(max_length=30, null=True)
    vs30 = models.CharField(max_length=30, null=True)
    soil_class = models.CharField(max_length=30, null=True)
    history = models.CharField(max_length=30, null=True)
    owner = models.CharField(max_length=30, null=True)
    sinv = models.CharField(max_length=30, null=True)

class events(models.Model):
    def __str__(self):              # __unicode__ on Python 2
          return self.event_id
    event_id = models.CharField(max_length=30)
    date = models.CharField(max_length=30, null=True)
    time = models.CharField(max_length=30, null=True)
    fi = models.CharField(max_length=30, null=True)
    lamda = models.CharField(max_length=30, null=True)
    depth = models.CharField(max_length=30, null=True)
    mi = models.CharField(max_length=30, null=True)
    mb = models.CharField(max_length=30, null=True)
    ms = models.CharField(max_length=30, null=True)
    mw = models.CharField(max_length=30, null=True)
    mo = models.CharField(max_length=30, null=True)
    strike = models.CharField(max_length=30, null=True)
    dip = models.CharField(max_length=30, null=True)
    rake = models.CharField(max_length=30, null=True)
    notes = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=100, null=True)
