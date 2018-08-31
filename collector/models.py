from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ImageRecord(models.Model):
    image_file_path = models.CharField(max_length=100)
    path_prefix = models.CharField(_('Field Name: Path prefix'), max_length=50)
    
    FILE_TYPE_RAW = 'raw'
    file_type = models.CharField(_('Field Name: File type'), max_length=10, choices=((FILE_TYPE_RAW, 'RAW'),), default=FILE_TYPE_RAW)
    
    machine_id = models.CharField(_('Field Name: Machine ID'), max_length=20)
    
    WORK_MODE_RAD = 16
    work_mode = models.IntegerField(_('Field Name: Work mode'), choices=((WORK_MODE_RAD, 'rad'),), default=WORK_MODE_RAD)
    
    SYNC_MODE_EXTERNAL = 1
    SYNC_MODE_SOFT = 2
    SYNC_MODE_AUTO = 3
    SYNC_MODE_MANUAL = 4
    SYNC_MODE_SCAN = 5
    SYNC_MODE_CHOICES = ((SYNC_MODE_EXTERNAL, _('External')),
                         (SYNC_MODE_SOFT, _('Soft')),
                         (SYNC_MODE_AUTO, _('Auto AED ')),
                         (SYNC_MODE_MANUAL, _('Manual')),
                         (SYNC_MODE_SCAN, _('Scan AED')),)
    sync_mode = models.IntegerField(_('Field Name: Sync mode'), choices=SYNC_MODE_CHOICES, default=SYNC_MODE_EXTERNAL)
    
    correction = models.IntegerField()
    normal = models.BooleanField(_('Field Name: Normal'), default=True)
    created_at = models.DateTimeField(_('Field Name: Created at'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', verbose_name=_('Field Name: Creator'))
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, 
                                         related_name='modified_by', verbose_name=_('Field Name: Last modifier'))
    last_modified_at = models.DateTimeField(_('Field Name: Last modified at'), blank=True, null=True)
    
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
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    
    def __str__(self):
        return str(_(self.name))
    
class Label(models.Model):
    label_type = models.ForeignKey(LabelType, on_delete=models.CASCADE, verbose_name=_('Field Name: Label type'))
    value = models.CharField(_('Field Name: Label value'), max_length=100)
    record = models.ForeignKey(ImageRecord, on_delete=models.CASCADE, verbose_name=_('Field Name: Record'))
