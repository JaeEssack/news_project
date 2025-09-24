from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

from .models import Article, CustomUser, Publisher
from .forms import ArticleForm


def is_reader(user):
    return user.role == 'reader'

def is_journalist(user):
    return user.role == 'journalist'    

def is_editor(user):
    return user.role == 'editor'


@login_required
@user_passes_test(is_reader)
def reader_dashboard(request):
    """
    Display the dashboard for readers, showing articles from
    subscribed publishers and journalists.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered dashboard template with articles.
    """
    from django.db.models import Q
    subscribed_publishers = request.user.subscribed_publishers.all()
    subscribed_journalists = request.user.subscribed_journalists.all()

    articles = Article.objects.filter(
        is_approved=True
    ).filter(
        Q(publisher__in=subscribed_publishers) | Q(journalist__in=subscribed_journalists)
    ).order_by('-created_at')

    all_publishers = Publisher.objects.all()
    all_journalists = CustomUser.objects.filter(role='journalist')

    return render(request, 'news_app/reader_dashboard.html', {
        'articles': articles,
        'publishers': all_publishers,
        'journalists': all_journalists
    })


@login_required
@user_passes_test(is_reader)
def subscribe_publisher(request, publisher_id):
    """
    Subscribe the logged-in reader to a publisher.

    Args:
        request (HttpRequest): The HTTP request object.
        publisher_id (int): ID of the publisher to subscribe to.

    Returns:
        HttpResponseRedirect: Redirects to reader dashboard.
    """
    publisher = get_object_or_404(Publisher, id=publisher_id)
    request.user.subscribed_publishers.add(publisher)
    return redirect('reader_dashboard')


@login_required
@user_passes_test(is_reader)
def unsubscribe_publisher(request, publisher_id):
    """
    Unsubscribe the logged-in reader from a publisher.

    Args:
        request (HttpRequest): The HTTP request object.
        publisher_id (int): ID of the publisher to unsubscribe from.

    Returns:
        HttpResponseRedirect: Redirects to reader dashboard.
    """
    publisher = get_object_or_404(Publisher, id=publisher_id)
    request.user.subscribed_publishers.remove(publisher)
    return redirect('reader_dashboard')

@login_required
@user_passes_test(is_reader)
def follow_journalist(request, journalist_id):
    """
    Follow a journalist as a reader.

    Args:
        request (HttpRequest): The HTTP request object.
        journalist_id (int): ID of the journalist to follow.

    Returns:
        HttpResponseRedirect: Redirects to reader dashboard.
    """
    journalist = get_object_or_404(CustomUser, id=journalist_id, role='journalist')
    request.user.subscribed_journalists.add(journalist)
    return redirect('reader_dashboard')

@login_required
@user_passes_test(is_reader)
def unfollow_journalist(request, journalist_id):
    """
    Unfollow a journalist as a reader.

    Args:
        request (HttpRequest): The HTTP request object.
        journalist_id (int): ID of the journalist to unfollow.

    Returns:
        HttpResponseRedirect: Redirects to reader dashboard.
    """
    journalist = get_object_or_404(CustomUser, id=journalist_id, role='journalist')
    request.user.subscribed_journalists.remove(journalist)
    return redirect('reader_dashboard')


@login_required
@user_passes_test(is_journalist)
def journalist_dashboard(request):
    """
    Display articles authored by the logged-in journalist.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered dashboard template with articles.
    """
    articles = Article.objects.filter(journalist=request.user).order_by('-created_at')
    return render(request, 'news_app/journalist_dashboard.html', {'articles': articles})


@login_required
@user_passes_test(is_journalist)
def create_article(request):
    """
    Allow a journalist to create a new article.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered form template or redirect after saving.
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.journalist = request.user
            article.save()
            return redirect('journalist_dashboard')
    else:
        form = ArticleForm()
    return render(request, 'news_app/create_article.html', {'form': form})


@login_required
@user_passes_test(is_editor)
def editor_dashboard(request):
    """
    Display unapproved articles for editors to review.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered editor dashboard template.
    """
    articles = Article.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'news_app/editor_dashboard.html', {'articles': articles})


@login_required
@user_passes_test(is_editor)
def approve_article(request, article_id):
    """
    Approve an article as an editor.

    Args:
        request (HttpRequest): The HTTP request object.
        article_id (int): ID of the article to approve.

    Returns:
        HttpResponseRedirect: Redirects to editor dashboard.
    """
    article = get_object_or_404(Article, id=article_id)
    article.is_approved = True
    article.save()
    return redirect('editor_dashboard')


@login_required
def redirect_dashboard(request):
    """
    Redirect users to their role-specific dashboard.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the appropriate dashboard.
    """
    role = getattr(request.user, 'role', None)

    if role == 'reader':
        return redirect('reader_dashboard')
    elif role == 'journalist':
        return redirect('journalist_dashboard')
    elif role == 'editor':
        return redirect('editor_dashboard')
    else:
        return redirect('login')


class CustomLoginView(LoginView):
    """Custom login view that redirects users to role-specific dashboards."""
    template_name = 'news_app/login.html'

    def get_success_url(self):
        """Redirect users to their role-specific dashboard after login"""
        role = getattr(self.request.user, 'role', None)
        # Debug log for development
        print(f"DEBUG: Logged in as {self.request.user.username}, role={role}") 

        if role == 'reader':
            return reverse('reader_dashboard')
        elif role == 'journalist':
            return reverse('journalist_dashboard')
        elif role == 'editor':
            return reverse('editor_dashboard')
        else:
            return reverse('login')
        

class CustomLogoutView(LogoutView):
    """Custom logout view allowing GET requests for convenience."""
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
