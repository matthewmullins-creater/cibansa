from django.db import models
from django.contrib.auth.models import  AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import UserManager
import uuid
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    USERNAME_FIELD ="email";
    REQUIRED_FIELDS= ["username"]

    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)
    username = models.CharField(_('username'),max_length=500,blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Un select this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table="cb_user"

    def get_full_name(self):
        return self.profile.get_full_name()

    def get_short_name(self):
        return self.username

    def get_profile_pix(self):
        if self.profile.has_photo:
            return '<img src="http://placehold.it/35x35" alt="%s" class="img-circle" width="75" height="75">' % \
                   self.profile.avatar.url

        else:
            return '<div style="width: 75px;height: 75px;background: #ccc;text-align: center;border-radius: 50%;">' \
                   '<div style="padding-top: 27%;padding-bottom:' \
                   ' 52%;font-size: 23px;">{0}{1}</div></div>'.format(self.profile.first_name[:1],self.profile.last_name[:1])

    def __str__(self):
        return "%s" % (self.get_full_name())



def photo_upload_path(instance,filename):
    return "".join(["%s%s%s%s" %("profile-photo/",str(instance.first_name),str(instance.last_name),"/"),filename])


class CbUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=16,null=True)
    dob = models.DateField(blank=True, null=True)
    country =models.CharField(max_length=2,null=True,blank=True)
    city=models.CharField(null=True,blank=True,max_length=50)

    gender = models.CharField(max_length=10, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar= models.ImageField(blank=True, default="default_avatar.jpg", upload_to=photo_upload_path)
    has_photo = models.BigIntegerField(default=0,null=True)
    is_visible = models.BooleanField(default=True)

    def get_full_name(self):
        return "%s %s" %(self.first_name,self.last_name)

    def get_short_name(self):
        return "%s" %(self.first_name)

    class Meta:
         # managed = False
        db_table = 'cb_user_profile'


class CbTempPassword(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    used = models.BooleanField(default=False)
    created_at =models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table="cb_temp_password"


