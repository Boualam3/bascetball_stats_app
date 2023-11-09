from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import datetime
from django.core.exceptions import ValidationError


from .validators import validate_mmdd_date_format


class Team(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    team = models.CharField(max_length=100,blank=True, null=True)

    year_2023 = models.CharField(max_length=10,blank=True, null=True)
    last_3 = models.CharField(max_length=10,blank=True, null=True)
    last_1 = models.CharField(max_length=10,blank=True, null=True)
    home = models.CharField(max_length=10,blank=True, null=True)
    away = models.CharField(max_length=10,blank=True, null=True)
    year_2022 = models.CharField(max_length=10,blank=True, null=True)
    original_link = models.CharField(max_length=255,blank=True, null=True)
    

    def __str__(self) -> str:
        return self.team

    def get_absolute_url(self):
        return reverse('team-details',args=[str(self.id)])
    
    def get_teamstats(self):
        return self.team_stats.get()

class TeamStats(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE,related_name='team_stats')
    created_at = models.DateTimeField(auto_now_add=True)

    stats_details_formatted_html = models.TextField(blank=True,null=True)





class ResultAndScheduleStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='result_and_schedule_stats') 
    date = models.DateField(blank=True,null=True)
    opponent = models.CharField(max_length=100, blank=True, null=True)
    result = models.CharField(max_length=10, blank=True, null=True)  
    location = models.CharField(max_length=50, blank=True, null=True)
    win_loss = models.CharField(max_length=1, blank=True, null=True)  
    conference = models.CharField(max_length=100, blank=True, null=True)  
    spread = models.CharField(max_length=100,blank=True,null=True)
    total = models.CharField(max_length=100,blank=True,null=True)
    money = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self) -> str:
        return f'Result and Schedule For : {self.team}'

    def save(self, *args, **kwargs):
        # Add your custom date validation here
        try:
            date_obj = datetime.strptime(self.date, '%m/%d').replace(year=datetime.now().year)
            self.date = date_obj
        except ValueError:
            
            raise ValidationError("Enter a valid date in the 'mm/dd' format.")

        super(ResultAndScheduleStats, self).save(*args, **kwargs)



class PowerRatings(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='power_ratings')
    created_at = models.DateTimeField(auto_now_add=True)

    predictive_rating = models.CharField(max_length=50, help_text="Predictive Power Rating",blank=True, null=True)
    home_rating = models.CharField(max_length=50, help_text="Home Power Rating",blank=True, null=True)
    away_rating = models.CharField(max_length=50, help_text="Away Power Rating",blank=True, null=True)

    def __str__(self):
        return f'{self.team} power rating'
    

class KeyOffensiveStatsLS(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='key_offensive_stats')
    created_at = models.DateTimeField(auto_now_add=True)
    points_per_game = models.CharField(max_length=50, help_text="Points Per Game",blank=True, null=True)
    average_score_margin = models.CharField(max_length=50, help_text="Average Score Margin",blank=True, null=True)
    assists_per_game = models.CharField(max_length=50, help_text="Assists Per Game",blank=True, null=True)
    total_rebounds_per_game = models.CharField(max_length=50, help_text="Total Rebounds Per Game",blank=True, null=True)
    effective_fg_percentage = models.CharField(max_length=50, help_text="Effective FG Percentage",blank=True, null=True)
    offensive_rebound_percentage = models.CharField(max_length=50, help_text="Offensive Rebound Percentage",blank=True, null=True)
    free_throw_attempt_to_field_goal_attempt_ratio = models.CharField(max_length=50, help_text="Free Throw Attempt to Field Goal Attempt Ratio",blank=True, null=True)
    turnover_percentage = models.CharField(max_length=50, help_text="Turnover Percentage",blank=True, null=True)

    def __str__(self):
        return f'{self.team} key off stats LS' 
    

class KeyDefensiveStatsLS(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='key_defensive_stats')
    created_at = models.DateTimeField(auto_now_add=True)
    opponent_points_per_game = models.CharField(max_length=50, help_text="Opponent Points Per Game",blank=True, null=True)
    opponent_effective_fg_percentage = models.CharField(max_length=50, help_text="Opponent Effective FG Percentage",blank=True, null=True)
    offensive_rebounds_per_game = models.CharField(max_length=50, help_text="Offensive Rebounds Per Game",blank=True, null=True)
    defensive_rebounds_per_game = models.CharField(max_length=50, help_text="Defensive Rebounds Per Game",blank=True, null=True)
    blocks_per_game = models.CharField(max_length=50, help_text="Blocks Per Game",blank=True, null=True)
    steals_per_game = models.CharField(max_length=50, help_text="Steals Per Game",blank=True, null=True)
    personal_fouls_per_game = models.CharField(max_length=50, help_text="Personal Fouls Per Game",blank=True, null=True)

    def __str__(self):
        return f'{self.team} key def stats LS' 

class Contact(models.Model):
    name = models.CharField(max_length=158)
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_time = models.DateField()

    def __str__(self):
        return f'from {self.name}'
