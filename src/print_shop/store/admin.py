from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfiles,
    Materials,
    Filament,
    Suppliers,
    RawMaterials,
    InventoryChange,
    Models,
    Shipping,
    Orders,
    OrderItems,
    FulfillmentStatus,
)


class UserProfileInline(admin.StackedInline):
    model = UserProfiles
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Materials)
admin.site.register(Filament)
admin.site.register(Suppliers)
admin.site.register(RawMaterials)
admin.site.register(InventoryChange)
admin.site.register(Models)
admin.site.register(Shipping)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(FulfillmentStatus)

