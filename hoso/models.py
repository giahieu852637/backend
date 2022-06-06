from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, null=False,unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ModelUse(models.Model):
    title = models.CharField(max_length=250, null=False)
    image = models.ImageField(upload_to='image/hoso/%Y/%m', default=None, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        

class Field(ModelUse):
    class Meta:
        unique_together = ('title', 'category')
        ordering = ["-id"]

    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class FileHoSo(ModelUse):
    class Meta:
        unique_together = ('title', 'field')
        ordering = ["-id"]

    hoso = models.FileField(upload_to='file/hoso/%Y/%m', default=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, related_name="files" , null=True)


class NopHoSo(ModelUse):

    NONE, SEE, SUCCESS, FAIL = range(4)
    ACTIONS = [
        (NONE, 'Đang chờ'),
        (SEE, 'Đã xem'),
        (SUCCESS, 'Thành công'),
        (FAIL, 'Thất bại'),
    ]
    class Meta:
        unique_together = ('title', 'field')
        ordering = ["-id"]

    fullname = models.TextField(null=True, blank=True)
    cmnd = models.TextField(null=True, blank=True)
    ngaythangnamsinh = models.CharField(max_length=10, null=True, blank=True)
    sonha= models.TextField(null=True, blank=True)
    tonha= models.TextField(null=True, blank=True)
    huyennha = models.TextField(null=True, blank=True)
    tinhnha = models.TextField(null=True, blank=True)
    sdt = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=254)

    hoso = models.FileField(upload_to='file/hoso/%Y/%m', default=None, null=True, blank=True)
    hosoduocky = models.FileField(upload_to='file/hosoky/%Y/%m', default=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="vanban" , null=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, related_name="vanban" , null=True)
    user = models.ForeignKey(User,related_name='hosos', on_delete= models.CASCADE)
    
    status = models.PositiveSmallIntegerField(choices=ACTIONS, default=0)


class StatusHoSo(models.Model):
    class Meta:
        ordering = ["-id"]

    NONE, SEE, SUCCESS, FAIL = range(4)
    ACTIONS = [
        (NONE, 'Đang chờ'),
        (SEE, 'Đã xem'),
        (SUCCESS, 'Thành công'),
        (FAIL, 'Thất bại'),
    ]
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    hosonop = models.OneToOneField(NopHoSo, on_delete= models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=ACTIONS, default=0)
    created_date = models.DateTimeField(auto_now_add=True)




class ActionBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    hoso = models.ForeignKey(FileHoSo, on_delete= models.CASCADE)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    
    class Meta:
        abstract = True # Lớp trừu tượng

class Action(ActionBase):
    NONE, CHECK, FAIL = range(3)
    ACTIONS = [
        (NONE, 'none'),
        (CHECK, 'check'),
        (FAIL, 'fail'),
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=NONE)

class Comment(ActionBase):
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.content


class CauHoi(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    email = models.TextField()
    content = models.TextField()
    contentTL = models.TextField()
    type = models.CharField(max_length=250, null=False)




class CauHoiPublic(models.Model):
    title = models.CharField(max_length=250, null=False)
    content = models.TextField()
    contentTL = models.TextField()

    def __str__(self):
        return self.title