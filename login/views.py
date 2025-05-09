from django.shortcuts import render, redirect
from signup.models import User  # On utilise le modèle User de l'app signup

# Vue pour la page de connexion
def loginaction(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Vérification des identifiants avec le modèle ORM
        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id  # Ajoute l'id utilisateur à la session
            # Redirection selon le rôle
            if user.email == 'adminadmin@gmail.com' and user.role == 'admin':
                return redirect('/hotelweb/admin/dashboard/')
            return redirect('welcome')  # Redirection vers la vue welcome
        else:
            # Au lieu de rediriger vers error.html, on affiche un message sur la page de login
            error_message = "Identifiants incorrects. Veuillez réessayer."
            return render(request, 'login_page.html', {'error_message': error_message})

    return render(request, 'login_page.html')  # Affiche le formulaire en GET

def logout_view(request):
    request.session.flush()  # Supprime toute la session (déconnexion)
    return redirect('login')  # Redirige vers la page de login (nom correct)

# Vue "welcome" pour la page d'accueil
def welcome(request):
    user_name = None
    user_id = request.session.get('user_id')
    if user_id:
        from signup.models import User
        user = User.objects.filter(id=user_id).first()
        if user:
            user_name = f"{user.first_name} {user.last_name}".strip()
    return render(request, "welcome.html", {"user_name": user_name})
