from django.core.management.base import BaseCommand
from minibadge.models import Award, Badge
from google_spreadsheet.api import SpreadsheetAPI
import os

class Command(BaseCommand):
  args = '<one>'
  help = 'Load badge award submissions'

  def handle(self, *args, **options):
    client = SpreadsheetAPI(os.environ["EMAIL"], os.environ["PASS"], "yrsbadger")

    worksheet = client.get_worksheet("0Ar9L6jllB7SPdFd3Y0lBMDdOODM1aFNJUUJ6Zy1DbkE", 1)

    for row in worksheet.get_rows():
      # find the badge
      badge = Badge.objects.filter(title=row["title"])
      if not len(badge):
        print "Could not find badge [%s]" % row["title"]
        continue
      badge = badge[0]

      # check if there's not already been one for this user
      award = Award.objects.filter(badge=badge, email=row["email"])
      if len(award):
        print "Already send award for %s to %s" % (badge, row["email"])
        continue
      award = Award.objects.create(badge=badge, email=row["email"])
      award.save()
      # TODO: send the email
