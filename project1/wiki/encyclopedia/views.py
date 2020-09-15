from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpRequest
from django import forms

from . import util
import markdown2
import random

# Form For New Page
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': "title"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class':'content'}))

# Home Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page
def entry(request, title):
    entry = util.get_entry(title)

    # If entry doesn't exist returns error page
    if entry == None:
            return render(request, "encyclopedia/error.html")

    # Check if method is POST
    if request.method == "POST":
        updated_content = request.POST.get('textarea')
        print(updated_content)

        # If updated save updated entry to disk
        updated_entry = util.save_entry(title, updated_content)

        # Display updated entry page to user
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))

    # If entry exists return presents entry's page 
    return render(request, "encyclopedia/title.html", {
        "entry": markdown2.markdown(entry),
        "title": title
    })

# Search
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

# New Page
def new_page(request):

    # List of existing entries in lower case
    entries = util.list_entries()
    entries_lower = []
    for entry in entries:
        entries_lower.append(entry.lower())

    # Check if method is POST
    if request.method == "POST":
        
        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            # Isolate the title and content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            # If entry already exists display error with link to existing entry
            if title.lower() in entries_lower:
                return render(request, "encyclopedia/already_exists.html", {
                    "title": title.lower()
                })

            # If it doesn't exists then save new entry to disk
            new_entry = util.save_entry(title, content)

            # Display new entry page to user
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    # If method is GET present new page form to user
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

# Edit Page
def edit_page(request, title):
    entry = util.get_entry(title)

    # If entry doesn't exist returns error page
    if entry == None:
            return render(request, "encyclopedia/error.html")
    
    # Present edit page form to user
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "entry": entry
    })

# Random Page
def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    random_entry = util.get_entry(random_title)

    # Return page with random entry
    return render(request, "encyclopedia/random.html", {
        "random_entry": markdown2.markdown(random_entry),
        "title": random_title
    })

