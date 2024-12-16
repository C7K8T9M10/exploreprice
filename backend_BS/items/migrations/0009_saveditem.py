# Generated by Django 4.2.11 on 2024-12-13 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0008_priceimg'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by_users', to='items.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'item')},
            },
        ),
    ]
