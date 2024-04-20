from django.db import models
from django.urls import reverse
from account.models import User 
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_converter


# Article Manager based on articles that are published.
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')

# Category Manager based on categories that are active.
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)



class IPAddress(models.Model):
    """This model shows the IP addresses of users."""

    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی پی")

    class Meta:
        verbose_name = "آدرس آی پی"
        verbose_name_plural = "آدرس آی پی ها"

        
class Category(models.Model):
    """
    This model is related to the classification of articles, which can 
    create article categories and subcategories for each article.
    """

    parent=models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیر دسته')
    title=models.CharField(max_length=200, verbose_name='دسته بندی عناوین')
    slug=models.SlugField(max_length=100, unique=True,verbose_name='آدرس دسته بندی')
    status=models.BooleanField(default=True,verbose_name='آیا نمایش داده شوند؟')
    position=models.IntegerField(verbose_name='پوزیشن')

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering=['parent__id','position']

    def __str__(self):
        return self.title

    objects = CategoryManager()

class Article(models.Model):
    """This model is related to user articles."""
    
    STATUS_CHOICES=(
        ('d', 'پیش نویس'),        # draft
        ('p', 'منتشرشده'),        # publish
        ('i', 'در حال بررسی'),    # investigation
        ('b', 'برگشت داده شده'),   # back

    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name="نویسنده")
    title=models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug=models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    category=models.ManyToManyField(Category, verbose_name="دسته بندی", related_name="articles")
    description=models.TextField(verbose_name='محتوا')
    thumbnail=models.ImageField(upload_to="images", verbose_name='تصویر مقاله')
    publish=models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    is_special=models.BooleanField(default=False,verbose_name='مقاله ویژه')
    status=models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    hits = models.ManyToManyField(IPAddress, through= "ArticleHit", blank=True, related_name="hits", verbose_name="بازدیدها")
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"
        ordering=['-publish']

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("account:home")
    

    def jpublish(self):
        """This method is for Persianizing the date and time."""

        return jalali_converter(self.publish)
    
    jpublish.short_description = "زمان انتشار"



    def thumbnail_tag(self):
        """
        This method also shows the photos of the articles in the admin 
        panel of Django in the articles section Community Verified icon.
        """

        return format_html("<img width=100 height=75 style = 'border-radius: 13px'; src='{}'>".format(self.thumbnail.url))    
    thumbnail_tag.short_description = "عکس مقاله"


    def category_to_str(self):
        """
        This method puts a comma in the category section where it shows 
        which category the articles belong to so that they can be seen better.
        """

        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description="دسته بندی"


    objects = ArticleManager()


class ArticleHit(models.Model):
    """
    This model is related to the number of views of articles, which 
    counts the number of articles according to the IP address of each user.
    """
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
