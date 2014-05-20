from django.http import HttpResponse
from django.shortcuts import render



def corpus_overview(request, corpus_name):
    # Add list of Documents/Utterances to corpus_overview
    return HttpResponse(corpus_name)


def home(request):
    # TODO: Add list of current corpora to homepage
    return render(request, "home.html")
