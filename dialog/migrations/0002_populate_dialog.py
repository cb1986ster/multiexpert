from django.db import migrations, models

def stupid_dialog_data(apps, schema_editor):
    from dialog.models import Anwser, Statement

    ################################################################################
    ### Rozpoczęcia rozmowy
    ################################################################################
    main_entry = [
        Statement.objects.create( text = text, entry = True ) for text in [
            "Witaj!<br/>Z czym do mnie przychodzisz?",
            "Cześć!<br/>Jak mogę Ci pomóc?",
            "Siema!<br/>O czym pogadamy?",
        ]
    ]
    entry_goto = Anwser.objects.create(text = "[Rozpocznij nowy dialog]",goto = main_entry[0])
    ################################################################################
    ### Przejście do początku rozmowy
    ################################################################################
    z_tym_nie_pomoge = Statement.objects.create(text = "Z tym akurat nie pomoge :(")
    z_tym_nie_pomoge.anwsers.add(entry_goto)
    fajnie_ze_moglem_pomoc = Statement.objects.create(text="Cieszę się że mogłem pomóc :)")
    fajnie_goto = Anwser.objects.create(text="To wszystko, czego mi trzeba!",goto = fajnie_ze_moglem_pomoc)
    fajnie_ze_moglem_pomoc.anwsers.add(entry_goto)
    ################################################################################
    ### Gotowanie
    ################################################################################
    co_chcesz_ugotowac = Statement.objects.create(text = "Co chcesz ugotować?")
    co_chcesz_ugotowac_goto = Anwser.objects.create(
        text = "Chcę coś zrobić do jedzenia, ale nie wiem jak.",
        goto = co_chcesz_ugotowac
    )
    for entry in main_entry: entry.anwsers.add(co_chcesz_ugotowac_goto)
    gotowanie_czegos_innego_goto = Anwser.objects.create(text = "Chcę zrobić coś innego.",goto = co_chcesz_ugotowac)

    jak_zrobic_herbate = Statement.objects.create(text = "Aby zrobić herbatę potrzebujesz:<ul><li>Czajnik</li><li>Wodę</li><li>Szklankę</li><li>Wsad herbaciany</li></ul>Zagotuj wodę w czajniku, wsad umieść w szklance. Po zagotowaniu wody wlej wrzątek do szklanki. Uwżaj na, aby nie przekroczyć pojemność szklanki!")
    jak_zrobic_kanapke = Statement.objects.create(text = 'Serio? Zobacz:<br/><iframe width="560" height="315" src="https://www.youtube.com/embed/8nKt3LOx7nA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
    jak_zrobic_bimber  = Statement.objects.create(text = 'Serio? Zobacz:<br/><iframe width="560" height="315" src="https://www.youtube.com/embed/l0PLYoAM98o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
    co_chcesz_ugotowac.add_option("Herbatę",jak_zrobic_herbate)
    co_chcesz_ugotowac.add_option("Kanapkę",jak_zrobic_kanapke)
    co_chcesz_ugotowac.add_option("Bimber",jak_zrobic_bimber)
    co_chcesz_ugotowac.add_option("Marmolade",z_tym_nie_pomoge)
    co_chcesz_ugotowac.add_option("W sumie to nie wiem",z_tym_nie_pomoge)
    jak_zrobic_herbate.anwsers.add(gotowanie_czegos_innego_goto)
    jak_zrobic_kanapke.anwsers.add(gotowanie_czegos_innego_goto)
    jak_zrobic_bimber.anwsers.add(gotowanie_czegos_innego_goto)
    jak_zrobic_herbate.anwsers.add(fajnie_goto)
    jak_zrobic_kanapke.anwsers.add(fajnie_goto)
    jak_zrobic_bimber.anwsers.add(fajnie_goto)

    ################################################################################
    ### Programowanie
    ################################################################################
    co_chcesz_programowac = Statement.objects.create(text = "Co chcesz programować?")
    co_chcesz_programowac_goto = Anwser.objects.create(
        text = "Chce programować! Powiedz mi jak!",
        goto = co_chcesz_programowac
    )
    for entry in main_entry: entry.anwsers.add(co_chcesz_programowac_goto)
    programowanie_czegos_innego_goto = Anwser.objects.create(text = "Chcę zrobić coś innego.",goto = co_chcesz_programowac)

    jak_zrobic_strone_www = Statement.objects.create(text = 'Idź na kurs! Zobacz ten adres <a href="http://coderslab.pl" target="_blank">coderslab.pl</a>.')
    jak_to_wyglada        = Statement.objects.create(text = 'Nie jest lekko, zobacz:<br/><iframe width="560" height="315" src="https://www.youtube.com/embed/_q-l6Cn6WxY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')

    co_chcesz_programowac.add_option("Stronę WWW",jak_zrobic_strone_www)
    co_chcesz_programowac.add_option("W sumie czy to się opłaca? Jak to w ogóle wygląda?",jak_to_wyglada)
    co_chcesz_programowac.add_option("W sumie to nie wiem...",z_tym_nie_pomoge)

    jak_zrobic_strone_www.anwsers.add(programowanie_czegos_innego_goto)
    jak_to_wyglada.anwsers.add(programowanie_czegos_innego_goto)
    jak_zrobic_strone_www.anwsers.add(fajnie_goto)
    jak_to_wyglada.anwsers.add(fajnie_goto)

    ################################################################################
    ### Chcę posłuchać muzyki
    ################################################################################
    muzyka = Statement.objects.create(text = "Co masz ochotę posłuchać?")
    muzyka_goto = Anwser.objects.create(
        text = "Włącz jakąś muzykę",
        goto = muzyka
    )
    for entry in main_entry: entry.anwsers.add(muzyka_goto)
    muzyka_cos_innego_goto = Anwser.objects.create(text = "Chcę posłuchać coś innego.",goto = muzyka)

    opcje_muzyki = {
        'Puść Moonspela': 'https://www.youtube.com/watch?v=FvFwzWLJJHc&list=PLnqoM9PUg_fT5q8UtrhJpyY9u2g4yiunL&index=1',
        'Mam ochotę posłuchać Maji Kleszcz':  'https://www.youtube.com/watch?v=XUIg6-Qd_Mw&list=RDEMCssGsuaojm42cDu1E6ofLQ&start_radio=1',
        'To może Kult': 'https://www.youtube.com/watch?v=a0vXhwYDfOA&list=RDoE9CFBFUP9Q&index=3',
        'Mam ochotę na KSU': 'https://www.youtube.com/watch?v=4-T03gG2CDQ&list=PLOlFuIptLeWbRffnrJtbbCFAgS9wPzV7Q'
    }
    to_jeszcze_gotowanie_goto = Anwser.objects.create(text = "To teraz powiedz mi jeszcze jak coś ugotować",goto = co_chcesz_ugotowac)

    for opcja_tekst, link in opcje_muzyki.items():
        zdanie = Statement.objects.create(text = 'Zobacz tę playlistę <a href="{}" target="_blank">{}</a>.'.format(link,link))
        zdanie.anwsers.add(to_jeszcze_gotowanie_goto)
        zdanie.anwsers.add(muzyka_cos_innego_goto)
        zdanie.anwsers.add(fajnie_goto)
        muzyka.add_option(opcja_tekst,zdanie)

    muzyka.add_option("DiscoPolo na maksiora!",z_tym_nie_pomoge)


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(stupid_dialog_data)
    ]
