from django.contrib import admin
from .models import Article, Category, IPAddress



#Admin header change
admin.site.site_header='وبلاگ جنگویی من'


def make_published(modeladmin, request, queryset):
     """This method will put all or part of the articles 
     in the publishing mode in the admin panel of Django."""

     rows_updated = queryset.update(status='p')
     if rows_updated == 1:
         message_bit = "منتشر شد"
     else:
         message_bit = "منتشر شدند" 
     modeladmin.message_user(request, "{} پست {}".format(rows_updated, message_bit))
make_published.short_description = "انتشار مقاله های انتخاب شده"



def make_draft(modeladmin, request, queryset):
     """This method will put all or part of the articles 
     in the draft mode in the admin panel of Django."""

     rows_updated = queryset.update(status='d')
     if rows_updated == 1:
         message_bit = "پیش نویس شد"
     else:
         message_bit = "پیش نویس شدند" 
     modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_draft.short_description = "پیش نویس شدن مقاله های انتخاب شده"



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position','title','slug','parent','status')
    list_filter = (['status'])
    search_fields = ('title','slug')
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Category, CategoryAdmin)



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','thumbnail_tag','slug','author','jpublish','is_special','status','category_to_str')
    list_filter = ('publish','status')
    search_fields = ('title','description')
    prepopulated_fields = {'slug':('title',)}
    ordering=['-status', '-publish']
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
admin.site.register(IPAddress)