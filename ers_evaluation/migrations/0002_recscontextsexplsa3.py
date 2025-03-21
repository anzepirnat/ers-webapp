# Generated by Django 5.1.3 on 2025-03-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ers_evaluation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecsContextsExplsA3",
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
                ("elder_id", models.IntegerField()),
                ("activity_ids", models.CharField(max_length=100)),
                ("activity_texts", models.CharField(max_length=300)),
                ("context_time", models.CharField(max_length=100)),
                ("context_place", models.CharField(max_length=100)),
                ("explanation", models.CharField(max_length=1000)),
            ],
        ),
    ]
