# Generated by Django 4.1.1 on 2022-10-01 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_articlemodel_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlemodel',
            options={'ordering': ['-publish'], 'verbose_name': 'مقاله', 'verbose_name_plural': 'مقالات'},
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='blog.categorymodel', verbose_name='عبارت زیر دسته '),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='category',
            field=models.ManyToManyField(related_name='articles', to='blog.categorymodel', verbose_name='دسته بندی'),
        ),
    ]
