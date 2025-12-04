from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import UserProfile

# Liste simple de pièces (exemple)
DENOMS = [1,5,10,20,50,100,500,1000]


# ------------------------------------------------------------
# 1) INSCRIPTION
# ------------------------------------------------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        currency = request.POST.get("currency")
        pattern_raw = request.POST.get("pattern")  # ex: "1,5,20"

        # Transformation du pattern en liste
        pattern_list = [int(x) for x in pattern_raw.split(',') if x.isdigit()]
        total = sum(pattern_list)

        # Enregistrer dans la base
        UserProfile.objects.create(
            username=username,
            currency=currency,
            pattern=pattern_raw,
            total=total
        )

        request.session['username'] = username
        return redirect("dashboard")

    return render(request, "signup.html", {
        "denoms": DENOMS
    })


# ------------------------------------------------------------
# 2) CONNEXION PAR PATTERN
# ------------------------------------------------------------
def login_view(request):
    error = None

    if request.method == "POST":
        pattern_raw = request.POST.get("pattern")

        # Recalcul du total
        pattern_list = [int(x) for x in pattern_raw.split(',') if x.isdigit()]
        total = sum(pattern_list)

        try:
            user = UserProfile.objects.get(pattern=pattern_raw, total=total)
            request.session['username'] = user.username
            return redirect("dashboard")

        except UserProfile.DoesNotExist:
            error = "Pattern incorrect."

    return render(request, "login.html", {
        "error": error
    })


# ------------------------------------------------------------
# 3) DASHBOARD SIMPLE
# ------------------------------------------------------------
def dashboard_view(request):
    username = request.session.get("username")

    if not username:
        return render(request, "dashboard.html", {"is_logged": False})

    user = UserProfile.objects.get(username=username)

    return render(request, "dashboard.html", {
        "is_logged": True,
        "user": user
    })
