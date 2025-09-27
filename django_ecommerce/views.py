from django.shortcuts import render


def home_view(request):
    """A simple view for the homepage."""
    return render(request, "home.html", {})