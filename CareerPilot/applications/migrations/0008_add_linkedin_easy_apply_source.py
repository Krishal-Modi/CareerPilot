from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_jobapplication_source_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='source',
            field=models.CharField(
                blank=True,
                choices=[
                    ('linkedin', 'LinkedIn'),
                    ('linkedin_easy_apply', 'LinkedIn Easy Apply'),
                    ('company_website', 'Company Website'),
                    ('indeed', 'Indeed'),
                    ('glassdoor', 'Glassdoor'),
                    ('referral', 'Referral'),
                    ('recruiter', 'Recruiter'),
                    ('cold_email', 'Cold Email'),
                    ('university', 'University Portal'),
                    ('other', 'Other'),
                ],
                default='linkedin',
                max_length=30,
            ),
        ),
    ]
