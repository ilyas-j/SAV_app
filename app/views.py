from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Check which group the user belongs to
            if user.groups.filter(name='technicien').exists():
                return redirect('technicien_home')
            elif user.groups.filter(name='responsable_sav').exists():
                return redirect('responsable_home')  # Fixed name to match URL
            elif user.groups.filter(name='client').exists():
                return redirect('client_home')
            else:
                # If no group, redirect to default page
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

        # Verify passwords match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': "Les mots de passe ne correspondent pas."})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': "Ce nom d'utilisateur existe déjà."})

        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Add user to the right group
        try:
            group = Group.objects.get(name=user_type)  # "client", "responsable_sav" or "technicien"
            user.groups.add(group)
        except Group.DoesNotExist:
            # Create the group if it doesn't exist
            group = Group.objects.create(name=user_type)
            user.groups.add(group)

        # Automatic login or redirect to login
        messages.success(request, "Compte créé avec succès ! Connecte-toi maintenant.")
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def technicien_home(request):
    return render(request, 'technicien_home.html')

@login_required
def respo_home(request):
    return render(request, 'responsable_home.html')

@login_required
def client_home(request):
    return render(request, 'client_home.html')

@login_required
def default_home(request):
    return render(request, 'default_home.html', {'message': 'Bienvenue sur votre espace personnel'})