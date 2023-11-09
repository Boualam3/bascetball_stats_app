from django.contrib import admin
from .models import Team,TeamStats ,PowerRatings,KeyOffensiveStatsLS,KeyDefensiveStatsLS,ResultAndScheduleStats

# Register your models here.

admin.site.register(Team)
admin.site.register(ResultAndScheduleStats)
admin.site.register(TeamStats)
admin.site.register(PowerRatings)
admin.site.register(KeyOffensiveStatsLS)
admin.site.register(KeyDefensiveStatsLS)