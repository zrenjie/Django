from django.views.generic import CreateView, ListView, UpdateView
from . import models
from .forms import ImageRecordCreateForm, LabelForm
from django.forms import inlineformset_factory
from django.utils import timezone
from django.urls import reverse
from collector.forms import ImageRecordForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _

# Create your views here.

@method_decorator(login_required, name='dispatch')
class ImageRecordListView(ListView):
    model = models.ImageRecord
    template_name = "collector/record_list.html"
    context_object_name = 'record_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = models.ImageRecord.objects.all().order_by('-created_at')
        return queryset

@method_decorator(login_required, name='dispatch')
class ImageRecordCreateView(CreateView):
    model = models.ImageRecord
    form_class = ImageRecordCreateForm
    template_name = 'collector/create_record.html'
    
    def get_context_data(self, **kwargs):
        form = ImageRecordCreateForm(initial={
                                            'offset_corrected': True,
                                            'gain_corrected': True,
                                            'defect_corrected': True,
                                            'path_prefix': '\\\\192.168.1.40\\public\\'})
        
        context = super().get_context_data(**kwargs)
        context['form'] = form
        LabelFormSet = inlineformset_factory(models.ImageRecord, models.Label, form=LabelForm)
        if self.request.POST:
            context['labels_formset'] = LabelFormSet(self.request.POST)
        else:
            context['labels_formset'] = LabelFormSet()
            
        return context
    
    def form_invalid(self, form):
        print('form invalid')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        print('form valid')
        print(self.request.POST)
        instance = form.instance
        instance.image_file_path = self.request.POST['absolute_path']
        instance.creator = self.request.user
        instance.created_at = timezone.now()
        
        correction = 0
        offset_corrected = self.request.POST.get('offset_corrected', False)
        if offset_corrected:
            correction |= 0x1
            
        gain_corrected = self.request.POST.get('gain_corrected', False)
        if gain_corrected:
            correction |= 0x2
                
        defect_corrected = self.request.POST.get('defect_corrected', False)
        if defect_corrected:
            correction |= 0x4
            
        instance.correction = correction
        
        labels_formset = self.get_context_data()['labels_formset']
        with transaction.atomic():
            self.object = form.save()
            
            if labels_formset.is_valid():
                labels_formset.instance = self.object
                labels_formset.save()
                
                messages.success(self.request, _('Create record successfully'))

        return super().form_valid(form)
    
    def get_success_url(self):
        if self.request.POST.get('_save', ''):
            print('save')
            return reverse('collector:home')
        elif self.request.POST.get('_addanother',''):
            print('add another')
            return reverse('collector:create_record')
        elif self.request.POST.get('_continue', ''):
            print('_continue')
            return reverse('collector:update_record', kwargs={'pk':self.object.id})


@method_decorator(login_required, name='dispatch') 
class ImageRecordUpdateView(UpdateView):   
    form_class = ImageRecordForm
    model = models.ImageRecord
    template_name = 'collector/create_record.html'
    
    def get_object(self, queryset=None):
        return models.ImageRecord.objects.get(id=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        record = self.get_object()
        image_file_path = record.image_file_path
        
        correction = record.correction
        offset_corrected = bool(correction & 0x01)
        gain_corrected = bool(correction & 0x02)
        defect_corrected = bool(correction & 0x04)
        form = ImageRecordForm(instance = self.get_object(), initial={'offset_corrected':offset_corrected,
                                                                      'gain_corrected': gain_corrected,
                                                                      'defect_corrected':defect_corrected})
        context['form'] = form
        context['image_file_path'] = image_file_path
        
        LabelFormSet = inlineformset_factory(models.ImageRecord, models.Label, form=LabelForm)
        if self.request.method == 'POST':
            formset = LabelFormSet(self.request.POST, instance=record)
            context['labels_formset'] = formset
        else:
            formset = LabelFormSet(instance=record)
            context['labels_formset'] = formset
        
        return context 
    
    def form_invalid(self, form):
        print('form invalid')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        print('form valid')
        print(self.get_context_data())
        instance = form.instance
        print(instance.image_file_path)
        
        if self.request.POST['absolute_path']:
            instance.image_file_path = self.request.POST['absolute_path']
        
        instance.creator = self.request.user
        instance.created_at = timezone.now()
        
        correction = 0
        offset_corrected = self.request.POST.get('offset_corrected', False)
        if offset_corrected:
            correction |= 0x1
            
        gain_corrected = self.request.POST.get('gain_corrected', False)
        if gain_corrected:
            correction |= 0x2
                
        defect_corrected = self.request.POST.get('defect_corrected', False)
        if defect_corrected:
            correction |= 0x4
            
        instance.correction = correction
        instance.last_modified_at = timezone.now()
        instance.last_modified_by = self.request.user
        
        labels_formset = self.get_context_data()['labels_formset']
        with transaction.atomic():
            self.object = form.save()
            
            if labels_formset.is_valid():
                labels_formset.save()
                
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.request.POST.get('_save', ''):
            print('save')
            messages.success(self.request, _('Update record successfully'))
            return reverse('collector:home')
        elif self.request.POST.get('_addanother',''):
            print('add another')
            messages.success(self.request, _('Update record successfully and add another'))
            return reverse('collector:create_record')
        elif self.request.POST.get('_continue', ''):
            print('_continue')
            messages.success(self.request, _('Update record successfully and continue editing'))
            return reverse('collector:update_record', kwargs={'pk':self.object.id})