from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from users.models import Member, Church
from .forms import ChurchForm, MemberFormUpdate, MemberFormCreate
from django.contrib import messages


@login_required(login_url="login")
def members(request):
    members = Member.objects.filter(church=request.user.church, role="member")
    context = {"members": members, "screen": "members", "active_menu": "members"}
    return render(request, "main/users/index.html", context)


@login_required(login_url="login")
def add_member(request: HttpRequest):

    form = MemberFormUpdate()

    if request.method == "POST":
        form = MemberFormUpdate(request.POST)
        if form.is_valid():
            member: Member = form.save(commit=False)
            member.church = request.user.church
            member.set_password("000000")
            member.save()
            return redirect("members")


    context = {"form": form, "screen": "add-member", "active_menu": "members"}
    return render(request, "main/users/index.html", context)


@login_required(login_url="login")
def profile(request: HttpRequest, type, id):

    if request.user.is_superuser:
        church_profile = Church.objects.get(id=id)
        context = {
            "profile": church_profile,
        }
    else:
        member_profile = Member.objects.get(id=id)
        context = {
            "profile": member_profile,
            "screen": "profile",
            "type": type,
            "active_menu": type,
            "state": "view",
        }

    return render(request, "main/users/index.html", context)


@login_required(login_url="login")
def profile_edit(request: HttpRequest, type, id):

    if request.user.is_superuser:
        user_profile = Church.objects.get(id=id)
        form = ChurchForm(request.POST or None, instance=user_profile)
    else:
        user_profile = Member.objects.get(id=id)
        form = MemberFormUpdate(request.POST or None, instance=user_profile)

    if request.method == "POST" and form.is_valid():
        form.save()
        # messages.success(request, "Profile updated successfully!")
        return redirect(f"/profile/{type}/{id}")

    else:
        print(form.errors)

    context = {
        "profile": user_profile,
        "screen": "profile",
        "type": type,
        "active_menu": type,
        "form": form,
        "state": "edit",
    }

    return render(request, "main/users/index.html", context)


@login_required(login_url="login")
def delete_user(request: HttpRequest, id):

    if request.user.is_superuser:
        church = Church.objects.get(id=id)
        church.delete()
        return redirect("dashboard")
    else:
        member = Member.objects.get(id=id)
        member.delete()
        return redirect("members")
