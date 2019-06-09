from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Employee])
admin.site.register([Student])
admin.site.register([Nationality])
admin.site.register([Blog])
admin.site.register([Author])
admin.site.register([Entry])
admin.site.register([UserKey])
admin.site.register([Bookmark])