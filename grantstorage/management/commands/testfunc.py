from django.core.management.base import BaseCommand, CommandError
from grantstorage.storage.mongo.mongostorage import MongoStorage


class Command(BaseCommand):
    help = 'Test some functionality'

    def handle(self, *args, **options):
        ms = MongoStorage()

        # grants = ms.find_grant_by_group('plgglaoisi')
        # for g in grants:
        #     print(GrantSerializer(g).data)

        print(ms.find_user_by_login('plgpawlik'))
