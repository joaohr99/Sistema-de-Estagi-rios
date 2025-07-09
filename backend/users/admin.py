# users/admin.py

from django.contrib import admin
from .models import CustomUser, EstagiarioProfile, ResponsavelFaculdadeProfile, ResponsavelUPALaProfile, RegistroProgresso

admin.site.register(CustomUser)
admin.site.register(EstagiarioProfile)
admin.site.register(ResponsavelFaculdadeProfile)
admin.site.register(ResponsavelUPALaProfile)
admin.site.register(RegistroProgresso)