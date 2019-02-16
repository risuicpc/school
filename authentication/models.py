from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django import forms

class MyUserManager(BaseUserManager):
    def create_user(self, u_name, f_name, m_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not u_name:
            raise ValueError('Users must have an usrer name address')

        user = self.model(
            # email=self.normalize_email(email),
            u_name=u_name,
            f_name=f_name,
            m_name=m_name,  
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, u_name, f_name, m_name,  password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            u_name,
            f_name,
            m_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    r_name      = models.CharField(max_length=10)
    
    def __str__(self):
        return self.r_name

class User(AbstractBaseUser):
    disablity_choices = (
        ('d', 'No Disable'), 
        ('e', 'Eay Disable'),
    )
    valid_phone  = RegexValidator(regex=r'^\+?1?\d{10,15}$', message="Phone number must be entered in the format : 09******** or +2519********")

    f_name          = models.CharField(max_length=255, verbose_name='first name')
    m_name          = models.CharField(max_length=255, verbose_name='middel name')
    l_name          = models.CharField(max_length=255, verbose_name='last name')
    sex             = models.CharField(max_length=2, choices=(('m', 'Male'), ('f', 'Female'),))
    img             = models.ImageField(max_length=255, default='admin-avatar.png', upload_to='profile', verbose_name='Photo')
    u_name          = models.CharField(max_length=255, verbose_name='user name', unique=True)
    email           = models.EmailField(max_length=255, verbose_name='email address', blank=True, null=True)
    phone           = models.CharField(max_length=20, validators=[valid_phone], verbose_name='phone')
    is_admin        = models.BooleanField(default=False)
    role            = models.ManyToManyField(Role, related_name="membership")
    date_of_birth   = models.DateField(blank=True, null=True, verbose_name='date of birth')
    place_of_birth  = models.CharField(max_length=100, blank=True, null=True, verbose_name='place of birth')
    disablity       = models.CharField(max_length=2, choices=disablity_choices, default='d')
    city            = models.CharField(max_length=255, blank=True, null=True, verbose_name='city')
    subcity         = models.CharField(max_length=255, blank=True, null=True, verbose_name='subcity')
    wereda          = models.CharField(max_length=255, blank=True, null=True, verbose_name='wereda')
    home_number     = models.CharField(max_length=20, blank=True, null=True, verbose_name='home number')

    objects = MyUserManager()

    USERNAME_FIELD = 'u_name'
    REQUIRED_FIELDS = ['f_name', 'm_name']

    def __str__(self):
        return '{} {}'.format(self.f_name, self.m_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def fullname(self):
        return '{} {}'.format(self.f_name, self.m_name)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def admin(self):
        try:
            r = Role.objects.get(r_name='admin')
            return r in self.role.all()
        except Role.DoesNotExist:
            return False
    @property
    def is_teacher(self):
        try:
            r = Role.objects.get(r_name='teacher')
            return r in self.role.all()
        except Role.DoesNotExist:
            return False

    @property
    def is_student(self):
        try:
            r = Role.objects.get(r_name='student')
            return r in self.role.all()
        except Role.DoesNotExist:
            return False
    
    @property
    def is_parent(self):
        try:
            r = Role.objects.get(r_name='parent')
            return r in self.role.all()
        except Role.DoesNotExist:
            return False