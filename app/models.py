from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse  
from django.urls import path  
import pandas as pd
import openpyxl
from django.contrib.auth.admin import UserAdmin



# Định nghĩa action export_users_as_excel
def export_users_as_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Users'

    # Tiêu đề các cột
    ws.append(['Username', 'First Name', 'Last Name', 'Email'])

    # Duyệt qua danh sách người dùng và thêm vào Excel
    for user in queryset:
        ws.append([user.username, user.first_name, user.last_name, user.email])

    # Cấu hình để tải file Excel về
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    wb.save(response)
    return response

export_users_as_excel.short_description = "Export selected users to Excel"


# Sử dụng UserAdmin mặc định của Django
class CustomUserAdmin(UserAdmin):
    actions = [export_users_as_excel]

# Đăng ký lại User model với UserAdmin tùy chỉnh của bạn
admin.site.unregister(User)  # Unregister model User trước khi đăng ký lại
admin.site.register(User, CustomUserAdmin)






# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','first_name','last_name','password1','password2']

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property #là chuyển phương thức ở trên sử dụng trực tiếp và k lưu vào database
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 
    # số lượng vp
    @property 
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    # tong giá tiền
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property 
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobi = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address


   
    
    