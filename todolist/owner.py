from django.views.generic import ListView


class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """

