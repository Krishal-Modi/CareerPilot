from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_alter_jobapplication_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='source',
            field=models.CharField(blank=True, choices=[('linkedin', 'LinkedIn'), ('company_website', 'Company Website'), ('indeed', 'Indeed'), ('glassdoor', 'Glassdoor'), ('referral', 'Referral'), ('recruiter', 'Recruiter'), ('cold_email', 'Cold Email'), ('university', 'University Portal'), ('other', 'Other')], default='linkedin', max_length=30),
        ),
    ]