from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Team(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    team = models.CharField(max_length=100,blank=True, null=True)

    year_2022 = models.CharField(max_length=10,blank=True, null=True)
    last_3 = models.CharField(max_length=10,blank=True, null=True)
    last_1 = models.CharField(max_length=10,blank=True, null=True)
    home = models.CharField(max_length=10,blank=True, null=True)
    away = models.CharField(max_length=10,blank=True, null=True)
    year_2021 = models.CharField(max_length=10,blank=True, null=True)
    original_link = models.CharField(max_length=255,blank=True, null=True)
    

    def __str__(self) -> str:
        return self.team

    def get_absolute_url(self):
        return reverse('team-details',args=[str(self.id)])
    
    def get_teamstats(self):
        return self.team_stats.get()

class TeamStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='team_stats')
    created_at = models.DateTimeField(auto_now_add=True)

    # Power Ratings
    predictive_rating = models.CharField(max_length=50, help_text="Predictive Power Rating",blank=True, null=True)
    home_rating = models.CharField(max_length=50, help_text="Home Power Rating",blank=True, null=True)
    away_rating = models.CharField(max_length=50, help_text="Away Power Rating",blank=True, null=True)

    # Key Offensive Stats (Last Season)
    points_per_game = models.CharField(max_length=50, help_text="Points Per Game",blank=True, null=True)
    average_score_margin = models.CharField(max_length=50, help_text="Average Score Margin",blank=True, null=True)
    assists_per_game = models.CharField(max_length=50, help_text="Assists Per Game",blank=True, null=True)
    total_rebounds_per_game = models.CharField(max_length=50, help_text="Total Rebounds Per Game",blank=True, null=True)
    effective_fg_percentage = models.CharField(max_length=50, help_text="Effective FG Percentage",blank=True, null=True)
    offensive_rebound_percentage = models.CharField(max_length=50, help_text="Offensive Rebound Percentage",blank=True, null=True)
    free_throw_attempt_to_field_goal_attempt_ratio = models.CharField(max_length=50, help_text="Free Throw Attempt to Field Goal Attempt Ratio",blank=True, null=True)
    turnover_percentage = models.CharField(max_length=50, help_text="Turnover Percentage",blank=True, null=True)

    # Key Defensive Stats (Last Season)
    opponent_points_per_game = models.CharField(max_length=50, help_text="Opponent Points Per Game",blank=True, null=True)
    opponent_effective_fg_percentage = models.CharField(max_length=50, help_text="Opponent Effective FG Percentage",blank=True, null=True)
    offensive_rebounds_per_game = models.CharField(max_length=50, help_text="Offensive Rebounds Per Game",blank=True, null=True)
    defensive_rebounds_per_game = models.CharField(max_length=50, help_text="Defensive Rebounds Per Game",blank=True, null=True)
    blocks_per_game = models.CharField(max_length=50, help_text="Blocks Per Game",blank=True, null=True)
    steals_per_game = models.CharField(max_length=50, help_text="Steals Per Game",blank=True, null=True)
    personal_fouls_per_game = models.CharField(max_length=50, help_text="Personal Fouls Per Game",blank=True, null=True)

    def __str__(self):
        return f"Stats for {self.team.team}"

    def get_stats_as_dict(self):
        return {
            "PowerRatings": {
                "Predictive": self.predictive_rating,
                "Home": self.home_rating,
                "Away": self.away_rating
            },
            "KeyOffensiveStatsLS": {
                "Points Per Game": self.points_per_game,
                "Average Score Margin": self.average_score_margin,
                "Assists Per Game": self.assists_per_game,
                "Total Rebounds Per Game": self.total_rebounds_per_game,
                "Effective FG Percentage": self.effective_fg_percentage,
                "Offensive Rebound Percentage": self.offensive_rebound_percentage,
                "Free Throw Attempt to Field Goal Attempt Ratio": self.free_throw_attempt_to_field_goal_attempt_ratio,
                "Turnover Percentage": self.turnover_percentage
            },
            "KeyDefensiveStatsLastS": {
                "Opponent Points Per Game": self.opponent_points_per_game,
                "Opponent Effective FG Percentage": self.opponent_effective_fg_percentage,
                "Offensive Rebounds Per Game": self.offensive_rebounds_per_game,
                "Defensive Rebounds Per Game": self.defensive_rebounds_per_game,
                "Blocks Per Game": self.blocks_per_game,
                "Steals Per Game": self.steals_per_game,
                "Personal Fouls Per Game": self.personal_fouls_per_game
            }
        }


class Contact(models.Model):
    name = models.CharField(max_length=158)
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_time = models.DateField()

    def __str__(self):
        return f'from {self.name}'
