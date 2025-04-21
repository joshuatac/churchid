from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Church, Member, Department
from django.http.request import HttpRequest
from .forms import DepartmentForm
from activities.models import Donation, Event, Post, Announcement, PrayerRequest

# Create your views here.


@login_required(login_url="login")
def dashboard(request: HttpRequest):

    # Admin Dashboard
    if request.user.is_superuser:
        churches = Church.objects.all()
        context = {"churches": churches}
        return render(request, "main/admin/dashboard.html", context)

    # Users Dashboard
    members = Member.objects.filter(church=request.user.church, role="member")
    donations = Donation.objects.filter(church = request.user.church)[:5]
    events = Event.objects.filter(church = request.user.church)[:5]
    posts = Post.objects.filter(church = request.user.church)[:3]
    announcements = Announcement.objects.filter(church= request.user.church, published=True)
    if request.user.is_staff:
        prayers = PrayerRequest.objects.filter(church= request.user.church)
    else:
        prayers = PrayerRequest.objects.filter(church= request.user.church, sender= request.user)

    
    event = request.GET.get("id", None)
    if  event:
        try :
            event = Event.objects.get(id= event)
            event.new = False
        except:
           event =None
       
       
    context = {
        "members": members, 
        "screen": "dashboard", 
        "active_menu": "dashboard",
        "donations": donations,
        "events": events,
        "event": event,
        "posts": posts,
        'announcements': announcements,
        "prayers": prayers 
        }
    return render(request, "main/users/index.html", context)


@login_required(login_url="login")
def departments(request: HttpRequest):
    id = request.GET.get("id")
    delete = request.GET.get("delete")

    if delete:
        department = Department.objects.get(id=delete)
        department.delete()
        return redirect("departments")

    form = DepartmentForm()
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if id:
            department = Department.objects.get(id=id)
            form = DepartmentForm(request.POST or None, instance=department)
        if form.is_valid():
            dept: Department = form.save(commit=False)
            dept.church = request.user.church
            dept.save()
            return redirect("departments")

    if id:
        department = Department.objects.get(id=id)
        form = DepartmentForm(request.POST or None, instance=department)

    # Users Departments

    departments = Department.objects.all()
    context = {
        "departments": departments,
        "screen": "departments",
        "form": form,
        "edit": id,
        "active_menu": "departments",
    }
    return render(request, "main/users/index.html", context)
