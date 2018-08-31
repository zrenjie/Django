from django.contrib import admin
from . import models

# Register your models here.
class LabelInLine(admin.TabularInline):
    model = models.Label
    extra = 1
    
class RecordAdmin(admin.ModelAdmin):
    inlines = [LabelInLine, ]
    list_display = ("__str__", "machine_id", "work_mode",
                  "sync_mode", "normal", "created_at", "last_modified_at", "creator")
    
    list_filter = ('normal', 'sync_mode', 'created_at', 'creator')
    
    search_fields = ['image_file_path', 'machine_id']
    fieldsets = (
            ("Basic", {
                'fields': ("image_file_path", "file_type", "machine_id", "work_mode",
                  "sync_mode", 'normal', 'creator')
                    }),
            )

 
class DetectorAdmin(admin.ModelAdmin):
    list_display = ("name", "prefix", "width", "height", "desc")
    

class CorrectionAdmin(admin.ModelAdmin):
    list_display = ("desc",)
    

class LabelTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "desc")
    
    
class LabelAdmin(admin.ModelAdmin):
    list_display = ("label_type", "value", "record")  
         
admin.site.register(models.ImageRecord, RecordAdmin)
admin.site.register(models.Detector, DetectorAdmin)
admin.site.register(models.Correction, CorrectionAdmin)
admin.site.register(models.LabelType, LabelTypeAdmin)
admin.site.register(models.Label, LabelAdmin)