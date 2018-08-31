from . import base_forms
from . import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.forms.formsets import DELETION_FIELD_NAME

class ImageRecordForm(base_forms.BetterModelForm):
    offset_corrected = forms.BooleanField(required=False, label=_('Form field: Offset corrected'))
    gain_corrected = forms.BooleanField(required=False, label=_('Form field: Gain corrected'))
    defect_corrected = forms.BooleanField(required=False, label=_('Form field: Defect corrected'))
    
    class Meta:
        model = models.ImageRecord
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'readonly':True}),
            'last_modified_at': forms.DateTimeInput(attrs={'readonly':True})}
        
        fieldsets = (
            (_('Fieldset: Basic'), {
                'fields':('path_prefix', 'file_type', 'machine_id', 'work_mode', 'sync_mode',
                          'normal', 'created_at', 'creator', 'last_modified_at', 'last_modified_by')}),
            (_('Fieldset: Correction'), {
                'fields':('offset_corrected', 'gain_corrected', 'defect_corrected')}))


class ImageRecordCreateForm(base_forms.BetterModelForm):
    offset_corrected = forms.BooleanField(required=False)
    gain_corrected = forms.BooleanField(required=False)
    defect_corrected = forms.BooleanField(required=False)
    
    class Meta:
        model = models.ImageRecord
        
        fieldsets = (
            (_('Fieldset: Basic'), {
                'fields': ('path_prefix', 'file_type', 'machine_id', 'work_mode', 'sync_mode',
                       'normal')}),
            (_('Fieldset: Correction'), {
                'fields':('offset_corrected', 'gain_corrected', 'defect_corrected')}))
        
        
class LabelForm(forms.ModelForm):
    value = forms.CharField(label=_('Field Name: Label value'), widget=forms.TextInput(attrs={'size':50}))
    class Meta:
            model = models.Label
            exclude = ()
