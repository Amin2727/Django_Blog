from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User
from .forms import ProfileForm
from .mixins import (
    FieldsMixin, 
    FormValidMixin,
    AuthorAccessMixin,
    AuthorsAccessMixin,
    SuperUserMixin
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.models import Article




class ArticleList(AuthorsAccessMixin,ListView):
    """This view is related to show articles in user profile"""

    template_name = 'registration/home.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)



class ArticleCreate(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
    """This view is related to create article for users."""

    model = Article
    fields = ["author", "title", "slug", "category", "description", "thumbnail", "publish", "status",]
    template_name = 'registration/article-create-update.html'



class ArticleUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    """This view is related to update article for users."""

    model = Article
    fields = ["author", "title", "slug", "category", "description", "thumbnail", "publish", "status",]
    template_name = 'registration/article-create-update.html'



class ArticleDelete(SuperUserMixin, DeleteView):
    """This view is related to delete article for users."""

    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'



class Profile(LoginRequiredMixin, UpdateView):
    """This view is related to the user's profile."""

    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs



class Login(LoginView):
    """This view is related to user login."""
    def get_success_url(self):
        user = self.request.user
    
        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")

class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")
