# Generated by Django 4.2.13 on 2024-06-23 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_book_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemorder',
            name='livro',
        ),
        migrations.RemoveField(
            model_name='itemorder',
            name='pedido',
        ),
        migrations.AddField(
            model_name='itemorder',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.book', verbose_name='Livro'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemorder',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.order', verbose_name='Pedido'),
            preserve_default=False,
        ),
    ]