import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.teamrankings.com/ncaa-basketball/team/virginia-cavaliers')

# Sample HTML content containing the table
html_content = """
<table class="tr-table team-blockup">
    <tbody>
        <tr>
            <td class="top" colspan="3">1st Place, ACC (0-0 Conf)</td>
        </tr>
        <tr class="team-blockup-data">
            <td>
                <div>
                    <h4>Record</h4>
                    <p>0-0</p>
                </div>
            </td>
            <td>
                <div>
                    <h4>Predictive rank</h4>
                    <p><span>#42</span></p>
                </div>
            </td>
            <td>
                <div>
                    <h4>Streak</h4>
                    <p>--</p>
                </div>
            </td>
        </tr>
    </tbody>
</table>
"""

# Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# # Find the table element by its class
# table = soup.find('table', class_='tr-table team-blockup')

# # Extract data from the table
# data = {}
# rows = table.find_all('tr', class_='team-blockup-data')

# for row in rows:
#     cells = row.find_all('td')
#     data[cells[0].find('h4').get_text()] = cells[0].find('p').get_text()
#     data[cells[1].find('h4').get_text()] = cells[1].find('p').find('span').get_text()
#     data[cells[2].find('h4').get_text()] = cells[2].find('p').get_text()

# print(data)

# table = soup.find('table', {'id': 'DataTables_Table_0'})

# # Extract data from the table rows
# for row in table.find_all('tr'):
#     # Extract data from each cell in the row
#     cells = row.find_all('td')
#     if len(cells) > 0:
#         date = cells[0].text.strip()
#         opponent = cells[1].text.strip()
#         result = cells[2].text.strip()
#         spread = cells[6].text.strip()
#         total = cells[7].text.strip()
#         money = cells[8].text.strip()

#         # Print the extracted data
#         print(f"Date: {date}, Opponent: {opponent}, Result: {result}, Spread: {spread}, Total: {total}, Money: {money}")


from datetime import datetime

def convert_date_string(date_str):
    try:
        # Get the current year
        default_year = datetime.now().year

        # Split the date string into month and day
        month, day = map(int, date_str.split('/'))

        # Create a datetime object with the current year, month, and day
        converted_date = datetime(default_year, month, day)
        return converted_date

    except ValueError:
        # Handle any potential errors in date format
        return None

# Example usage:
date_str = "11/29"

converted_date = convert_date_string(date_str)
if converted_date:
    print(f"Converted Date: {converted_date}")
else:
    print("Invalid date format")