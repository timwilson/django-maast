from django.shortcuts import render


def faq_view(request):
    return render(request, "faq.html")


def privacy_policy_view(request):
    return render(request, "privacy_policy.html")


def terms_of_use_view(request):
    return render(request, "terms_of_use.html")