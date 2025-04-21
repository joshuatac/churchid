from django.shortcuts import render, redirect
from users.models import Church, Member
from users.forms import ChurchForm, MemberFormCreate
from django.http.request import HttpRequest
from django.contrib import messages
import random
import string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, EmailForm
from .services import MessagingService
from .models import Otp

# Create your views here.


def generate_unique_id():
    """Generate a unique numeric ID for the username"""
    while True:
        unique_id = "".join(
            random.choices(string.digits, k=8)
        )  # Generate an 8-digit number
        if not Member.objects.filter(username=unique_id).exists():
            return unique_id


def register(request: HttpRequest, option=None):
    context = {"screen": option}

    if request.method == "GET":

        if option == "email-verification":
            form = EmailForm()
            context = {"form": form, "screen": option}
        else:

            # Check if user has verified otp
            otp = request.session.get("otp")
            if not otp:
                return redirect("login")

            else:

                email = request.session.get("email")

                # Membership Form Screen
                if option == "member":

                    church = Church.objects.get(id=request.GET.get("church"))
                    form = MemberFormCreate(initial={"church": church, "email": email})
                    context = {"form": form, "screen": option, "church": church}

                    # Church Selection Screen
                elif option == "select-church":

                    churches = Church.objects.all()
                    context = {"churches": churches, "screen": option}

                    # Church Form Screen
                elif option == "church":

                    form = ChurchForm(initial={"email": email})
                    context = {"form": form, "screen": option}

    # IF METHOD IS A POST METHOD
    else:
        church = None
        form = None
        email = request.session.get("email", "")
        post_data = request.POST.copy()  # Make it mutable
        if email:
            post_data["email"] = email  # Inject your value

        # Send OTP to email
        if option == "email-verification":
            form = EmailForm(post_data)

            if form.is_valid():
                email = form.cleaned_data["email"]
                mail = MessagingService(email)
                try:
                    otp = mail.send_otp_email()
                    request.session["email"] = email
                    request.session["otp"] = otp
                    messages.success(request, "OTP sent successfully!")
                    return redirect("/register/otp-verification/")

                except Exception as e:
                    messages.error(request, e.message)

            else:
                print(form.errors)

        # Verify OTP
        elif option == "otp-verification":
            otp_values = request.POST.getlist("otp")
            otp = "".join(otp_values)

            user_otp = request.session.get("otp")
            if user_otp:
                otp_matched = user_otp == otp

                if otp_matched:
                    messages.success(request, "OTP verified successfully!")
                    return redirect("/register/options/")
                else:
                    messages.error(request, "Invalid OTP!")

        # Register Member
        elif option == "member":

            form = MemberFormCreate(post_data)
            church = Church.objects.get(id=request.GET.get("church"))

            if form.is_valid():
                member: Member = form.save(commit=False)
                member.church = church
                mail = MessagingService(member.email)
                try:
                    context = {"member": member}
                    mail.send_email(context, "registration", "Account created.")
                    member.save()
                    return redirect("success")
                except Exception as e:
                    messages.error(request, e.message)

        # Register Church
        else:
            form = ChurchForm(post_data, request.FILES)
            if form.is_valid():
                church: Church = form.save()
                Member.objects.create_user(
                    username=generate_unique_id(),
                    password=form.clean_password(),
                    email=church.email,
                    church=church,
                    role="leader",
                    is_staff=True,
                    is_active=True,  # To set to False
                )
                return redirect("success")

        context = {"form": form, "screen": option, "church": church}
    return render(request, "register.html", context)


# Login


def login_user(request: HttpRequest):

    if request.user.is_authenticated:
        # Redirect to previous page if 'next' exists, otherwise go to dashboard
        next_url = request.GET.get("next", "dashboard")
        return redirect(next_url)

    if request.method == "POST":

        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=user_id, password=password)
            if user:

                login(request, user)

                if request.user.is_superuser:
                    return redirect("dashboard")

                else:
                    if not request.user.church.is_active:
                        messages.info(request, "Church currently inactive!")
                        logout(request)
                        return redirect("login")
                    return redirect("dashboard")
            else:
                messages.error(request, "Invalid credentials!")

    form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("login")


# Successful Registration
def success(request):
    return render(request, "success.html")


@login_required(login_url="login")
def account_activation(request: HttpRequest, id):

    if request.user.is_superuser:
        account = Church.objects.get(id=id)
    else:
        account = Member.objects.get(id=id)
        account.new = False
    account.is_active = False if account.is_active else True

    try:
        protocol = 'https' if request.is_secure() else 'http'

        # Get host: e.g. example.com or 127.0.0.1:8000
        host = request.get_host()

        # Full base URL
        domain = f"{protocol}://{host}"
        link = f"{domain}/login/"
        context = {"account": account, "link": link if account.is_active else None}
        mail = MessagingService(account.email)
        mail.send_email(context, "activation", "Account Status")
        account.save()
        if account.is_active:
            messages.success(request, "Account Activated!!!")
        else:
            messages.error(request, "Account Deactivated!!!")
    except Exception as e:
        messages.error(request, e.message)

    return redirect("dashboard" if request.user.is_superuser else "members")


def member_account_activation(request, id):
    pass
