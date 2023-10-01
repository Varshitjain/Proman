from django.contrib import admin
from .models import Company
from .models import UserProfile
from .models import Invite
from .models import WorkProfile
from .models import EmpProfile
from .models import EmpAppraisal, SelfEval



class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name','email','city','found_date']
    search_fields = ['name', 'social_name','city']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company','joining','age','gender']

class WorkProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

class InviteAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'invited',]
    search_fields = ['inviter', 'invited',]
    # list_filter = ['inviter', 'invited,']

class EmpProfileAdmin(admin.ModelAdmin):
	list_display = ['emp','salary_level']

class EmpAppraisalAdmin(admin.ModelAdmin):
	list_display = ['emp']

class SelfEvalAdmin(admin.ModelAdmin):
	list_display = ['user']

# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(WorkProfile, WorkProfileAdmin)
admin.site.register(EmpProfile, EmpProfileAdmin)
admin.site.register(EmpAppraisal, EmpAppraisalAdmin)
admin.site.register(SelfEval, SelfEvalAdmin)
