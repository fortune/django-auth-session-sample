 # Django の認証とセッションの基礎

 Django の認証システムとセッションまわりの基礎的事項を実演するためのサンプルを作成する。

 [Djangoの認証システムを使用する](https://docs.djangoproject.com/ja/2.2/topics/auth/default/)
 [Django の認証方法のカスタマイズ](https://docs.djangoproject.com/ja/2.2/topics/auth/customizing/)
 [セッションの使いかた](https://docs.djangoproject.com/ja/2.2/topics/http/sessions/)

 ## プロジェクトとアプリケーションの作成

 認証システムを実験する `accounts` アプリケーションと、セッションの実験をする `session_test` アプリケーションをつくる。

 ```shell
$ mkdir django-auth-session-sample
$ cd django-auth-session-sample
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install django
(.venv) $ django-admin startproject project .
(.venv) $ python manage.py startapp accounts
(.venv) $ python manage.py startapp session_test
 ```

 `project.settings` モジュールの `INSTALLED_APPS` の最後にここで作成した `accounts` と `session_test` の２つのアプリケーションを登録する。

`INSTALLED_APPS`にはデフォルトでいくつかのアプリケーションが登録されている。その中の `django.contrib.auth` が認証システムを提供するパッケージであり、`django.contrib.sessions` がセッションフレームワークを提供するパッケージだ。データベースのマイグレーションを実行すると、これらが必要とする Model もマイグレーションされる。

認証とセッションは、Django のミドルウェアも使用する。Django の View から透過的に認証、セッションを扱えるようにするために、URL ディスパッチャの前に HTTP リクエストを処理しなければならないからだ。`settings` モジュールの `MIDDLEWARE` には `django.contrib.sessions.middleware.SessionMiddleware` と `django.contrib.auth.middleware.AuthenticationMiddleware` とがデフォルトで含まれている。


 ## User モデルの拡張とデータベースのマイグレーション

Django 提供の認証システム `django.contrib.auth` が使用する User モデルは `django.contrib.auth.models.User` クラスであり、データベースのマイグレーションのときに、これに対応するテーブルがデータベースに作成される。特に必要ないのだが、ここでは User モデルをカスタマイズしてみる。その方法にはいくつかあるが、`django.contrib.auth.models.AbstractUser` クラスを拡張することで実施する。

`accounts.models` モジュールで `django.contrib.auth.models.AbstractUser` を拡張した User クラスを定義し、`project.settings` モジュールで

```python
AUTH_USER_MODEL = 'accounts.User'
```

の定義を追加する。これにより、認証システムはデフォルトの User モデルではなく、指定した `accounts.models.User` クラスを使用するようになる。

その後、データベースのマイグレーションを実行し、superuser を作成する。

```shell
(.venv) $ python manage.py makemigrations accounts
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
```

superuser を作成するとき、拡張した User モデルで追加したフィールドが NULL を許可するか、default 値を指定していないと、エラーになる。


## 拡張した User モデルを管理サイトで確認する

`settings` の `INSTALLED_APPS` には管理サイトを提供する `django.contrib.admin` パッケージが登録されており、その他の必要な設定もされているので、開発用サーバを起動し、上で作成した superuser で管理サイトにログインできる。

```shell
(.venv) $ python manage.py runserver
```

http://localhost:8000/admin/ にアクセスし、ログインしても、ここまでの設定ではユーザを確認できないだろう。自分で作成、あるいは拡張したモデルを管理サイトに表示するには、`admin` モジュールで登録しなければならない。

ここでも、`accounts.admin` モジュールで `accounts.models.User` を登録している。User モデルの場合、password フィールドを暗号化してデータベースに入れるため、管理サイト上でのカスタマイズが必要であり、そのための設定もしている。


## accounts アプリケーションで認証の実験

（開発サーバなら）http://localhost:8000/accounts/ で表示されるページから Django 提供の認証ビューと自作のログインビューを試せるようにした。

[Django 提供の認証ビュー](https://docs.djangoproject.com/ja/2.2/topics/auth/default/#module-django.contrib.auth.views)


Django 提供の認証ビューは以下のとおり。

- django.contrib.auth.views.LoginView
- django.contrib.auth.views.LogoutView
- django.contrib.auth.views.PasswordChangeView
- django.contrib.auth.views.PasswordChangeDoneView
- django.contrib.auth.views.PasswordResetView
- django.contrib.auth.views.PasswordResetDoneView
- django.contrib.auth.views.PasswordResetConfirmView
- django.contrib.auth.views.PasswordResetCompleteView
- django.contrib.auth.views.logout_then_login

`project.urls` モジュールの定義中の

```python
path('accounts/', include('django.contrib.auth.urls')),
path('accounts/logout_then_login/', auth_views.logout_then_login, name='logout_then_login'),
```

がこれらを有効にしている部分だ。ドキュメントに載っているが、`logout_then_login` ビュー関数以外はデフォルトの `name` 属性が定義されているし、すべてデフォルトで使用するフォーム、およびテンプレート名が決まっている。たとえば、`LoginView` ではフォームとして `django.contrib.auth.forms.AuthenticationForm` を使用しているので、自作のログインビュー関数の `accounts.views.login` 関数でもそれを使うようにしている。
 
 デフォルトのテンプレート名はすべて、`registration/login.html` や `registration/logged_out.html`, `registration/password_change_form.html` といったようにすべて `registration/` ではじまる。これらは自分で用意しなければ `django.contrib.admin` パッケージ中の `templates/registration` フォルダ中のものが使用される。つまり、管理サイトで使用しているものが流用されるということだ。それではまずいなら、それらを参考に自作する。

 `registration/login.html` に関してはデフォルトのものがないので自分で作るしかない。`accounts/templates/registration/login.html` に作成した。


 ## session_test アプリケーションでセッションの実験

 セッションオブジェクトは必要なときにデータベースへと保存される。これは `django.contrib.sessions.models.Session` モデルであり、`django.contrib.sessions` が `settings` の `INSTALLED_APPS` に登録されているので、データベースのマイグレーション時に対応するテーブルが作成される。これを管理サイトで確認することができるように `session_test.admin` モジュールで設定した。

 （開発用サーバなら）http://localhost:8000/session-test/ でセッションに書き込みをしない View 関数、http://localhost:8000/session-test/countup/ で書き込みをする View 関数を試せる。


 ## 認証とセッションの関係

 Django ではリクエストのたびにセッションオブジェクトが作成され、View 関数に渡される最初の引数である `HttpRequest` オブジェクトの `session` 属性にセットされるので、View 関数では `request.session` でセッションオブジェクトにアクセスできる。セッションオブジェクトの作成と `HttpRequest` オブジェクトへのセットは、ミドルウェアである `django.contrib.sessions.middleware.SessionMiddleware` がやってくれる。

 セッションオブジェクトへの書き込みが実行されると、session key が生成され、セッション情報がデータベースへと格納される。そして、HTTP のレスポンスには

 ```
 Set-Cookie: sessionid=i7v7i2pqzy8a92ddsb4j4vf4vl61h0ll; expires=Thu, 09 May 2019 02:10:51 GMT; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax
 ```

 のように session key を sessionid という名前のクッキーとして保持するようにブラウザに指示するヘッダがつけられる。以後、ブラウザは、リクエストのたびに

 ```
 Cookie: sessionid=i7v7i2pqzy8a92ddsb4j4vf4vl61h0ll
```

というようなリクエストヘッダがつけられる。`SessionMiddleware` はデータベースから、これを session key とするセッション情報を取得し、それからセッションオブジェクトを生成して HttpRequest オブジェクトにセットする。有効なセッション情報がデータベースになければ、空のセッションオブジェクトを作成する。

ブラウザのツールで sessionid クッキーの値を他人の session key に書き換えることができれば、他人のセッションを乗っ取れる（セッションハイジャック）。

Django 標準の認証システムではセッションを利用している。そのため、`django.contrib.auth.login` 関数で User オブジェクトを登録すると、セッションにユーザの ID が書き込まれ、データベースにセッション情報が格納される。`django.contrib.auth.logout` 関数でログアウトすると、セッションは完全に破棄され、データベースからも削除される。

データベースに新規保存されたセッション情報の有効期限はデフォルトで２週間だ。これを過ぎたセッションの session key をリクエストヘッダで指定しても無視され、空のセッションが作成される。データベースには期限切れのセッション情報が残り続ける。

データベースへはセッションオブジェクトをシリアライズしたものが保存されるので、そのままでは読めない。これを読むには次のようにする。

```shell
(.venv) $ python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> 
>>> session = Session.objects.get(pk='eu6wrgm6vc3m897hsrkybk640voicoqs')
>>> session
<Session: eu6wrgm6vc3m897hsrkybk640voicoqs>
>>> 
>>> session.get_decoded()
{'_auth_user_id': '1', '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend', '_auth_user_hash': '6ecd5a4d48a9bf9eaff9481552f8451b1903b6dc', 'count': 2}
>>>
```

これはログイン済みのユーザの session key を指定して読み出したもの。ログインしていないユーザのセッションなら、`_auth_user_` ではじまるキーは含まれない。

