from django.shortcuts import render, redirect
from django.http import HttpResponse
from poll.forms import CreatePollForm
from poll.models import Poll, Voting_result
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate

# Create your views here.
def home(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request,'poll/home.html',context)

@login_required
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form':form
    }
    return render(request,'poll/create.html',context)

@login_required
def vote(request,poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        selected_option = request.POST['poll']
        if Voting_result.objects.filter(choice=poll,voter=request.user).exists():
            return HttpResponse('You have already voted')
        elif selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invaid Form')

        poll.save()
        Voting_result.objects.create(voter=request.user, choice=poll)
        return redirect('results', poll.id)
    context = {
        'poll': poll
    }
    return render(request,'poll/vote.html',context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll': poll
    }
    return render(request,'poll/results.html',context)

@login_required
def delete_poll(request, poll_id):
    Poll.objects.get(pk=poll_id).delete()
    return redirect('home')
