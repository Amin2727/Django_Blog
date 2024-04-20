from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


class FieldsMixin():
    """
    This mixin says that if the user is a superuser, 
    show the author, otherwise, only show the above fields.
    """

    def dispatch(self, request, *args, **kwargs):
        self.fields = [
                "title", "slug", "category",
                "description", "thumbnail","publish", 
                "is_special", "status",
        ]
        if request.user.is_superuser:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)



class FormValidMixin():
    """
    This mixin says that the article should be 
    displayed as a draft on the normal author panel page.
    """

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)



class AuthorAccessMixin():
    """
    This mixin says that only the superuser can delete or 
    edit the articles and the normal author cannot do this.
    """

    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article,pk=pk)
        if article.author == request.user and article.status in ['b', 'd'] or \
            request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page!!")



class AuthorsAccessMixin():
    """
    This mixin says that users who are neither authors nor superusers 
    cannot see the articles in their profile and can only see their own profile.
    """
    
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("account:login")



class SuperUserMixin():
    """We use this mixin so that normal users cannot delete articles."""

    def dispatch(self, request,*args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You can't see this page!!")
        