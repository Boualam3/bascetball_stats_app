# Basketball Stats Tracker

A personal portfolio project that automates the collection and display of basketball statistics. It scrapes data daily, processes it with Pandas, and organizes everything into a clean, team-based web interface.

## How it Works
1. **Scraping:** Custom Python scripts (using BeautifulSoup) fetch raw HTML tables from third-party sports sites.
2. **Data Processing:** Pandas cleans the raw data, handles date formatting, and filters out unnecessary metrics to focus on "only the data that matters."
3. **Storage:** The processed data is mapped to Django models (Teams, Power Ratings, Offense/Defense stats).
4. **Display:** A responsive Django frontend allows users to navigate stats by team with smooth scroll animations.

## Tech Stack
* **Language:** Python
* **Web Framework:** Django
* **Data Tools:** Pandas, BeautifulSoup4
* **Frontend:** Bootstrap 5, JavaScript



## Project Structure
* `scrap_teams`: Management command to initialize the team list.
* `scrap_stats`: Management command to fetch detailed offensive/defensive data for each team.
* `models.py`: Relational database structure designed for fast scouting and lookup.

## Screenshots

### 1. Home (Hero)
The landing page.
![Hero Section](/bascetball_stats_app/bascetball_stat/static/assests/hero-screenshot.png)

### 2. Team Rankings (Table Listing)
The main table showing the overall classification of teams after the daily scrape.
![Team Rankings](/bascetball_stats_app/bascetball_stat/static/assests/table-screenshot.png)

### 3. Team Insights (Specific Stats)
Detailed view for a single team, including Power Ratings and Offensive/Defensive metrics.
![Team Stats](/bascetball_stats_app/bascetball_stat/static/assests/stats-screenshot.png)

## Setup
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py scrap_teams` (To get the ranking list)
4. `python manage.py scrap_stats` (To get details for each team)
5. `python manage.py runserver`