from django.contrib import admin
from .models import Category, Field, FileHoSo, Action, Action, Comment, NopHoSo,StatusHoSo, CauHoiPublic, CauHoi

admin.site.register(Category)
admin.site.register(Field)
admin.site.register(FileHoSo)
admin.site.register(Action)
admin.site.register(Comment)
admin.site.register(NopHoSo)
admin.site.register(StatusHoSo)
admin.site.register(CauHoiPublic)
admin.site.register(CauHoi)