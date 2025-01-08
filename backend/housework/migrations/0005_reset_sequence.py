from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('housework', '0004_alter_contributor_name'),
    ]

    operations = [
        migrations.RunSQL(
            """
            SELECT setval(pg_get_serial_sequence('"housework_houseworkrecord"','id'), 
                (SELECT MAX(id) FROM "housework_houseworkrecord")+1);
            """
        )
    ]
