from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .models import Donation, Event, Announcement, Post, PrayerRequest
from .forms import DonationForm, EventForm, PostForm, AnnouncementForm, PrayerRequestForm


# Create your views here.

# Donations
@login_required(login_url="login")
def member_donations(request: HttpRequest):
    
    if request.user.is_staff:
        donations  = Donation.objects.filter(church =request.user.church)
    else:
        donations = Donation.objects.filter(donor = request.user, church =request.user.church)

    context = {
        "donations": donations, 
        "screen": "donations", 
        "active_menu": "donations"
        }
    return render(request, "main/users/index.html", context)



@login_required(login_url="login")
def donate(request: HttpRequest):
    
    form = DonationForm()
    
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation: Donation = form.save(commit=False)
            donation.donor = request.user
            donation.church = request.user.church
            donation.save()
            return redirect("donations")
    
    context = {
        "form": form,
        "screen": "donations", 
        "active_menu": "donations"
        }
    return render(request, "main/users/index.html", context)


# Prayer Requests
@login_required(login_url="login")
def prayer_requests(request: HttpRequest):
    id = request.GET.get("id")
    edit = request.GET.get("edit")
    delete = request.GET.get("delete")
    status = request.GET.get("status")
    form = PrayerRequestForm(request.POST or None)
    
    # Change Prayer Status
    if status:
        prayer = PrayerRequest.objects.get(id=id)
        prayer.status = status
        prayer.new = False
        prayer.save()
        return redirect("prayers")


    # Delete Prayer
    if delete:
        prayer = PrayerRequest.objects.get(id=delete)
        prayer.delete()
        return redirect("prayers")

    # Edit Prayer
    if edit:
        prayer = PrayerRequest.objects.get(id=edit)
        form = PrayerRequestForm(request.POST or None, instance=prayer)
        
    if request.method == "POST":
        if form.is_valid():
            prayer: PrayerRequest = form.save(commit=False)
            prayer.church = request.user.church
            prayer.sender = request.user
            
            prayer.save()
            return redirect("prayers")

    if id:
        prayer = PrayerRequest.objects.get(id=id)
    else:
        prayer = None

    # Users Prayers

    prayers = PrayerRequest.objects.all()
    context = {
        "prayer": prayer,
        "prayers": prayers,
        "screen": "prayers",
        "form": form,
        "edit": edit,
        "active_menu": "prayers",
    }
    return render(request, "main/users/index.html", context)


# Events
@login_required(login_url="login")
def events(request:HttpRequest, type = "view"): 
    
    church_events = Event.objects.filter(church = request.user.church)
    form = EventForm()
    button_text = "Create"
    
    
        

    event = request.GET.get("id", None)
    if  event:
        try :
            event = Event.objects.get(id= event)
            form = EventForm(request.POST or None, instance= event)
            event.new = False
            button_text = "Update"
        except:
           event = None
           
    if type == "delete":
        event.delete()
        return redirect("/events/view/")
    
     
    if request.method == "POST":
        form = EventForm(request.POST or None, instance= event)
        if form.is_valid():
            event:Event = form.save(commit=False)
            event.church = request.user.church
            event.save() 
            return redirect("/events/view/")
   
    context = {
        "screen": "events",
        "active_menu": "events",
        "events": church_events,
        'type': type,
        'form': form,
        "event": event,
        'button_text': button_text
    }
    
    return render(request, "main/users/index.html", context)


# Announcements
@login_required(login_url="login")
def announcements(request: HttpRequest):
    id = request.GET.get("id")
    delete = request.GET.get("delete")

    if delete:
        announcement = Announcement.objects.get(id=delete)
        announcement.delete()
        return redirect("announcements")

    form = AnnouncementForm()
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if id:
            announcement = Announcement.objects.get(id=id)
            form = AnnouncementForm(request.POST or None, instance=announcement)
        if form.is_valid():
            dept: Announcement = form.save(commit=False)
            dept.church = request.user.church
            dept.save()
            return redirect("announcements")

    if id:
        announcement = Announcement.objects.get(id=id)
        form = AnnouncementForm(request.POST or None, instance=announcement)

    # Users Announcements

    announcements = Announcement.objects.all()
    context = {
        "announcements": announcements,
        "screen": "announcements",
        "form": form,
        "edit": id,
        "active_menu": "announcements",
    }
    return render(request, "main/users/index.html", context)


# Posts
@login_required(login_url="login")
def posts(request:HttpRequest, type = "view"): 
    
    church_posts = Post.objects.filter(church = request.user.church)
    form = PostForm()
    button_text = "Create"
    id = request.GET.get("id", None)
    
    
        

    post = request.GET.get("id", None)
    if  post:
        try :
            post = Post.objects.get(id= post)
            form = PostForm(request.POST or None, request.FILES or None, instance= post)
            post.new = False
            button_text = "Update"
        except:
           post = None
           
    if type == "delete":
        post.delete()
        return redirect("/posts/view/")
    
     
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None, instance= post)
        if form.is_valid():
            post:Post = form.save(commit=False)
            post.church = request.user.church
            post.save() 
            if type == 'edit':
                return redirect(f"/posts/view/?id={request.GET.get('id', None)}")
            else:
                return redirect("/posts/view/")
   
    context = {
        "screen": "posts",
        "active_menu": "posts",
        "posts": church_posts,
        'type': type,
        'form': form,
        "post": post,
        'id': id,
        'button_text': button_text
    }
    
    return render(request, "main/users/index.html", context)
