from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

UserAdmin.fieldsets[2][1]['fields'] = (


                                        'is_active',
                                        'is_staff',
                                        'is_superuser',
                                        'is_author',
                                        'special_user',
                                        'groups',
                                        'user_permissions',

)

UserAdmin.list_display += ('is_author', 'is_special_user')
admin.site.register(User, UserAdmin)