from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('applications', '0001_initial'),
	]

	operations = [
		migrations.AlterField(
			model_name='jobapplication',
			name='status',
			field=models.CharField(
				choices=[
					('saved', 'Saved'),
					('applied', 'Applied'),
					('pending', 'Pending'),
					('assessment', 'Assessment'),
					('interview', 'Interviewed'),
					('accepted', 'Accepted'),
					('offer', 'Offer'),
					('rejected', 'Rejected'),
					('withdrawn', 'Withdrawn'),
				],
				default='saved',
				max_length=20,
			),
		),
	]