"Admin customization for adcode models."

from django.contrib import admin

from adcode.models import Section, Size, Placement


class PlacementInline(admin.StackedInline):
    model = Placement.sections.through


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'pattern', 'priority', )
    list_editable = ('priority', )
    inlines = (PlacementInline, )
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('-priority', 'name', )
   

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', )
    list_filter = ('width', 'height', )


class PlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', )
    list_filter = ('size', 'sections', )
    filter_horizontal = ('sections', )
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Section, SectionAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Placement, PlacementAdmin)
