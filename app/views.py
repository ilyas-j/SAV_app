from multiprocessing import AuthenticationError
from django.shortcuts import render # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.models import User, Group # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login as auth_login # type: ignore

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # 🔥 Ici on vérifie dans quel groupe est l'utilisateur
            if user.groups.filter(name='technicien').exists():
                return redirect('technicien_home')
            elif user.groups.filter(name='responsable_sav').exists():
                return redirect('respo_home')
            elif user.groups.filter(name='client').exists():
                return redirect('client_home')
            else:
                # Si pas de groupe, rediriger vers une page par défaut
                return redirect('default_home')

        else:
            return render(request, 'login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})

    return render(request, 'login.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_type = request.POST['user_type']

        # Vérifier que les mots de passe correspondent
        if password != confirm_password:
            return render(request, 'signup.html', {'error': "Les mots de passe ne correspondent pas."})

        # Vérifier que le nom d'utilisateur n'existe pas déjà
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': "Ce nom d'utilisateur existe déjà."})

        # Créer l'utilisateur
        user = User.objects.create_user(username=username, password=password)

        # Ajouter l'utilisateur dans le bon groupe
        try:
            group = Group.objects.get(name=user_type)  # "client", "responsable_sav" ou "technicien"
            user.groups.add(group)
        except Group.DoesNotExist:
            return render(request, 'signup.html', {'error': "Le type d'utilisateur est invalide."})

        # Connecter automatiquement ou rediriger vers login
        messages.success(request, "Compte créé avec succès ! Connecte-toi maintenant.")
        return redirect('login')  # ou une autre page si tu veux

    return render(request, 'signup.html') 
def technicien_home(request):
    return render(request, 'technicien_home.html')

def respo_home(request):
    return render(request, 'responsable_home.html')

def client_home(request):
    return render(request, 'client_home.html')