from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Request, Message

# Create your views here.


def home(request):
    return render(request, 'core/home.html')


def request_list(request):
    requests = Request.objects.all().order_by('-created_at')
    return render(request, 'core/request_list.html', {'requests': requests})


def create_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Request.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        return redirect('request_list')

    return render(request, 'core/create_request.html')



@login_required
def request_list(request):
    status = request.GET.get('status')

    if request.user.is_staff:
        requests = Request.objects.all()
        base_title = "All Requests"
    else:
        requests = Request.objects.filter(created_by=request.user)
        base_title = "My Requests"

    if status:
        requests = requests.filter(status=status)

    requests = requests.order_by('-created_at')

    status_titles = {
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'completed': 'Completed',
    }

    if status in status_titles:
        page_title = f"{status_titles[status]} - {base_title}"
    else:
        page_title = base_title

    return render(request, 'core/request_list.html', {
        'requests': requests,
        'current_status': status,
        'page_title': page_title,
    })




@login_required
def create_request(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Request.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        return redirect('request_list')

    return render(request, 'core/create_request.html')

@login_required
def request_detail(request, pk):
    req = get_object_or_404(Request, pk=pk)

# Permission check
    if not (request.user.is_staff or req.created_by == request.user):
        return redirect('request_list')
    messages = req.messages.all().order_by('created_at')


    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Message.objects.create(
                request=req,
                sender=request.user,
                content=content
            )
            return redirect('request_detail', pk=req.pk)

    return render(request, 'core/request_detail.html', {
        'request_obj': req,
        'messages': messages,
    })



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})



@login_required
def home(request):
    if request.user.is_staff:
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(created_by=request.user)

    total_requests = requests.count()
    pending_requests = requests.filter(status='pending').count()
    in_progress_requests = requests.filter(status='in_progress').count()
    completed_requests = requests.filter(status='completed').count()

    context = {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'in_progress_requests': in_progress_requests,
        'completed_requests': completed_requests,
    }

    return render(request, 'core/home.html', context)








