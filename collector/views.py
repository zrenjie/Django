from django.views.generic import CreateView, ListView, UpdateView
from . import models
from .forms import ImageRecordCreateForm
from django.utils import timezone
from django.urls import reverse
from collector.forms import ImageRecordForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        
        instance = form.save()
        self.id = instance.id
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
            return reverse('collector:update_record', kwargs={'pk':self.id})


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
        form = ImageRecordForm(instance = self.get_object())
        context['form'] = form
        context['image_file_path'] = image_file_path
        
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
        
        instance = form.save()
        self.id = instance.id
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
            return reverse('collector:update_record', kwargs={'pk':self.id})