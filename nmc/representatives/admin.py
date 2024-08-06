from django.contrib import admin
from .models import County, Ward, Position, Representative

admin.site.register(County)
admin.site.register(Ward)
admin.site.register(Position)
admin.site.register(Representative)
