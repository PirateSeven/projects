from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django import forms


class DteMaster(models.Model):
    dte_id = models.CharField(_('DTE ID'), max_length=8, null=True, blank=True)
    dte_name = models.CharField(_('DTE Name'), max_length=50, null=True, blank=True)
    registered_date = models.DateTimeField(_('date joined'), default=timezone.now)

    def __str__(self):
        return self.dte_name

class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル

    usernameを使わず、emailアドレスをユーザー名として使うようにしています。

    """
    email = models.EmailField(_('Enterprise ID'), unique=True)
    # enterprise_id = email
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    # employee_name = models.CharField(last_name + first_name)
    employee_id = models.CharField(_('employee id'), max_length=8, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    career_level_CHOICES = [
        ('1', 'CL1'),
        ('2', 'CL2'),
        ('3', 'Cl3'),
        ('4', 'CL4'),
        ('5', 'CL5'),
        ('6', 'CL6'),
        ('7', 'CL7'),
        ('8', 'CL8'),
        ('9', 'CL9'),
        ('10', 'CL10'),
        ('11', 'CL11'),
        ('12', 'CL12'),
        ('13', 'CL13'),
    ]
    career_level = models.CharField(
        max_length=4,
        choices=career_level_CHOICES,
        default="0",
    )
    dte_id = models.CharField(_('IGNORE'), max_length=5, blank=True)
    dte_name = models.ForeignKey(DteMaster, on_delete=models.CASCADE, null=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    CAREER_LEVEL_FIELD = 'Career Level'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email

# GENERIC CHOICES
GENERIC_ACTIVE_STATUS_CHOICES = [
    ('0', 'inactive'),
    ('1', 'active'),
]

class EmployeeStatus(models.Model):
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ACTIVE_STATUS_CHOICES = [
        ('0', 'Employed'),
        ('1', 'Resigned'),
    ]
    active_status = models.CharField(
        max_length=1,
        choices=ACTIVE_STATUS_CHOICES,
        default="0",
    )
    joined_date = models.DateField(_('Joined Date'), null=True, blank=False)
    resigned_date = models.DateField(_('Resigned Date'), null=True, blank=True)

    def __str__(self):
        return self.employee_id.employee_id

class AccountMaster(models.Model):
    account_id = models.CharField(_('Account ID'), max_length=8, blank=False)
    account_name = models.CharField(_('Account Name'), max_length=50, blank=False)
    registered_date = models.DateField(_('Registered Date'), null=True, blank=True)
    active_status = models.CharField(_('Active Status'),
        max_length=1,
        choices=GENERIC_ACTIVE_STATUS_CHOICES,
        default="1",
    )
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.account_name

class ProjectMaster(models.Model):
    # account_id = models.ForeignKey(AccountMaster, on_delete=models.CASCADE, related_name="account_ids2")
    account_name = models.ForeignKey(AccountMaster, on_delete=models.CASCADE, related_name="account_names2")
    project_id = models.CharField(_('Project ID'), max_length=8, blank=False)
    project_name = models.CharField(_('Project Name'), max_length=50, blank=False)
    registered_date = models.DateField(_('Registered Date'), null=True, blank=True)
    active_status = models.CharField(_('Active Status'),
        max_length=1,
        choices=GENERIC_ACTIVE_STATUS_CHOICES,
        default="1",
    )
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.project_name


class RoleMaster(models.Model):
    role_id = models.CharField(_('Role ID'), max_length=8, blank=False)
    role_name = models.CharField(_('Role Name'), max_length=50, blank=False)
    role_description = models.CharField(_('Role Description'), max_length=50, blank=False)
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.role_name

class EmployeeAssignmentHistory(models.Model):
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_ids")
    # account_id = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE,  related_name="account_ids3")
    account_name = models.ForeignKey(AccountMaster, on_delete=models.CASCADE,  related_name="account_names3")
    project_name = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE,  related_name="project_ids")
    role_name = models.ForeignKey(RoleMaster, on_delete=models.CASCADE,  related_name="role_names")
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.employee_id.employee_id


class SkillCategoryMaster(models.Model):
    skill_category_id = models.CharField(_('Skill Category'), max_length=8, blank=False)
    skill_category_name = models.CharField(_('Skill Category Name'), max_length=50, blank=False)
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.skill_category_name


class SkillMaster(models.Model):
    skill_id = models.CharField(_('Skill ID'), max_length=8, blank=False)
    skill_name = models.CharField(_('Skill Name'), max_length=50, blank=False)
    skill_category_name = models.ForeignKey(SkillCategoryMaster, on_delete=models.CASCADE,
                                            related_name="skill_category_name1")
    active_status = models.CharField(_('Active Status'),
                                     max_length=1,
                                     choices=GENERIC_ACTIVE_STATUS_CHOICES,
                                     default="1",
                                     )
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.skill_name

class EmployeeSkills(models.Model):
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_ids2")
    skill_category_name = models.ForeignKey(SkillCategoryMaster, on_delete=models.CASCADE,
                                            related_name="skill_category_name2")
    skill_name = models.ForeignKey(SkillMaster, on_delete=models.CASCADE,  related_name="skill_name2")

    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.employee_id.employee_id


class EmployeeJobHistory(models.Model):
    role_description = models.CharField(_('Role Description'), max_length=50, blank=False)
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_ids7")
    exp_detail = models.CharField(_('Exp Detail'), max_length=200, blank=False)
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.employee_id.employee_id


class VendorMaster(models.Model):
    vendor_id = models.CharField(_('Vendor Id'), max_length=8, blank=False, primary_key=True)
    vendor_name = models.CharField(_('Vendor Name'), max_length=50, blank=False)
    active_status = models.CharField(_('Active Status'),
                                     max_length=1,
                                     choices=GENERIC_ACTIVE_STATUS_CHOICES,
                                     default="1",
                                     )
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.vendor_name


class TrainingMaster(models.Model):
    training_id = models.CharField(_('Training Id'), max_length=8, blank=False, primary_key=True)
    training_name = models.CharField(_('Training Name'), max_length=50, blank=False)
    vendor_name = models.ForeignKey(VendorMaster, on_delete=models.CASCADE, related_name="vendor_name1")
    active_status = models.CharField(_('Active Status'),
                                     max_length=1,
                                     choices=GENERIC_ACTIVE_STATUS_CHOICES,
                                     default="1",
                                     )
    registered_date = models.DateField(_('Registered Date'), null=True, blank=True)

    def __str__(self):
        return self.training_name


class EmployeeTrainingHistory(models.Model):
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_ids3")
    completion_date = models.DateField(_('Completion Date'), null=True, blank=True)
    training_name = models.ForeignKey(TrainingMaster, on_delete=models.CASCADE, related_name="training_name1")
    registered_date = models.DateTimeField(_('Registered Date'), default=timezone.now)

    def __str__(self):
        return self.employee_id.employee_id
