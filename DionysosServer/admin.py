from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Restaurant, Table, Section, Category, FoodSection, Food, Order, UserProfile, OrderedFood

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Section)
admin.site.register(Category)
admin.site.register(FoodSection)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderedFood)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
