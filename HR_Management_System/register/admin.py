from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User
from register.models import DteMaster, EmployeeStatus, AccountMaster, ProjectMaster, RoleMaster, EmployeeAssignmentHistory, SkillCategoryMaster, SkillMaster, EmployeeSkills,EmployeeJobHistory,EmployeeTrainingHistory,TrainingMaster,VendorMaster

admin.site.register(EmployeeStatus)
admin.site.register(AccountMaster)
admin.site.register(ProjectMaster)
admin.site.register(RoleMaster)
admin.site.register(EmployeeAssignmentHistory)
admin.site.register(EmployeeJobHistory)
admin.site.register(DteMaster)
admin.site.register(SkillCategoryMaster)
admin.site.register(SkillMaster)
admin.site.register(EmployeeSkills)
admin.site.register(EmployeeTrainingHistory)
admin.site.register(TrainingMaster)
admin.site.register(VendorMaster)


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class EmployeeStatusChangeForm(UserChangeForm):
    class Meta:
        model = EmployeeStatus
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name' ,'employee_id', 'date_of_birth',
                                         'career_level', 'dte_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)
