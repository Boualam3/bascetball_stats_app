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
# Create your views here.




def home(request):
    teams = Team.objects.all()
    return render(request, template_name='pages/home.html', context={'teams': teams})


class TeamListView(ListView):
    model = Team
    template_name = 'pages/team_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):

        # pagination
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
    context_object_name = 'team'
    query_pk_and_slug = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_stats = context['team'].get_teamstats()
        context['team_stats'] = team_stats.get_stats_as_dict()
        teams_with_original_links = Team.objects.exclude(original_link__isnull=True).exclude(original_link__exact='')

        return context
    

def about_page(request):

     return render(request, template_name='pages/about.html')



def contact_page(request):
    if request.method == 'POST':
        contact = Contact()
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact.name = name
        contact.subject = subject
        contact.email = email
        contact.message = message
        contact.save()
        return redirect('contact')
    
    if request.method == 'GET':
        return render(request, template_name='pages/contact.html', context={'title': 'Contact us', "header_title": "contact us", "header_desc": "let’s stay in touch!", })