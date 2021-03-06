# Generated by Django 2.2.8 on 2020-02-23 10:24

from django.db import migrations
from django.utils import timezone
from django.contrib.auth import get_user_model


def create_superuser(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.

    # Create Superuser
    # https://gist.github.com/inirudebwoy/7eb2d74ea950c38559e5
    super_user = get_user_model()(
        pk=1,
        is_active=True,
        is_superuser=True,
        is_staff=True,
        username='admin',
        email='',
        last_login=timezone.now(),
    )
    super_user.set_password('admin')
    super_user.save()


class Migration(migrations.Migration):

    # First need to create build in user tables like user_auth
    # to be able to create superuser
    # https://docs.djangoproject.com/en/2.2/howto/writing-migrations/#controlling-the-order-of-migrations
    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
