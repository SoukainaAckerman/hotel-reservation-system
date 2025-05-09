from django.shortcuts import render, redirect
from .models import User  # ✅ On utilise le modèle Django ORM

def signaction(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        genre = request.POST.get("genre")  # ✅ tu as remplacé statut par genre
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ✅ Insertion via ORM dans db.sqlite3 → table signup_user
        new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            statut=genre,   # Utilise la valeur du formulaire (homme/femme/etc)
            email=email,
            password=password,
            role='client'   # Toujours client par défaut
        )
        
        # Connexion automatique de l'utilisateur après inscription
        request.session['user_id'] = new_user.id
        request.session['user_email'] = email
        request.session['user_role'] = 'client'

        return redirect("welcome")  # Redirection après signup

    return render(request, "signup_page.html")


def welcome(request):
    return render(request, "welcome.html")

def fix_all_roles_to_client():
    User.objects.all().update(role='client')

from signup.models import User
User.objects.filter(role='c.').update(role='client')
