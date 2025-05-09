from django.contrib import admin
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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'Address', 'Phone')
    search_fields = ('user__username', 'user__email', 'Address', 'Phone')
    list_filter = ('user__is_staff', 'user__is_active')


admin.site.register(UserProfiles, UserProfileAdmin)
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

