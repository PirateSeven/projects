from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('about/', views.about, name='about'),
    path('emp/', views.IndexView.as_view(), name='index'),
    path('emp/status/add/', views.EmpStatusAddView.as_view(), name='emp_status_add'),
    path('emp/status/update/<int:pk>/', views.EmpStatusUpdateView.as_view(), name='emp_status_update'),
    path('emp/skills/add/', views.EmployeeSkillsAddView.as_view(), name='emp_skills_add'),
    path('emp/skills/update/<int:pk>/', views.EmployeeSkillsUpdateView.as_view(), name='emp_skills_update'),
    path('emp/skills/list', views.emp_skill_list, name='emp_skill_list'),


    path('emp/jobhistory/add/', views.EmployeeJobHistoryAddView.as_view(), name='emp_job_hist_add'),
    path('emp/jobhistory/update/<int:pk>/', views.EmployeeJobHistoryUpdateView.as_view(), name='emp_job_hist_update'),
    path('emp/jobhistory/list', views.emp_job_history_list, name='emp_job_history_list'),



    path('emp/assignment/add/', views.EmployeeAssignmentHistoryAddView.as_view(), name='emp_assign_add'),
    path('emp/assignment/update/<int:pk>/', views.EmployeeAssignmentHistoryUpdateView.as_view(), name='emp_assign_update'),
    path('master/assignment/list', views.assign_list, name='emp_assign_list'),

    path('emp/training_history/add/', views.EmployeeTrainingHistoryAddView.as_view(), name='emp_training_history_add'),
    path('emp/training_history/update/<int:pk>/', views.EmployeeTrainingHistoryUpdateView.as_view(), name='emp_training_history_update'),
    path('master/training_history/list', views.training_history_list, name='traiing_history_list'),



    # path('emp/delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path('master/account/add/', views.AccountMasterAddView.as_view(), name='master_account_add'),
    path('master/account/update/<int:pk>/', views.AccountMasterUpdateView.as_view(), name='master_account_update'),
    path('master/account/list', views.account_list, name='account_list'),
    path('master/project/add/', views.ProjectMasterAddView.as_view(), name='master_project_add'),
    path('master/project/update/<int:pk>/', views.ProjectMasterUpdateView.as_view(), name='master_project_update'),
    path('master/project/list', views.project_list, name='project_list'),

    path('master/role/add/', views.RoleMasterAddView.as_view(), name='master_role_add'),
    path('master/role/update/<int:pk>/', views.RoleMasterUpdateView.as_view(), name='master_role_update'),
    path('master/role/upload', views.role_upload, name='role_upload'),
    path('master/role/list', views.role_list, name='role_list'),

    path('master/skill/category/add/', views.SkillCategoryMasterAddView.as_view(), name='master_skill_ctg_add'),
    path('master/skill/category/update/<int:pk>/', views.SkillCategoryMasterUpdateView.as_view(), name='master_skill_ctg_update'),
    path('master/skill/ctg/list', views.skill_category_list, name='skill_category_list'),


    path('master/skill/add/', views.SkillMasterAddView.as_view(), name='master_skill_add'),
    path('master/skill/update/<int:pk>/', views.SkillMasterUpdateView.as_view(), name='master_skill_update'),
    path('master/skill/list', views.skill_list, name='skill_list'),

    path('master/dte/add/', views.DteMasterAddView.as_view(), name='master_dte_add'),
    path('master/dte/update/<int:pk>/', views.DteMasterUpdateView.as_view(), name='master_dte_update'),
    path('master/dte/list', views.dte_list, name='dte_list'),
    # path('master/dte/upload', views.dte_upload, name='dte_upload'),


    path('master/vendor/add/', views.VendorMasterAddView.as_view(), name='master_vendor_add'),
    path('master/vendor/update/<int:pk>/', views.VendorMasterUpdateView.as_view(), name='master_vendor_update'),
    path('master/vendor/upload', views.vendor_upload, name='vendor_upload'),
    path('master/vendor/list', views.vendor_list, name='vendor_list'),

    path('master/training/add/', views.TrainingMasterAddView.as_view(), name='master_training_add'),
    path('master/training/update/<int:pk>/', views.TrainingMasterUpdateView.as_view(), name='master_training_update'),
    path('master/training/list', views.training_list, name='training_list'),








    path('emp/list/', views.emp_list, name='list'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
]
