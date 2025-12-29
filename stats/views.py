import os
import pandas as pd
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView
from .models import Team,TeamStats,Contact 
from django.contrib import messages
# from .tables import TeamTable
# Create your views here.




def home(request):
    # table = TeamTable(Team.objects.all())
    # table = Team.objects.all()
    return render(request, template_name='home.html')


class TeamListView(ListView):
    model = Team
    template_name = 'pages/team_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):

        context = super(TeamListView, self).get_context_data(**kwargs)

        team_list = Team.objects.all()
        paginator = Paginator(team_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            list_team_paginated = paginator.page(page)
        except PageNotAnInteger:
            list_team_paginated = paginator.page(1)
        except EmptyPage:
            list_team_paginated = paginator.page(paginator.num_pages)


        context['list_team'] = list_team_paginated
        context['query_search'] = self.request.GET.get('q') or ''

        current_group = (list_team_paginated.number - 1) // 10 + 1
        start_page = (current_group - 1) * 10 + 1
        end_page = min(current_group * 10, paginator.num_pages)

        # Set the page range for the template
        context['page_range'] = range(start_page, end_page + 1)
        return context
        
    def get_queryset(self):
        search = self.request.GET.get('q')
        # filtered_teams = []
        # if ',' in search:
        #     for team_name in search.split(','):
        #         filtered_teams.extend(
        #             Team.objects.filter(Q(team__icontains=team_name))
        #     )
        #     return filtered_teams

        if search is not None:
            return Team.objects.filter(
                Q(team__icontains=search) 
            )
        return Team.objects.all()

class TeamDetailView(DetailView):
    model = Team
    template_name = "pages/team_details.html"
    # template_name = "tables_tab.html"
    context_object_name = 'team'
    query_pk_and_slug = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = context['team']

        context['stats_details_formatted_html'] = team.team_stats.stats_details_formatted_html
        context['power_ratings_obj'] = team.power_ratings.all()
        context['key_offensive_stats_obj'] = team.key_offensive_stats.all()
        context['key_defensive_stats_obj'] = team.key_defensive_stats.all()
        context['result_and_schedule_stats_obj'] = team.result_and_schedule_stats.all()

        return context
    

def about_page(request):

     return render(request, template_name='pages/about.html')


def contact_page(request):
    if request.method == 'POST':
        # 1. Bot Prevention: Check Honeypot
        if request.POST.get('b_username'):
            # It's a bot. Divert them silently.
            return redirect('contact')

        # 2. Get Data
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # 3. Simple Validation & Save
        if name and email and message:
            Contact.objects.create(
                name=name,
                subject=subject,
                email=email,
                message=message
            )
            messages.success(
                request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    # GET Request logic
    context = {
        'title': 'Contact Us',
        'header_title': 'Contact Us',
        'header_desc': 'Let’s stay in touch!',
    }
    return render(request, 'pages/contact.html', context)
