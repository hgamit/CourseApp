# Generated by Django 2.2.7 on 2020-01-27 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maintain', '0004_auto_20200116_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clas_hware',
            name='hware_notes',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='class_description',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='class_type',
        ),
        migrations.AddField(
            model_name='classroom',
            name='class_computers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classroom',
            name='class_instr_computer',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
