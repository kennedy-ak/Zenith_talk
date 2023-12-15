from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm, CommentForm



# Create your views here.


def post_list(request):
    object_list = Post.published.all()
    paginator =Paginator(object_list,2) #  posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page results
        posts = paginator.page(paginator.num_pages)


 
    return render(request,
                 'blog/post/list.html',
                 {'posts': posts,'page':page})

def post_detail(request, year, month, day, post):
    
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    #list of active comment
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        #a comment was made
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but dont save to the database
            new_comment = comment_form.save(commit=False)

            # assign current post to the current comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments':comments,
                  'new_comment':new_comment,
                  'comment_form' :comment_form
                  
                  })




def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'akogokennedy@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})