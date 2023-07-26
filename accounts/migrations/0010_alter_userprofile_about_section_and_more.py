# Generated by Django 4.2.2 on 2023-07-25 03:45

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0009_alter_userprofile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="about_section",
            field=models.TextField(blank=True, default="", max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="passions",
            field=models.TextField(blank=True, default="", max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=accounts.models.user_profile_picture_path,
            ),
        ),
    ]
