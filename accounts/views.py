from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

# Create your views here.


def index(request):
    #return HttpResponse('Hello')
    return render(request, 'accounts/home.html')


def login(request):
    """
    自作のログイン関数

    Django 提供の django.contrib.auth.views.LoginView が実行するログイン処理と
    同じことをしている。

    ログインを実行して、成功したとき、next という名前のフィールドがあったなら、
    そこへリダイレクトさせる。ないならば、settings.LOGIN_REDIRECT_URL へと
    リダイレクトさせる。

    LoginView で使っている AuthenticationForm を使っているが、別に使わなくても
    ログイン処理は書ける（その場合、ここで使っているテンプレートも変える必要があるだろう）。
    ユーザ名とパスワードをリクエストで受け取り、authenticate() 関数で User オブジェクトの
    取得を試行し、取得できたら認証できたということだから、login() 関数でそれをセッションに登録する。
    """
    if request.method == 'GET':
        form = AuthenticationForm()
        next = request.GET.get('next')
        next = '' if next is None else next
        return render(request, 'accounts/mylogin.html', {'form': form, 'next': next})
    elif request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        next = request.POST.get('next')
        next = '' if next is None else next

        # AuthenticationForm の is_valid() は妥当性検証のみならず、認証処理も実行する。
        # その結果が True ならば認証を通ったということであり、get_user() で User オブジェクトも
        # 取得できるので、authenticate() 関数を使う必要がない。
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #user = auth.authenticate(username=username, password=password)
            user = form.get_user()
            if user is not None:
                print(user)
                auth.login(request, user)
                if len(next):
                    return redirect(next)
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                form.add_error(None, 'Failed to authenticate.')
                return render(request, 'accounts/mylogin.html', {'form': form, 'next': next})
                
        else:
            print(form.errors)
            return render(request, 'accounts/mylogin.html', {'form': form, 'next': next})

