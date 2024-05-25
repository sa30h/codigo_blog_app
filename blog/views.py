from .models import Blog,Comment,Like,Tag

from django.shortcuts import render,redirect, get_object_or_404

from django.db.models import Q
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.core.mail import send_mail

# Create your views here.

# def BlogView(request):
#     return render(request,'blog/bloglist.html')
BLOG_POSTS_PER_PAGE = 5

def DetailBlogView(request, pk):
     if request.user.is_authenticated:
        context = {}
        comments=Comment.objects.filter(blog__id=pk)
        context['comments']=comments
        tags=Tag.objects.filter(blog__id=pk)
        context['tags']=tags
        blog_post = get_object_or_404(Blog, pk=pk)
        comment_like=Like.objects.filter(comment__pk=pk,liked_by=request.user).first()
        if comment_like:
            context['is_comment_liked']=str(comment_like.like)
        context['blog_post'] = blog_post
        return render(request, 'blog/detail_blog.html', context)
     else:
          return redirect('login')

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ") # python 
    for q in queries:
        posts = Blog.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).distinct()

        postsbytag = Tag.objects.filter(
				Q(tag_content__icontains=q)
			).distinct()
        
        for post in posts:
             queryset.append(post)
        for post in postsbytag:
             print('tag post',post)
             queryset.append(post.blog)
             
    return list(set(queryset))

def BlogView(request, *args, **kwargs):
	
    if(request.user.is_authenticated):
	
        context = {}

        # Search
        query = ""
        if request.GET:
            query = request.GET.get('tagq', '')
            # query = request.GET.get('bodyq', '')
            context['query'] = str(query)
            # context['bodyquery'] = str(query)
            blog_posts = sorted(get_blog_queryset(query), key=attrgetter('updated_on'), reverse=True)
                    # Pagination
            page = request.GET.get('page', 1)
            blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
            try:
                blog_posts = blog_posts_paginator.page(page)
            except PageNotAnInteger:
                blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
            except EmptyPage:
                blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

            context['blog_posts'] = blog_posts

            return render(request, "blog/bloglist.html", context)

        blog_posts = sorted(get_blog_queryset(query), key=attrgetter('updated_on'), reverse=True)
        


        # Pagination
        page = request.GET.get('page', 1)
        blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
        try:
            blog_posts = blog_posts_paginator.page(page)
        except PageNotAnInteger:
            blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
        except EmptyPage:
            blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

        context['blog_posts'] = blog_posts

        return render(request, "blog/bloglist.html", context)
    else:
          return redirect('login')
    

def AddComment(request,pk=None):

    if(request.method == 'GET'):
            comment_data=request.GET.get('comment',"")
            blog=Blog.objects.filter(pk=pk).first()
            print('comment',comment_data)
            commentIns=Comment(blog=blog,comment_by=request.user,comment=comment_data)
            if commentIns:
                commentIns.save()
    return redirect('blogdetail',pk=pk)


def AddTag(request,pk=None):

    if(request.method == 'GET'):
            tag_query=request.GET.get('tag',"")
            blog=Blog.objects.filter(pk=pk).first()
            print('comment',tag_query)
            tagIns=Tag(blog=blog,tag_content=tag_query)
            if tagIns:
                tagIns.save()
            print(tag_query,'tag')

    return redirect('blogdetail',pk=pk)

def LikeComment(request,pk=None):

    if(request.method == 'GET'):
            like_query=request.GET.get('islike',"")
            comment=Comment.objects.filter(pk=pk).first()
            print('comment',comment)
            like_ins=Like.objects.filter(liked_by=request.user)
            if like_ins.count()>0:
                 like_ins.like=like_query
                 like_ins.save()
            else:
                 likeIns=Like(comment=comment,liked_by=request.user,like=like_query)
            if likeIns:
                likeIns.save()
            print(like_query,'like query')

    return redirect('blogdetail',pk=pk)



def ShareBlog(request):
     if request.method=="POST":
        from_mail=request.POST.get('from_mail')
        to_mail=request.POST.get('to_mail')
        msg_body=request.POST.get('msg_body')

        send_mail("Blog Share","Here is the message.","from@example.com",["to@example.com"],fail_silently=False,)
