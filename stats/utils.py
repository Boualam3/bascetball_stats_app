import os,sys,sqlite3
from django.utils.text import slugify
import pandas as pd
from django.conf import settings
from .models import Team, TeamStats

connection = sqlite3.connect(os.path.join(settings.BASE_DIR,'db.sqlite3'))

def create_teams_objects(data_frame=[]):
     if not len(data_frame) : 
          csv_file_path = os.path.join(settings.BASE_DIR,'data_stats/table_data.csv')  
          data = pd.read_csv(csv_file_path)

          data_frame = data.where(pd.notnull(data), None)
     team_list = []
     for _, row in data_frame.iterrows():
          rank  = str(row['Rank'])
          team  = str(row['Team'])
          year_2022  = str(row['2022'])
          last_3  = str(row['Last 3'])
          last_1  = str(row['Last 1'])
          home  = str(row['Home'])
          away = str(row['Away'])
          year_2021  = str(row['2021'])
          original_link = str(row['More'])
          team_obj = Team(
               rank=rank,
               team=team,
               year_2022=year_2022,
               last_3=last_3,
               last_1=last_1,
               home=home,
               away=away,
               year_2021=year_2021,
               original_link=original_link
          )
          team_list.append(team_obj)
     Team.objects.bulk_create(team_list)



def create_team_stats_objects(team_id,data_frame):
     if data_frame is None:
          return
     # data_frame.to_sql('teamstats',connection, if_exists="replace", index=False)
     # connection.commit()
     # connection.close()


     column_mapping = {
          'predictive': 'predictive_rating',
          'home': 'home_rating',
          'away': 'away_rating',
          'pointsgame': 'points_per_game',
          'avg-score-margin': 'average_score_margin',
          'assistsgame': 'assists_per_game',
          'total-reboundsgm': 'total_rebounds_per_game',
          'effective-fg': 'effective_fg_percentage',
          'off-rebound': 'offensive_rebound_percentage',
          'ftafga': 'free_throw_attempt_to_field_goal_attempt_ratio',
          'turnover': 'turnover_percentage',
          'opp-pointsgame': 'opponent_points_per_game',
          'opp-effective-fg': 'opponent_effective_fg_percentage',
          'off-reboundsgm': 'offensive_rebounds_per_game',
          'def-reboundsgm': 'defensive_rebounds_per_game',
          'blocksgame': 'blocks_per_game',
          'stealsgame': 'steals_per_game',
          'personal-foulsgm': 'personal_fouls_per_game',
     }
     team_stats = TeamStats(team_id=team_id)
     for _,row in data_frame.iterrows():
          slug = slugify(row[0])
          field_name = column_mapping[slug]
          print(f'{field_name} : {row[1]}')
          setattr(team_stats,field_name , str(row[1]))
     team_stats.save()





def get_team_ids_and_links()-> list[dict]:
     teams_with_original_links = Team.objects.exclude(original_link__isnull=True).exclude(original_link__exact='')

     original_links_with_ids = []

     for team in teams_with_original_links:
          original_links_with_ids.append({'id': team.id, 'link': team.original_link or ''})
     
     return original_links_with_ids



"""
[       Rating Points Above Avg.
0  Predictive              11.8
1        Home                --
2        Away                --,                 Stat  Value
0        Points/Game   67.8
1   Avg Score Margin   +7.3
2       Assists/Game   15.7
3  Total Rebounds/Gm   32.2
4     Effective FG %  51.2%
5      Off Rebound %  23.7%
6            FTA/FGA  0.347
7         Turnover %  12.0%,                  Stat  Value
0     Opp Points/Game   60.5
1  Opp Effective FG %  48.3%
2     Off Rebounds/Gm    7.0
3     Def Rebounds/Gm   22.7
4         Blocks/Game    4.3
5         Steals/Game    6.8
6   Personal Fouls/Gm   14.3]

"""
