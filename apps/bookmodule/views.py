from django.shortcuts import render
from django.db.models import Q, F, Count, Sum, Avg, Min, Max, FloatField
from django.db.models.functions import Cast
from .models import Book9, Publisher9
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

def lab9_task1(request):
    total_qty = Book9.objects.aggregate(total=Sum("quantity"))["total"] or 0

    if total_qty == 0:
        books = Book9.objects.none()
    else:
        books = Book9.objects.annotate(
            availability=Cast(F("quantity"), FloatField()) * 100.0 / float(total_qty)
        ).order_by("title")

    return render(request, "bookmodule/lab9_task1.html", {"books": books, "total_qty": total_qty})

def lab9_task2(request):
    pubs = Publisher9.objects.annotate(
        total_stock=Sum("book9__quantity")
    ).order_by("name")

    return render(request, "bookmodule/lab9_task2.html", {"pubs": pubs})

def lab9_task3(request):
    pubs = Publisher9.objects.annotate(
        oldest_pubdate=Min("book9__pubdate")
    ).order_by("name")

    return render(request, "bookmodule/lab9_task3.html", {"pubs": pubs})

def lab9_task4(request):
    pubs = Publisher9.objects.annotate(
        avg_price=Avg("book9__price"),
        min_price=Min("book9__price"),
        max_price=Max("book9__price"),
    ).order_by("name")

    return render(request, "bookmodule/lab9_task4.html", {"pubs": pubs})

def lab9_task5(request):
    pubs = Publisher9.objects.annotate(
        high_rated_count=Count("book9", filter=Q(book9__rating__gte=4))
    ).order_by("-high_rated_count", "name")

    return render(request, "bookmodule/lab9_task5.html", {"pubs": pubs})

def lab9_task6(request):
    cond = Q(book9__price__gt=50) & Q(book9__quantity__lt=5) & Q(book9__quantity__gte=1)

    pubs = Publisher9.objects.annotate(
        filtered_books_count=Count("book9", filter=cond)
    ).order_by("-filtered_books_count", "name")

    return render(request, "bookmodule/lab9_task6.html", {"pubs": pubs})