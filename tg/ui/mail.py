# encoding: utf-8

from __future__ import unicode_literals

import textwrap
import traceback

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
from django.utils.html import strip_tags

from core.models import Entry


def send_email_invitation():
    users = Entry.objects.filter(want_tg=False, num_issues=0).exclude(email='')

    # define the email template we want to send
    subject_template = '(Purring) Festskrift til Norsk Ordbok'
    body_template = textwrap.dedent('''
        <table style="width:100%"><td align=center style="text-align: center;"><table style="margin: 0 auto; text-align: left; width: 500px"><td>
        <p>Gode {{ user.printed_name }}!
        <p>&nbsp;

        <h3 style="margin: 0">Purring på subskripsjonsinnbyding</h3>
        <h1 style="margin: 0">Livet er æve, og evig er ordet</h1>
        <h2 style="margin: 0">Norsk Ordbok 1930–2016</h2>

        <p>I samband med utgjevinga av det tolvte og siste bandet av Norsk Ordbok, ynskjer prosjektorganisasjonen Norsk Ordbok 2014 og Det Norske Samlaget å gje ut eit festskrift. Festskriftet er tenkt som ein hyllest til det ordboksverket som blir det største vitskaplege og dokumenterande ordboksverket over norsk språk. Norsk Ordbok dekkjer både det norske folkemålet i bygd og by over heile landet og det nynorske skriftspråket. Både som språkdokumentasjon og som dokument over den norske kulturarven er Norsk Ordbok eit eineståande verk. Arbeidet med Norsk Ordbok starta alt i 1930, og papirutgåva er no i ferd med å bli fullført.
        <p>Festskriftet inneheld både kanoniske fagartiklar frå Norsk Ordboks historie, nye artiklar om den aktuelle stoda og framtidsperspektiva, biografiar over bidragsytarane til verket og bilete frå historia til ordboka.
        <p>Bidragsytarar i festskriftet er Kristin Bakken, Aina Basso, Marit Eikemo, Jon Fosse, Oddrun Grønvik, Alf Hellevik, Edvard Hoem, Christian-Emil Smith Ore, Sigmund Skard, Lars S. Vikør, Åse Wetås og Einar Økland. Dei tre underskrivne er redaktørar.

        <p style="text-align:center"><i>Oslo, oktober 2015</i>

        <p style="text-align:center; border-bottom: 1px dotted black; margin-bottom: 20px; padding-bottom: 20px;">Helene Urdland Karlsen · Lars S. Vikør · Åse Wetås
        <p>Redaksjonen vil invitere deg til å førehandstinge festskriftet, og samstundes få namnet ditt i Tabula gratulatoria. For å kunne stå på helsingslista, må du tinge minst eitt eksemplar av festskriftet til <b>kr 250,00</b> (pluss porto). Om du ynskjer det, kan du reservere deg mot å få namnet ditt i helsingslista, men likevel få tilsendt boka.

        <p>Du kan tinge skriftet på ein av desse måtane:<ol>
          <li>Send svarmelding per e-post til {email} eller ring +4722854380.
          <li>Send svar per brev til Det Norske Samlaget, Pb 4672 Sofienberg, 0506 Oslo. Merk brevet med «Festskrift til Norsk Ordbok».
          <li>Fyll ut eit elektronisk <a href='http://tg.s0.no/'>påmeldingsskjema</a>.
        </ol>

        <p><b>Ny tingingsfrist er <em style="color:red">5. desember 2015</em></b>.
        <p>Festskriftet skal etter planen liggje føre til lanseringa av band 12 den 9. mars 2016. Boka blir deretter send ut til tingarane med faktura vedlagd.
        </table>
        </table>
    '''.format(email=settings.EMAIL))
    plaintext_template = (
        strip_tags(body_template)
        .replace('skjema', 'skjema <http://tg.s0.no>')
        .replace('&nbsp', ''))

    # render and send the email
    for number, user in enumerate(users):
        print("[{n}/{t}]  {u}".format(n=number, t=len(users), u=user))
        ctx = Context({'user': user})
        subject = Template(subject_template).render(ctx)
        plain_body = Template(plaintext_template).render(ctx)
        html_body = Template(body_template).render(ctx)

        try:
            send_mail(
                subject, plain_body, settings.EMAIL,
                [user.email], html_message=html_body)
        except:
            traceback.print_exc(limit=1)
