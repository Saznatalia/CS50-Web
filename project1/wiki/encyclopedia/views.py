from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    title = util.get_entry(title)

    # If entry doesn't exist returns error page
    if title == None:
            return render(request, "encyclopedia/error.html")

    # If entry exists return presents entry's page 
    return render(request, "encyclopedia/title.html", {
        "title": markdown2.markdown(title)
    })


def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    entries_lower = []
    results = []
    for entry in entries:
        entries_lower.append(entry.lower())   
    # Redirect to existing entry page if query is same as existing entry
    if query in entries_lower:
        return HttpResponseRedirect(reverse("encyclopedia:title", args=(query,)))
    # Check if query is sub-string of entries
    for entry in entries_lower:
        if query in entry:
            results.append(entry)
    # If nothing was found return not found page
    if results == []:
        return render(request, "encyclopedia/not_found.html")
    # Return list of possible results, i.e. search result page
    return render(request, "encyclopedia/search.html", {
        "results": results
    })
