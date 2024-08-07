# Generated by Django 5.0.6 on 2024-07-30 11:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="version",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="versions",
                to="catalog.product",
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["name"], name="catalog_pro_name_f603c0_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["price"], name="catalog_pro_price_2d2a4c_idx"),
        ),
        migrations.AddIndex(
            model_name="version",
            index=models.Index(
                fields=["version_number"], name="catalog_ver_version_9b0854_idx"
            ),
        ),
    ]
