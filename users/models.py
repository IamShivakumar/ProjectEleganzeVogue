from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from datetime import datetime
import random, string


# Create your models here.

class usermanager(BaseUserManager):
    def create_user(self,first_name,last_name,username,password,email,**extrafields):
        if not email:
            raise ValueError("email is mandatory")
        if not username:
            raise ValueError("username is mandatory")
        user=self.model(email=self.normalize_email(email),
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,password,email,**extrafields):
        extrafields.setdefault('is_staff',True)
        extrafields.setdefault('is_admin',True)
        return self.create_user('','',username,password,email,**extrafields)


class CustomUser(AbstractBaseUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=50,unique=True)
    first_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    phone_number=models.PositiveBigIntegerField(null=True)
    modified_date=models.DateTimeField(auto_now=True,)
    created_date=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    wallet_balance=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    referral_code=models.CharField(max_length=50,null=True,blank=True)


    objects= usermanager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email','password']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    def generate_referral_code(self):
        prefix = self.username[:4]
        suffix = ''.join(random.choices(string.digits, k=4))
        self.referral_code = prefix.upper() + suffix
        self.save()

    class Meta:
        db_table="users"
    

class userAddress(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_address')
    name=models.CharField(max_length=150,null=False)
    house_no=models.CharField(max_length=10,null=False)
    street=models.CharField(max_length=50)
    state=models.CharField(max_length=50,null=False)
    city=models.CharField(max_length=100,null=False,default='City Unknown')
    pincode=models.BigIntegerField()
    is_primary=models.BooleanField(default=False)

    class Meta:
        db_table="users_address"


