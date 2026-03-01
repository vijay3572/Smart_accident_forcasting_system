from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm, LoginForm, AccidentReportForm
from .models import AccidentReport, Feedback, Contact

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignupForm, LoginForm


# =======================
# HOME PAGE
# =======================
def home(request):
    return render(request, "accounts/home.html")


# =======================
# SIGNUP VIEW
# =======================
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # ✅ password hashed + details saved

            messages.success(
                request,
                f"Account created successfully! Your User ID: {user.id}. Please login."
            )
            # ✅ IMPORTANT: after signup go to login page
            return redirect("accounts:login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


# =======================
# LOGIN VIEW
# =======================
def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # ✅ AuthenticationForm already authenticated the user
            user = form.get_user()
            login(request, user)  # ✅ session set

            messages.success(request, "Login successful!")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


# =======================
# LOGOUT VIEW
# =======================
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("accounts:login")


# =======================
# DASHBOARD
# =======================
@login_required(login_url="accounts:login")
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")
# =======================
# SEARCH LOCATION
# =======================
def search_location(request):
    query = request.GET.get("query", "").strip()
    results = []

    if query:
        results = AccidentReport.objects.filter(location__icontains=query)

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "search.html", context)


# =======================
# REPORT PAGE (Main)
# =======================
@login_required
def report(request):
    if request.method == "POST":
        form = AccidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect("accounts:report_success")
    else:
        form = AccidentReportForm()

    return render(request, "report.html", {"form": form})


# =======================
# REPORT SUCCESS PAGE
# =======================
@login_required
def report_success(request):
    return render(request, "accounts/report_success.html")


# =======================
# CONTACT / FEEDBACK PAGE
# =======================
def contact(request):
    success = False

    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        success = True

    return render(request, "contact.html", {"success": success})
