from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import EmployeeStatus, AccountMaster, ProjectMaster, RoleMaster, EmployeeAssignmentHistory, SkillCategoryMaster, SkillMaster, EmployeeSkills, EmployeeJobHistory, DteMaster, VendorMaster, TrainingMaster, EmployeeTrainingHistory


User = get_user_model()
empstatus = EmployeeStatus


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name', 'employee_id', 'date_of_birth', 'career_level',
                  'dte_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ( 'last_name', 'middle_name', 'first_name', 'career_level','dte_name' )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


ACTIVE_STATUS_CHOICES = [
    ('0', 'Employed'),
    ('1', 'Resigned'),
]


class EmployeeStatusCreateForm(forms.ModelForm):

    class Meta:
        model = empstatus
        fields = '__all__'


class AccountMasterCreateForm(forms.ModelForm):

    class Meta:
        model = AccountMaster
        fields = '__all__'


class DteMasterCreateForm(forms.ModelForm):

    class Meta:
        model = DteMaster
        fields = '__all__'


class ProjectMasterCreateForm(forms.ModelForm):

    class Meta:
        model = ProjectMaster
        fields = '__all__'


class EmployeeAssignmentHistoryCreateForm(forms.ModelForm):

    class Meta:
        model = EmployeeAssignmentHistory

        fields = '__all__'


class EmployeeJobHistoryCreateForm(forms.ModelForm):

    class Meta:
        model = EmployeeJobHistory
        fields = '__all__'


class EmployeeSkillsCreateForm(forms.ModelForm):

    class Meta:
        model = EmployeeSkills
        fields = '__all__'


class RoleMasterCreateForm(forms.ModelForm):

    class Meta:
        model = RoleMaster
        fields = '__all__'


class SkillCategoryMasterCreateForm(forms.ModelForm):

    class Meta:
        model = SkillCategoryMaster
        fields = '__all__'


class SkillMasterCreateForm(forms.ModelForm):

    class Meta:
        model = SkillMaster
        fields = '__all__'


class VendorMasterCreateForm(forms.ModelForm):

    class Meta:
        model = VendorMaster
        fields = '__all__'


class TrainingMasterCreateForm(forms.ModelForm):

    class Meta:
        model = TrainingMaster
        fields = '__all__'


class EmployeeTrainingHistoryCreateForm(forms.ModelForm):

    class Meta:
        model = EmployeeTrainingHistory
        fields = '__all__'
