from django.shortcuts import render, redirect, reverse, get_object_or_404
from .import  forms, models
from django.http import HttpResponse
# Create your views here.
def make_post(request):
    logged = request.session.get('logged')
    if not logged:
        return redirect(reverse('log in'))
    if request.method == 'POST':
        form = forms.make_post(request.POST)

        if form.is_valid():
            # Form data is valid, you can access cleaned data using form.cleaned_data
            text = form.cleaned_data['text']
            new_post = models.Post(author=logged,  text=text)
            new_post.save()
            return redirect(reverse('home page'))
        else:
            return render(request, 'make_post.html', {'form': form, 'message':  'form was invalid'})
    else:
        return render(request,  "make_post.html", {"form":forms.make_post()})
    

def homepage(request):
    logged = request.session.get('logged')
    if logged:
        posts = models.Post.objects.filter(author=logged)  
        return render(request, 'home.html', {'posts': posts, 'name': logged})
    else:
        return redirect(reverse('log in'))
    
def view_profile(request, username):
    logged = request.session.get('logged')
    if not logged:
        return redirect(reverse('log in'))
    posts = models.Post.objects.filter(author=username)  
    return render(request, 'view_profile.html', {'posts': posts, 'name': username})
    
    

def view_post(request, post_id):
    logged = request.session.get('logged')
    if request.method == 'POST':
        form = forms.make_comment(request.POST)
        if not form.is_valid():
            return render(request, 'login.html', {'form': make_post(), 
                                                  'message': 'form is not valid'})
        text = request.POST.get('text')
        new_comment = models.Comment(author=logged, content=text, on_post=post_id)
        new_comment.save()
       
    form = forms.make_comment()
    post =  models.Post.objects.filter(id=post_id).first()
    comments = models.Comment.objects.filter(on_post=post_id)
    return render(request, 'view_post.html', {'post': post, 'comments': comments, 'form': form})

def delete_comment(request, comment_id):
    logged = request.session.get('logged')
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment = get_object_or_404(models.Comment, id=comment_id)
        if comment.author !=  logged:
            return HttpResponse("You do not have permission to edit this comment")
        
        comment.delete()
        return view_post(request, post_id)
        return redirect(reverse('view post', post_id=post_id))
    else:
        return HttpResponse('method must be delete')

    

def delete_post(request, post_id):
    logged = request.session.get('logged')
    if request.method == 'POST':
        post = get_object_or_404(models.Post, id=post_id)
        if post.author !=  logged:
            return HttpResponse("You do not have permission to edit this post")
        
        post.delete()
    return redirect(reverse('home page'))