from django.contrib import admin
from core.models import User, VerifyTokenGen, Location, \
                        UserLocation, CategoryService, \
                        Freelancing, FreelancingService, Job

admin.site.register(User)
admin.site.register(VerifyTokenGen)
admin.site.register(Location)
admin.site.register(UserLocation)
admin.site.register(CategoryService)
admin.site.register(Freelancing)
admin.site.register(FreelancingService)
admin.site.register(Job)
