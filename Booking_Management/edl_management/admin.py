from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Lab)
admin.site.register(Booking)
admin.site.register(Equipment)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(BookEquipmentLetter)

# admin.site.register(Student)
# admin.site.register(Protest)
# admin.site.register(Borrower)