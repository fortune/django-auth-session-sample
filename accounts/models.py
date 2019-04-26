from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Django デフォルトの User モデルに属性を追加したモデル。
    認証にはこのモデルを使用する。
    """
    GENDER_CHOICES = (
        (0, '男性'),
        (1, '女性'),
        (2, 'その他'),
    )
    gender = models.IntegerField(verbose_name='性別', choices=GENDER_CHOICES, help_text='ユーザの性別を識別するフィールド', default=2)