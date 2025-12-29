import os
from pathlib import Path
from django.core.management.base import BaseCommand
from stats.utils import create_teams_objects
from stats.scrap import scrap_main_table


# TODO here we invoke the scrap method , should return DataFrame , then we invoke another method that take the DataFrame and create bulk objects  , this for first time when we wan to deploy
class Command(BaseCommand):
    help = 'first Scrap than populates data in database '

    def handle(self, *args, **options):
        print('Populating the database...')
        
        data_frame = scrap_main_table()
        # print(data_frame)
        create_teams_objects(data_frame)
        
        
        

