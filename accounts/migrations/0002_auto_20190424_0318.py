# Generated by Django 2.2 on 2019-04-24 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(0, '男性'), (1, '女性'), (2, 'その他')], default=2, help_text='ユーザの性別を識別するフィールド', verbose_name='性別'),
        ),
    ]
