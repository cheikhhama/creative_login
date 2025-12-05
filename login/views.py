from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Coin denominations (statistical, frontend only)
DENOMS = [1, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]

# ------------------------------------------------------------
# SIGNUP
# ------------------------------------------------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        currency = request.POST.get("currency")
        pattern_raw = request.POST.get("pattern")  # ex: "1,5,20"

        # Transform pattern into a list and calculate total
        pattern_list = [int(x) for x in pattern_raw.split(',') if x.isdigit()]
        total = sum(pattern_list)

        # Save to DB
        UserProfile.objects.create(
            username=username,
            currency=currency,
            pattern=pattern_raw,
            total=total
        )

        request.session['username'] = username
        return redirect("dashboard")

    return render(request, "login/signup.html", {"denoms": DENOMS})


# ------------------------------------------------------------
# LOGIN (pattern-based)
# ------------------------------------------------------------
def login_view(request):
    error = None

    if request.method == "POST":
        pattern_raw = request.POST.get("pattern")
        pattern_list = [int(x) for x in pattern_raw.split(',') if x.isdigit()]
        total = sum(pattern_list)

        try:
            user = UserProfile.objects.get(pattern=pattern_raw, total=total)
            request.session['username'] = user.username
            return redirect("dashboard")
        except UserProfile.DoesNotExist:
            error = "Pattern incorrect."

    return render(request, "login/login.html", {"error": error, "denoms": DENOMS})
def edit_pattern_view(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    user = UserProfile.objects.get(username=username)

    if request.method == "POST":
        pattern_raw = request.POST.get("pattern", "")
        pattern_list = [int(x) for x in pattern_raw.split(',') if x.isdigit()]
        total = sum(pattern_list)

        user.pattern = pattern_raw
        user.total = total
        user.save()

        return redirect("dashboard")

    return render(request, "login/edit.html", {
        "user": user,
        "denoms": DENOMS
    })
def dashboard_view(request):
    username = request.session.get("username") 

    if not username:
        return redirect("login")  

    try:
        user = UserProfile.objects.get(username=username)
        user.pattern_list = [int(x) for x in user.pattern.split(",") if x.isdigit()]
    except UserProfile.DoesNotExist:
        request.session.pop("username", None)
        return redirect("login")

    return render(request, "login/dashboard.html", {"user": user})


def logout_view(request):
    request.session.flush()
    return redirect("login")


def intro_view(request):
    return render(request, "login/intro.html")