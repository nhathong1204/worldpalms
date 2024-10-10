from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe,strip_tags
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('published', 'Published'),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True,length=10,max_length=20,prefix='cat',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100,default="Food")
    image = models.ImageField(upload_to="category",default="category.jpg")
    
    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True,length=10,max_length=20,alphabet='abcdefgh12345')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product_category')
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path,default="product.jpg")
    description = RichTextUploadingField(null=True,blank=True,default="Enter description here")
    additional_information = RichTextUploadingField(null=True,blank=True,default="Enter additional information here")
    nutritional_value = RichTextUploadingField(null=True,blank=True,default="Enter nutritional value here")
    price = models.DecimalField(max_digits=99999999999, decimal_places=2,default="100000")
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2,default="100000")
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10,default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        
    def product_description(self):
        return strip_tags(self.description)
    product_description.short_description = "Description"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    product_image.short_description = "Image"

    def __str__(self) -> str:
        return self.title
    
    def get_pecentage(self):
        new_price = (self.old_price - self.price) / self.old_price *100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="p_images")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Images'