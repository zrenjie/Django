from . import base_forms
from . import models
from django import forms

class ImageRecordForm(base_forms.BetterModelForm):
    offset_corrected = forms.BooleanField(required=False)
    gain_corrected = forms.BooleanField(required=False)
    defect_corrected = forms.BooleanField(required=False)
    
    class Meta:
        model = models.ImageRecord
        
        fieldsets = (
            ('Basic', {
                'fields':('path_prefix', 'file_type', 'machine_id', 'work_mode', 'sync_mode',
                          'normal', 'created_at', 'creator', 'last_modified_at', 'last_modified_by')}),
            ('Correction', {
                'fields':('offset_corrected', 'gain_corrected', 'defect_corrected')}))


class ImageRecordCreateForm(base_forms.BetterModelForm):
    offset_corrected = forms.BooleanField(required=False)
    gain_corrected = forms.BooleanField(required=False)
    defect_corrected = forms.BooleanField(required=False)
    
    class Meta:
        model = models.ImageRecord
        
        fieldsets = (
            ('Basic', {
                'fields': ('path_prefix', 'file_type', 'machine_id', 'work_mode', 'sync_mode',
                       'normal')}),
            ('Correction', {
                'fields':('offset_corrected', 'gain_corrected', 'defect_corrected')}))