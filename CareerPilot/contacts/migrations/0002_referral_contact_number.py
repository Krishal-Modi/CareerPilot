from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='contact_number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]