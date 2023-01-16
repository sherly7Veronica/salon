from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.core import validators  



class UserAccountManager(BaseUserManager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
          
        user = self.model(
            email = self.normalize_email(email) , 
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def create_superuser(self , email , password):
        user = self.create_user(
            email = self.normalize_email(email) , 
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
      
class UserAccount(AbstractBaseUser):
    class Types(models.TextChoices):
        STUDENT = "STUDENT" , "student"
        TEACHER = "TEACHER" , "teacher"
          
    type = models.CharField(max_length = 8 , choices = Types.choices , 
                            # Default is user is teacher
                            default = Types.TEACHER)
    email = models.EmailField(max_length = 200 , unique = True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
      
    # special permission which define that
    # the new user is teacher or student 
    is_student = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)
      
    USERNAME_FIELD = "email"
      
    # defining the manager for the UserAccount model
    objects = UserAccountManager()
      
    def __str__(self):
        return str(self.email)
      
    def has_perm(self , perm, obj = None):
        return self.is_admin
      
    def has_module_perms(self , app_label):
        return True
      
    def save(self , *args , **kwargs):
        if not self.type or self.type == None : 
            self.type = UserAccount.Types.TEACHER
        return super().save(*args , **kwargs)
        
class StudentManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.STUDENT)
        return queryset    
        
class Student(UserAccount):
    class Meta : 
        proxy = True
    objects = StudentManager()
      
    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.STUDENT
        self.is_student = True
        return super().save(*args , **kwargs)
      
class TeacherManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    def get_queryset(self , *args , **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.TEACHER)
        return queryset
      
class Teacher(UserAccount):
    class Meta :
        proxy = True
    objects = TeacherManager()
      
    def save(self  , *args , **kwargs):
        self.type = UserAccount.Types.TEACHER
        self.is_teacher = True
        return super().save(*args , **kwargs)    


class Product(models.Model):
    name = models.CharField(max_length=80)            
    price = models.IntegerField()
    # user = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)    

    def __str__(self):
        return self.name

class OrderDetail(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(
        verbose_name='Customer Email'
    )

    product = models.ForeignKey(
        to=Product,
        verbose_name='Product',
        on_delete=models.PROTECT
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    stripe_payment_intent = models.CharField(
        max_length=200, null=True
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )