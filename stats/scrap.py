import os,sys,requests,time
from bs4 import BeautifulSoup
import pandas as pd


def scrap_main_table():
    response = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/turnovers-per-game/')
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
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

            df.to_csv('data_stats/table_data.csv', index=False)
            
            return df
        else:
            print("Table not found on the webpage.")
            return []
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return []


def scrap_details_page(url):
    response = requests.get(url)
    data_frames = []
    all_columns_names = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_page = soup.find('div',class_="main-wrapper clearfix has-left-sidebar")
        aside = main_page.find('aside',class_='right-sidebar')
        tables_stats = aside.find_all('table',class_='tr-table')
        time.sleep(1)
        for idx,table_stat in enumerate(tables_stats):
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
            
            #we remove header (,columns=column_names) it make thing hard to use
            df = pd.DataFrame(table_data)
            data_frames.append(df)
            
            # we csv just for testing purposes
            df.to_csv(f'data_stats/others_stats_{idx}.csv', index=False)

        combined_df = pd.concat(data_frames, axis=0)
        # reset columns indexes
        combined_df = combined_df.reset_index(drop=True)

        return combined_df


# p = scrap_details_page('https://www.teamrankings.com/ncaa-basketball/team/virginia-cavaliers')
# print(p)