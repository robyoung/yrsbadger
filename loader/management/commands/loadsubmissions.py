from django.core.management.base import BaseCommand
from minibadge.models import Award, Badge
from google_spreadsheet.api import SpreadsheetAPI
import os

class Command(BaseCommand):
  args = '<one>'
  help = 'Load badge award submissions'

  def handle(self, *args, **options):
    client = SpreadsheetAPI(os.environ["EMAIL"], os.environ["PASS"], "yrsbadger")

    worksheet = client.get_worksheet("0AuaHiEjutiMUdE5SWTNvTUJTdlJ1ZXV3dUxoQkh6SGc", 1)

    for row in worksheet.get_rows():
      for title in map(str.strip, row["badgestoaward"].split(",")):
        try:
          badge = Badge.objects.get(title=title)
          if not row["youngpersonsemailaddress"]:
            print("ERROR: No email address")
          elif not Award.objects.filter(badge=badge, email=row["youngpersonsemailaddress"]):
            award = Award.objects.create(badge=badge, email=row["youngpersonsemailaddress"])
            award.save()
            award.send()
        except Badge.DoesNotExist:
          print("ERROR: Badge does not exist [%s] for %s" % (title, row["youngpersonsemailaddress"]))