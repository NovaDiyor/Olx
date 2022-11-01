from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", )}),
        (_("Personal info"), {"fields": ("first_name", "last_name", )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                ),
            },
        ),
        (_("EXTRA"), {
            "fields": ("status", "number", "email")
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(Information)
admin.site.register(AdImage)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(SubRegion)
admin.site.register(Subcategory)
admin.site.register(Ads)
admin.site.register(About)
admin.site.register(Wishlist)

