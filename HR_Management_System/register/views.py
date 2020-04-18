from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

)
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm, EmployeeStatusCreateForm, AccountMasterCreateForm, ProjectMasterCreateForm, RoleMasterCreateForm, EmployeeAssignmentHistoryCreateForm, SkillCategoryMasterCreateForm, SkillMasterCreateForm, EmployeeSkillsCreateForm, EmployeeJobHistoryCreateForm, DteMasterCreateForm, VendorMasterCreateForm, TrainingMasterCreateForm, EmployeeTrainingHistoryCreateForm,
)

from .models import User, EmployeeStatus, AccountMaster, ProjectMaster, RoleMaster, EmployeeAssignmentHistory, SkillCategoryMaster, SkillMaster, EmployeeSkills, EmployeeJobHistory, DteMaster, VendorMaster, TrainingMaster, EmployeeTrainingHistory

from django.core.paginator import Paginator
import csv, io


User = get_user_model()


def about(request):
    return render(request, 'register/about.html')


class Top(generic.TemplateView):
    template_name = 'register/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/top.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('register:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # まだ仮登録で、他に問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    """ユーザーの詳細ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_detail.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー情報更新ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('register:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('register:password_change_done')
    template_name = 'register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'register/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('register/mail_template/email_change/subject.txt', context)
        message = render_to_string('register/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('register:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'register/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

"""
LISTS
"""
def emp_list(request):
    user = User.objects.all()

    paginator = Paginator(user, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/list.html', {'user': user, 'articles': articles})

def vendor_list(request):
    data = VendorMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/vendor_list.html', {'data': data, 'articles': articles})

def dte_list(request):
    data = DteMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/dte_list.html', {'data': data, 'articles': articles})

def project_list(request):
    data = ProjectMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/project_list.html', {'data': data, 'articles': articles})


def training_list(request):
    data = TrainingMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得


    return render(request, 'register/training_list.html', {'data': data, 'articles': articles})


def role_list(request):
    data = RoleMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/role_list.html', {'data': data, 'articles': articles})



def account_list(request):
    data = AccountMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/account_list.html', {'data': data, 'articles': articles})


def skill_list(request):
    data = SkillMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/skill_list.html', {'data': data, 'articles': articles})


def skill_category_list(request):
    data = SkillCategoryMaster.objects.all()

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/skill_category_list.html', {'data': data, 'articles': articles})


def assign_list(request):

    if request.user.is_staff:
        data = EmployeeAssignmentHistory.objects.all()

    else:
        data = EmployeeAssignmentHistory.objects.filter(employee_id=request.user)



    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/assign_list.html', {'data': data, 'articles': articles})


def training_history_list(request):

    if request.user.is_staff:
        data = EmployeeTrainingHistory.objects.all()

    else:
        data = EmployeeTrainingHistory.objects.filter(employee_id=request.user)

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/training_history_list.html', {'data': data, 'articles': articles})


def emp_job_history_list(request):

    if request.user.is_staff:
        data = EmployeeJobHistory.objects.all()

    else:
        data = EmployeeJobHistory.objects.filter(employee_id=request.user)

    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/emp_job_history_list.html', {'data': data, 'articles': articles})


def emp_skill_list(request):

    if request.user.is_staff:
        data = EmployeeSkills.objects.all()

    else:
        data = EmployeeSkills.objects.filter(employee_id=request.user)


    paginator = Paginator(data, 5)  # 1ページに10件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'register/emp_skill_list.html', {'data': data, 'articles': articles})

"""
LISTS END
"""
class IndexView(generic.ListView):
    model = EmployeeStatus

    def models(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emp_list'] = self.object.EmployeeStatus.all()
        return context


class EmpStatusAddView(LoginRequiredMixin, generic.CreateView):
    model = EmployeeStatus
    form_class = EmployeeStatusCreateForm
    success_url = reverse_lazy('register:list')


class EmpStatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmployeeStatus
    form_class = EmployeeStatusCreateForm
    success_url = reverse_lazy('register:list')


class AccountMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = AccountMaster
    form_class = AccountMasterCreateForm
    success_url = reverse_lazy('register:account_list')


class AccountMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmployeeStatus
    form_class = AccountMasterCreateForm
    success_url = reverse_lazy('register:account_list')


class ProjectMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = ProjectMaster
    form_class = ProjectMasterCreateForm
    success_url = reverse_lazy('register:project_list')


class ProjectMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ProjectMaster
    form_class = ProjectMasterCreateForm
    success_url = reverse_lazy('register:project_list')


class RoleMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = RoleMaster
    form_class = RoleMasterCreateForm
    success_url = reverse_lazy('register:role_list')


class RoleMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = RoleMaster
    form_class = RoleMasterCreateForm
    success_url = reverse_lazy('register:role_list')


class EmployeeAssignmentHistoryAddView(LoginRequiredMixin, generic.CreateView):
    model = EmployeeAssignmentHistory
    form_class = EmployeeAssignmentHistoryCreateForm
    success_url = reverse_lazy('register:emp_assign_list')


class EmployeeAssignmentHistoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmployeeAssignmentHistory
    form_class = EmployeeAssignmentHistoryCreateForm
    success_url = reverse_lazy('register:emp_assign_list')


class SkillCategoryMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = SkillCategoryMaster
    form_class = SkillCategoryMasterCreateForm
    success_url = reverse_lazy('register:skill_category_list')


class SkillCategoryMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SkillCategoryMaster
    form_class = SkillCategoryMasterCreateForm
    success_url = reverse_lazy('register:skill_category_list')


class SkillMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = SkillMaster
    form_class = SkillMasterCreateForm
    success_url = reverse_lazy('register:skill_list')

class SkillMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SkillMaster
    form_class = SkillMasterCreateForm
    success_url = reverse_lazy('register:skill_list')


class EmployeeSkillsAddView(LoginRequiredMixin, generic.CreateView):
    model = EmployeeSkills
    form_class = EmployeeSkillsCreateForm
    success_url = reverse_lazy('register:emp_skill_list')


class EmployeeSkillsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmployeeSkills
    form_class = EmployeeSkillsCreateForm
    success_url = reverse_lazy('register:emp_skill_list')



class EmployeeJobHistoryAddView(LoginRequiredMixin, generic.CreateView):
    model = EmployeeJobHistory
    form_class = EmployeeJobHistoryCreateForm
    success_url = reverse_lazy('register:emp_job_history_list')


class EmployeeJobHistoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmployeeJobHistory
    form_class = EmployeeJobHistoryCreateForm
    success_url = reverse_lazy('register:emp_job_history_list')


class DteMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = DteMaster
    form_class = DteMasterCreateForm
    success_url = reverse_lazy('register:dte_list')


class DteMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DteMaster
    form_class = DteMasterCreateForm
    success_url = reverse_lazy('register:dte_list')


class VendorMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = VendorMaster
    form_class = VendorMasterCreateForm
    success_url = reverse_lazy('register:vendor_list')


class VendorMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = VendorMaster
    form_class = VendorMasterCreateForm
    success_url = reverse_lazy('register:vendor_list')


class TrainingMasterAddView(LoginRequiredMixin, generic.CreateView):
    model = TrainingMaster
    form_class = TrainingMasterCreateForm
    success_url = reverse_lazy('register:training_list')


class TrainingMasterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TrainingMaster
    form_class = TrainingMasterCreateForm
    success_url = reverse_lazy('register:training_list')


class EmployeeTrainingHistoryAddView(LoginRequiredMixin, generic.CreateView):
    model = EmployeeTrainingHistory
    form_class = EmployeeTrainingHistoryCreateForm
    success_url = reverse_lazy('register:traiing_history_list')


class EmployeeTrainingHistoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EmployeeTrainingHistory
    form_class = EmployeeTrainingHistoryCreateForm
    success_url = reverse_lazy('register:traiing_history_list')



"""
class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = EmployeeStatus
    success_url = reverse_lazy('register:/')
"""

class DetailView(generic.DetailView):
    model = EmployeeStatus




def vendor_upload(request):
    # declaring template
    template = "register/upload.html"
    data = VendorMaster.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be dte_id, dte_name',
        'data': data
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, "register/upload.html", prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = VendorMaster.objects.update_or_create(
            vendor_id=column[0],
            vendor_name=column[1],
        )
    context = {'data': data}
    head = "Your are uploading Vendor Master Information via CSV"

    return render(request, "register/upload.html", context)



def role_upload(request):
    # declaring template
    template = "register/upload.html"
    data = RoleMaster.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'カラムの並び順は登録フォームの順番に沿って下さい',
        'data': data
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, "register/upload.html", prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = RoleMaster.objects.update_or_create(
            role_id=column[0],
            role_name=column[1],
            role_description=column[2],
        )
    context = {'data': data}
    head = "Your are uploading Vendor Master Information via CSV"

    return render(request, "register/upload.html", context)
