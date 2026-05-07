from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "price", "edition"]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Price must be >= 0")
        return price

    def clean_edition(self):
        edition = self.cleaned_data["edition"]
        if edition < 1:
            raise forms.ValidationError("Edition must be >= 1")
        return edition