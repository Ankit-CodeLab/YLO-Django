from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

class Customer(models.Model):
    
    user = models.OneToOneField(User,null=False,blank=False,on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to='Profile_Pics/', blank=True)

    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATE_CHOICES = [
        ('', 'Select State'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Puducherry', 'Puducherry'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Ladakh', 'Ladakh'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    contact = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.', 'invalid')], blank=True)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$', 'Enter a valid 6-digit pincode.', 'invalid')], blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    def delete_old_profile_pic(self):

        if self.pk:
            old_customer = Customer.objects.get(pk=self.pk)
            if old_customer.profile_pic:
                if os.path.isfile(old_customer.profile_pic.path):
                    os.remove(old_customer.profile_pic.path)

@receiver(pre_save, sender=Customer)
def delete_old_profile_pic(sender, instance, **kwargs):
    if instance.pk:
        old_customer = Customer.objects.get(pk=instance.pk)
        if old_customer.profile_pic != instance.profile_pic:
            old_customer.profile_pic.delete(save=False)
     

class Categorie(models.Model):
    Category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.Category_name


class Product(models.Model):

    Product_Name = models.CharField(max_length=200)
    Category = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    Description = models.TextField()
    Price = models.FloatField(default=0.0)
    Sizes = models.CharField(max_length=50, blank=True, null=True)
    Stock = models.IntegerField(default=0)
    Product_Image = models.ImageField(upload_to='Product_Images/')
    Product_2 = models.IntegerField(default=None,blank=True,null=True)
    Product_3 = models.IntegerField(default=None,blank=True,null=True)

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "pk" : self.pk
        })
    
    def __str__(self):
        return self.Product_Name

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    Ordered = models.BooleanField(default=False)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=100, blank=True ,null=True)
    Quantity = models.IntegerField(default=1)
    Product_Image = models.URLField(null=True, blank=True)
    Order_Delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Quantity} Of {self.Product.Product_Name}"

    def get_total_item_price(self):
        return self.Quantity * self.Product.Price

    def get_final_price(self):
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    Items = models.ManyToManyField(OrderItem)
    Start_Date = models.DateTimeField(auto_now_add=True)
    Ordered_Date = models.DateTimeField()
    Ordered = models.BooleanField(default=False)
    Order_Id = models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    DateTime_Payment = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if self.Order_Id is None and self.DateTime_Payment and self.id:
            self.Order_Id = self.DateTime_Payment.strftime('PAY2ME%d%m%YORD') + str(self.id)

        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total=0
        for Order_Item in self.Items.all():
            total += Order_Item.get_final_price()
        return total
    
    def get_total_count(self):
        Order = Order.Objects.get(pk=self.pk)
        return Order.Items.count()