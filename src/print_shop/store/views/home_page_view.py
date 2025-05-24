from django.shortcuts import render


def home_page_view(request):
    """
    Renders the home page of the print shop.
    """
    return render(request, "customer_facing_pages/home.html")
