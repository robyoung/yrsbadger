from django.core.management.base import BaseCommand
from minibadge.models import Award

class Command(BaseCommand):
  args = '<email> <email> ...'
  help = 'Load badge award submissions'

  def handle(self, *emails, **options):
    for email in emails:
      print "Sending awards for %s" % email
      for award in Award.objects.filter(email=email):
        award.send()
        print "  %s sent" % award.badge.title
