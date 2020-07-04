''''''
from django.core.management.base import BaseCommand
from content.utils import download_all_words

class Command(BaseCommand):

    help = ''

    def handle(self, *args, **options):
        download_all_words()

