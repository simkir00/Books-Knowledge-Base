import re

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.db.models import Q

from .models import Book, Author
from .forms import SearchForm


def index(request):
    n_books = Book.objects.all().count()
    n_authors = Author.objects.all().count()
    data = {"n_books": n_books,
            "n_authors": n_authors}
    return render(request, "firstapp/index.html", context=data)


def book_catalog(request):
    books = Book.objects.all()

    query = None
    q = Q()
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            words = query.split()
            for word in words:
                q |= Q(title__icontains=word) |\
                     Q(author__first_name__icontains=word) |\
                     Q(author__last_name__icontains=word)
            results = books.filter(q).distinct()

    data = {"res": results,
            "query": query,
            "books": books}

    return render(request, "firstapp/book_catalog.html", context=data)


def book_page(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Http404("<h1>There is no book with id={0}</h1>".format(id))
    data = {"book": book}
    return render(request, "firstapp/book_info.html", context=data)


def author_catalog(request):
    authors = Author.objects.all()
    data = {"authors": authors}
    return render(request, "firstapp/author_catalog.html", context=data)


def author_page(request, id):
    try:
        author = Author.objects.get(pk=id)
    except Author.DoesNotExist:
        return HttpResponse("<h1>Автора с id={0} не существует</h1>".format(id), status=404)
    books = Book.objects.filter(Q(author__first_name=author.first_name) & Q(author__last_name=author.last_name))
    data = {"author": author,
            "books": books}
    return render(request, "firstapp/author_info.html", context=data)


def search(request):
    books = Book.objects.all()

    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = books.filter(Q(name__icontains=query) |
                                   Q(author__first_name__icontains=query) |
                                   Q(author__first_name__icontains=query))
    data = {"res": results,
            "query": query}
    return render(request, "", context=data)
