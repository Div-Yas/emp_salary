# Generated by Django 4.1.1 on 2022-12-03 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emp_App', '0003_alter_user_emp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='emp_id',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
