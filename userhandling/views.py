from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import urllib, json
import hashlib
import random
from .utils import Mailchimp, VerificationHash
from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm

from .models import Movie, MovieNightEvent, Profile, PasswordReset
# ...


# Access movie info using IMDB and add model instance containing info
def add_movie_fromIMDB(request, imdb_id):
    args = {"apikey": settings.OMDB_API_KEY, "i": imdb_id, "plot" : "full"}
    url_api = " http://www.omdbapi.com/?{}".format(urllib.parse.urlencode(args))

    # Load Return Object Into JSON
    try:
        with urllib.request.urlopen(url_api) as url:
            data = json.loads(url.read().decode())
    except:
        raise Exception("{} is not valid IMDB ID")

    # Create movie instance from returned JSON
    m = Movie(imdbID=imdb_id)
    m.title = data["Title"]
    m.year = data["Year"]
    m.director = data["Director"]
    m.runtime = data["Runtime"]
    m.plot = data["Plot"]
    m.country = data["Country"]
    m.actors = data["Actors"]
    m.save()

    return render(request, 'userhandling/index.html')

# Render Index Page, manage register
def index(request):
    movienights = MovieNightEvent.objects.order_by('-date')[:5]
    successful_verified = False
    context = {
        'movienights'           : movienights,
        'successful_verified'   : successful_verified,
        'email'                 : "",
        'username'              : ""
    }
    return render(request, 'userhandling/index.html', context)

#View called from activation email. Activate user if link didn't expire (48h default), or offer to
#send a second link if the first expired.
def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            activation_expired = True #Display: offer the user to send a new activation link
            id_user = profile.user.id
            # TODO THis will fail
            new_activation_link(request, id_user)

        else: #Activation successful
            # Activate user.
            profile.user.is_active = True
            profile.user.save()

            # Subscribe to Mailchimp list.
            mc = Mailchimp(settings.MAILCHIMP_EMAIL_LIST_ID)
            mc.add_email(profile.user.email)

            # Todo: Add more fields to Mailchimp.

            movienights = MovieNightEvent.objects.order_by('-date')[:5]
            successful_verified = True
            context = {
            'movienights'           : movienights,
            'successful_verified'   : successful_verified,
            'email'                 : profile.user.email,
            'username'              : profile.user.username
            }
            return render(request, 'userhandling/index.html', context)

    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
        return HttpResponse("User already registered.")


def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:

        #We generate a random activation key
        vh = VerificationHash()
        datas['activation_key']= vh.gen_ver_hash(datas['username'])

        # Update profile with new activation key and expiry data.
        profile = Profile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()


        # Resend verification email.
        mg = Mailgun()
        link="http://cinemaple.com/activate/"+profile.activation_key



        sender_email    = "admin@cinemaple.com"
        sender_name     = "Cinemaple"
        subject         = "Your new activation link."
        recipients      = [user.email]
        content         = "Please activate your email using the following link: " + link

        # Send message and retrieve status and return JSON object.
        status_code, r_json = mg.send_email(sender_email, sender_name, subject, recipients, content)

        assert status_code == 200, "Send of new key failed"
        request.session['new_link']=True #Display: new link sent
        return HttpResponse("Activation link expired. You have resent an activation link for {}.".format(user.email))

    return redirect('index')

def registration(request):
    registration_form = RegistrationForm()

    # Has a registration succesfully been submitted?
    successful_reg_submit = False
    subscribe_email = ''

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            datas={}
            datas['username']=registration_form.cleaned_data['username']
            datas['email']=registration_form.cleaned_data['email']
            datas['password1']=registration_form.cleaned_data['password1']
            datas['first_name']=registration_form.cleaned_data['first_name']
            datas['last_name']=registration_form.cleaned_data['last_name']

            # TODO: Check if user alredy exists

            #We generate a random activation key
            vh = VerificationHash()
            datas['activation_key']= vh.gen_ver_hash(datas['username'])

            registration_form.send_activation_email(datas)
            registration_form.save(datas) #Save the user and his profile

            successful_reg_submit = True
            subscribe_email = datas['email']

    context = {
        'form': registration_form,
        'successful_submit' : successful_reg_submit,
        'subscribe_email' :  str(subscribe_email),
    }
    return render(request, 'userhandling/registration.html', context)


def my_login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # At this point, the clean() fuction in the form already made sure that the user is valid and active.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(index)
            else:
                return HttpResponse("User is none despite clean in form.")
        else:
            login_form = form #Display form with error messages (incorrect fields, etc)

    context = {
        'login_form': login_form,
    }
    return render(request, 'userhandling/login.html', context)

def password_reset_request(request):
    # TODO: Make active flag to pw_rest
    form = PasswordResetRequestForm()
    successful_submit = False
    reset_email = ""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            reset_email = form.populate_PasswordReset_send_email()
            successful_submit = True

    context = {
        'form': form,
        'successful_submit' : successful_submit,
        'reset_email' : reset_email
    }
    return render(request, 'userhandling/password_reset_request.html', context)

def password_reset_request_done(request):
    form = PasswordResetRequestForm(request.POST)
    context = {
        'form': form,
        'successful_submit' : True,
    }
    return render(request, 'userhandling/password_reset_request.html', context)


def password_reset(request, reset_key):

     # get user
    try:
        pr = PasswordReset.objects.get(reset_key=reset_key)
        pr_exists = True
    except PasswordReset.DoesNotExist:
        return HttpResponse("Password link could not be associated with valid username.")

    if pr_exists:
        if timezone.now() > pr.created_at + datetime.timedelta(days=2):
            return HttpResponse("Password rest key expired, please restart password reset.")

    form = PasswordResetForm()
    successful_submit = False
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # get pw from form
            pw = form.cleaned_data['password1']
            if pr_exists:
                username = pr.username
                user = User.objects.get(username=username)
                user.password = pw
                user.save()
                successful_submit = True
    context = {
        'form': form,
        'successful_submit' : successful_submit,
        'reset_key' : reset_key
    }

    return render(request, 'userhandling/password_reset.html', context)



