from urllib import request
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Articlemodel

from django.contrib import messages


class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data
class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_superuser:
            self.fields = [
                
                'title', 'slug',
                'category', 'description', 
                'thumbnail', 'publish','is_special','status'
            ]
            
            if request.user.is_superuser:
                self.fields.append('author')

            return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
        def form_valid(self, form):
            if self.request.user.is_superuser:
                form.save()
            else:
                self.obj = form.save(commit=False)
                self.obj.author = self.request.user
                if not self.obj.status in ['d', 'i']:
                    self.obj.status  = 'd'
            return super().form_valid(form)

class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Articlemodel, pk=pk)
        if article.author == request.user and article.status in['d', 'b'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        else:
          
            raise Http404(' you can not see this page ')

class SuperAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        if  request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        else:
          
            raise Http404(' you can not see this page ')

class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if  request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)

            else:
            
                return redirect("account:profile")
        else:

            return redirect("login")
        