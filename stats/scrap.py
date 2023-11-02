import os,requests,time
from bs4 import BeautifulSoup
import pandas as pd



# Send a GET request to the webpage
response = requests.get('https://www.teamrankings.com/ncaa-basketball/stat/turnovers-per-game/')

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    main = soup.find('main')
    # time.sleep(1)
    # print(main)
    # with open('soup.html','w' ,encoding='utf-8') as file :
    #     file.write(f'{main}')


    # print(wrapper)
    table = main.find('table', class_='tr-table datatable scrollable')
    time.sleep(1)
    # print(table)
    # Check if the table was found
    if table:

        thead = table.find('thead')
        header_row = thead.find('tr')
        columns = header_row.find_all('th')
        column_names = [column.text.strip() for column in columns]
        # Extract the table data and convert it into a pandas DataFrame
        table_data = []
        club_links = []
        rows = table.find_all('tr')

        for row in rows[1:] :
            columns = row.find_all('td')
            if len(columns) > 0:
                clubs_data = []
                for idx,column in enumerate(columns) :
                    if idx == 1 : 
                        print(column)
                        link_html = column.a
                        if link_html :
                            link = link_html.get('href')
                        club_links.append({'name':column.text.lower(),'link':link or ''})
                    clubs_data.append(column.text) 
                
                table_data.append(clubs_data)

        df = pd.DataFrame(table_data,columns=column_names)

        # Save the DataFrame to a CSV file
        df.to_csv('table_data.csv', index=False)
        print(club_links)
    else:
        print("Table not found on the webpage.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)