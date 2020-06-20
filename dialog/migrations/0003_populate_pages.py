from django.db import migrations, models

def pages_data(apps, schema_editor):
    from dialog.models import Page
    Page.objects.create(
        title = "Co to jest?",
        type = "help",
        slug = "co-to-jest",
        text = """To jest jaka strona co ma udawać, że z Tobą rozmaiwa :)"""
    )
    Page.objects.create(
        title = "Jak to działa?",
        type = "help",
        slug = "jak-dziala",
        text = """Działanie jet bardzo proste i opiera się na prostym grafie rozmowy :)"""
    )


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0002_populate_dialog'),
    ]

    operations = [
        migrations.RunPython(pages_data)
    ]
