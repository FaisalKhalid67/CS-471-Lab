from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Student, Address 

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, "bookmodule/list_books.html")

def one_book(request):
    return render(request, "bookmodule/one_book.html")

def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def html5_links(request):
    return render(request, "bookmodule/html5_links.html")

def html5_text_formatting(request):
    return render(request, "bookmodule/html5_text_formatting.html")

def html5_listing(request):
    return render(request, "bookmodule/html5_listing.html")

def html5_tables(request):
    return render(request, "bookmodule/html5_tables.html")

def search(request):
    # If the form is submitted
    if request.method == "POST":
        string = (request.POST.get("keyword") or "").lower()
        isTitle = request.POST.get("option1")   # checkbox: None or "on"
        isAuthor = request.POST.get("option2")  # checkbox: None or "on"

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item["title"].lower():
                contained = True

            if not contained and isAuthor and string in item["author"].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, "bookmodule/bookList.html", {"books": newBooks})

    # Otherwise (GET) show the form page again
    return render(request, "bookmodule/search.html")

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains="and")  # multiple objects
    return render(request, "bookmodule/bookList.html", {"books": mybooks})

def complex_query(request):
    mybooks = (
        Book.objects
        .filter(author__isnull=False)
        .filter(title__icontains="and")
        .filter(edition__gte=2)
        .exclude(price__lte=100)[:10]
    )

    if len(mybooks) >= 1:
        return render(request, "bookmodule/bookList.html", {"books": mybooks})
    else:
        return render(request, "bookmodule/index.html")
    
def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, "bookmodule/bookList.html", {"books": books})

def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains="qu") | Q(author__icontains="qu"))
    )
    return render(request, "bookmodule/bookList.html", {"books": books})

def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & ~(Q(title__icontains="qu") | Q(author__icontains="qu"))
    )
    return render(request, "bookmodule/bookList.html", {"books": books})

def lab8_task4(request):
    books = Book.objects.all().order_by("title")
    return render(request, "bookmodule/bookList.html", {"books": books})

def lab8_task5(request):
    stats = Book.objects.aggregate(
        total_books=Count("id"),
        total_price=Sum("price"),
        avg_price=Avg("price"),
        max_price=Max("price"),
        min_price=Min("price"),
    )
    return render(request, "bookmodule/bookStats.html", {"stats": stats})

def lab8_task7(request):
    # produces rows like: {"city": "Riyadh", "num_students": 5}
    rows = (
        Address.objects
        .values("city")
        .annotate(num_students=Count("students"))
        .order_by("city")
    )
    return render(request, "bookmodule/studentsByCity.html", {"rows": rows})