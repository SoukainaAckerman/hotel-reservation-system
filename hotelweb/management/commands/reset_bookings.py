from django.core.management.base import BaseCommand
from hotelweb.models import Booking
from signup.models import User

class Command(BaseCommand):
    help = 'Efface toutes les réservations et tous les utilisateurs sauf admin.'

    def handle(self, *args, **kwargs):
        Booking.objects.all().delete()
        User.objects.exclude(email='admin@tonsite.com').delete()  # Remplace par ton email admin si besoin
        self.stdout.write(self.style.SUCCESS('Toutes les réservations et utilisateurs (hors admin) ont été supprimés.'))
