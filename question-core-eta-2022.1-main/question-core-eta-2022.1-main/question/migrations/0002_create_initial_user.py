from django.db import migrations
from django.contrib.auth.models import User


def create_initial_user(apps, schema_editor):
    User.objects.create_superuser(
        username='admin',
        password='123456',
        is_superuser=True,
        last_login='2020-03-07 02:12:09.779373+00'
    )


class Migration(migrations.Migration):
    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_user)
    ]
