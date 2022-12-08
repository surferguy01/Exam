from django.urls import path, include
from django.contrib import admin
from exam_app.models import *

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
class WishAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wish, WishAdmin)



urlpatterns = [
    path('admin/',admin.site.urls),
    path('', include('exam_app.urls')),
]
