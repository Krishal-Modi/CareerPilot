from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('applications', '0003_alter_jobapplication_date_applied'),
	]

	operations = [
		migrations.AlterField(
			model_name='jobapplication',
			name='job_url',
			field=models.CharField(blank=True, max_length=500),
		),
	]
