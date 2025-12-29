from pathlib import Path
import os,sys,requests,time

from datetime import datetime
from bs4 import BeautifulSoup
from django.utils.text import slugify
import pandas as pd


def scrap_main_table():
    response = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/turnovers-per-game/')
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'lxml')
        main = soup.find('main')

        table = main.find('table', class_='tr-table datatable scrollable')
        time.sleep(1)

        if table:
            thead = table.find('thead')
            header_row = thead.find('tr')
            columns = header_row.find_all('th')
            column_names = [column.text.strip() for column in columns] + ['More']
            table_data = []
            club_links = []
            rows = table.find_all('tr')

            for row in rows[1:] :
                columns = row.find_all('td')
                if len(columns) > 0:
                    clubs_data = [''] * 9
                    for idx,column in enumerate(columns):
                        link = ''
                        if idx == 1 : 
                            link_html = column.a
                            if link_html:
                                link = link_html['href']
                            club_links.append([column.text,link])
                            clubs_data[8] = link
                        clubs_data[idx] = column.text
                    table_data.append(clubs_data)

            df = pd.DataFrame(table_data,columns=column_names)
            output_dir = Path('data_stats')
            output_dir.mkdir(parents=True, exist_ok=True)
            file_path = output_dir / 'table_data.csv'
            df.to_csv(file_path, index=False)
            
            return df
        else:
            print("Table not found on the webpage.")
            return []
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return []




def scrap_details_page(url):
    response = requests.get(url)
    stats_dicts_of_data_frames={
        'PowerRatings':[],
        'KeyOffensiveStatsLS':[],
        'KeyDefensiveStatsLS':[],
        'ResultAndScheduleStats':[],
        'StatsDetailsFormattedHtml':''
        }
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        main_page = soup.find('div',class_="main-wrapper clearfix has-left-sidebar")
        time.sleep(1)
        aside = main_page.find('aside',class_='right-sidebar')

        tables_stats = aside.find_all('table',class_='tr-table')

        details_stats = main_page.find('table',class_='tr-table team-blockup')

        result_and_schedule_table = soup.find('table', class_="tr-table datatable scrollable")
        time.sleep(1)
        
        if details_stats :
            stats_dicts_of_data_frames['StatsDetailsFormattedHtml'] = str(details_stats)
        time.sleep(1)
        if len(details_stats):
            global data_frames
            data_frames = extract_data_from_tables(list_tables=tables_stats)

        if result_and_schedule_table :
            data_frame = extract_data_from_tables(table=result_and_schedule_table)
            # print(data_frame)
            data_frame = validate_and_sub_date_in_data_frame(data_frame)
            data_frames.append(data_frame)
            # print(data_frame)
        
        # assign data_frame to stats_dicts_of_data_frames 
        for idx, data_frame in enumerate(data_frames):
            if idx == 0:
                stats_dicts_of_data_frames['PowerRatings']=data_frame
            if idx == 1:
                stats_dicts_of_data_frames['KeyOffensiveStatsLS']=data_frame
            if idx == 2:
                stats_dicts_of_data_frames['KeyDefensiveStatsLS']=data_frame
            if idx == 3 :
                stats_dicts_of_data_frames['ResultAndScheduleStats']=data_frame
        return stats_dicts_of_data_frames


def validate_and_sub_date_in_data_frame(data_frame):
        current_year = datetime.now().year
        # convert the date strings to datetime objects using the current year
        data_frame["Date"] = pd.to_datetime(data_frame["Date"] + f"/{current_year}", format="%m/%d/%Y", errors="coerce")

        # check for invalid date formats (NaT represents invalid dates)
        invalid_dates = data_frame[data_frame["Date"].isna()]

        # filter out valid dates
        df_valid_dates = data_frame.dropna(subset=["Date"])
        
        return df_valid_dates

def extract_data_from_tables(table='',list_tables=[]):
    if len(table):
        tread = table.find('thead')
        header_row = tread.find('tr')
        columns = header_row.find_all('th')
        column_names = [column.text.strip() for column in columns] 
        
        table_data = []
        rows = table.find_all('tr')
        
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 0:
                rows_data = [] 
                for column in columns:
                    rows_data.append(column.text)
                
                table_data.append(rows_data)

        df = pd.DataFrame(table_data,columns=column_names)
        return df
    if len(list_tables):
        data_frames = []
        for idx,table_stat in enumerate(list_tables):
            tread = table_stat.find('thead')
            header_row = tread.find('tr')
            columns = header_row.find_all('th')
            # column_names = [column.text.strip() for column in columns] 
            table_data = []
            rows = table_stat.find_all('tr')
            
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 0:
                    clubs_data = [] 
                    for column in columns:
                        clubs_data.append(column.text)
                    
                    table_data.append(clubs_data)

            df = pd.DataFrame(table_data)
            data_frames.append(df)
        return data_frames
