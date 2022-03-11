from django.contrib import admin
from accounts.models import BDSGUser

# Register your models here.
class BDSGUserAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'is_active',)
  list_display_links = ('id', 'user', 'is_active',)
  search_fields = ('user__first_name', 'user__email', 'user__last_name')
  list_per_page = 25

admin.site.register(BDSGUser, BDSGUserAdmin)
