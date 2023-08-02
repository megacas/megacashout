# Generated by Django 4.2 on 2023-08-02 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_alter_product_category"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("payment", "0002_chatbot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.product",
            ),
        ),
    ]