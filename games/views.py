from django.db import models
from django.shortcuts import render
from django.views import View

from django.http import HttpResponseRedirect

from .models import the2048

import datetime

class the2048View(View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'games/2048.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        if request.is_ajax:
            data = request.POST
            moves = data["moves"]
            highestTile = data["highestTile"]
            score = data["score"]
            startTime = data["startTime"]
            endTime = data["endTime"]
            time_start = datetime.datetime.fromtimestamp(int(startTime))
            time_end = datetime.datetime.fromtimestamp(int(endTime))
            time_delta = time_end - time_start
            seconds_in_day = 24 * 60 * 60
            duration_tuple = divmod(time_delta.days * seconds_in_day + time_delta.seconds, 60)
            duration_name = str(duration_tuple[0]) + " min " + str(duration_tuple[1]) + " seconds"
            duration = duration_tuple[0]*60 + duration_tuple[1]
            var = the2048.objects.create(user=request.user, moves=moves, highest_tile=highestTile, score=score, time_start=time_start, time_end=time_end, duration=duration, duration_name=duration_name)

       
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class the2048Leaderboard(View):
    def get(self, request, *args, **kwargs):
        context = {}
        results = the2048.objects.all()
        context["results"] = results
        return render(request, 'games/2048_leaderboard.html', context)