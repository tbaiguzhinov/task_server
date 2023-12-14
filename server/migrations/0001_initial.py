# Generated by Django 4.2.3 on 2023-12-14 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ErrorLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.CharField(max_length=36, unique=True)),
                ("error", models.TextField()),
                ("date_stamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]