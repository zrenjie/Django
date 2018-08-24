from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse

# Create your models here.

class ImageRecord(models.Model):
    image_file_path = models.CharField(max_length=100)
    path_prefix = models.CharField(max_length=20)
    
    FILE_TYPE_RAW = 'raw'
    file_type = models.CharField(max_length=10, choices=((FILE_TYPE_RAW, 'RAW'),), default=FILE_TYPE_RAW)
    
    machine_id = models.CharField(max_length=20)
    
    WORK_MODE_RAD = 16
    work_mode = models.IntegerField(choices=((WORK_MODE_RAD, 'rad'),), default=WORK_MODE_RAD)
    
    SYNC_MODE_EXTERNAL = 1
    SYNC_MODE_SOFT = 2
    SYNC_MODE_AUTO = 3
    SYNC_MODE_MANUAL = 4
    SYNC_MODE_SCAN = 5
    SYNC_MODE_CHOICES = ((SYNC_MODE_EXTERNAL, 'External'),
                         (SYNC_MODE_SOFT, 'Soft'),
                         (SYNC_MODE_AUTO, 'Auto'),
                         (SYNC_MODE_MANUAL, 'Manual'),
                         (SYNC_MODE_SCAN, 'Scan'),)
    sync_mode = models.IntegerField(choices=SYNC_MODE_CHOICES, default=SYNC_MODE_EXTERNAL)
    
    correction = models.IntegerField()
    normal = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='modified_by')
    last_modified_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.image_file_path
    
    def get_absolute_url(self):
        return reverse('collector:record_detail', kwargs={'pk':self.pk})

class Detector(models.Model):
    name = models.CharField(max_length=10)
    prefix = models.CharField(max_length=10)
    width = models.IntegerField()
    height = models.IntegerField()
    desc = models.CharField(max_length=100)
    
    
class Correction(models.Model):
    desc = models.CharField(max_length=100)
    
    
class LabelType(models.Model):
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=100)
    
    
class Label(models.Model):
    label_type = models.ForeignKey(LabelType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    record = models.ForeignKey(ImageRecord, on_delete=models.CASCADE)