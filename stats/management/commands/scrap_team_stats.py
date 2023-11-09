import os
from pathlib import Path
from django.core.management.base import BaseCommand
from stats.utils import create_teams_objects,create_team_stats_objects,get_team_ids_and_links
from stats.scrap import scrap_main_table , scrap_details_page



class Command(BaseCommand):
    help = 'Scrap every team details stats'

    def handle(self, *args, **options):
        teams_link_details = get_team_ids_and_links()
        for idx,data in enumerate(teams_link_details):
            id = data['id']
            link = data['link']
            dicts_of_data_frame = scrap_details_page(link)
            # print(dicts_of_data_frame)
            if link and id :
                print('Here we go ')

                p = create_team_stats_objects(id,dicts_of_data_frame)
                # print(p)
            if idx == 1 :
                break