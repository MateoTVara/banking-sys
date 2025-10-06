from django.contrib import admin
from .models import *

admin.site.register(Test)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(ExchangeRate)
admin.site.register(Account)
admin.site.register(JudicialHold)
admin.site.register(AccountMovement)