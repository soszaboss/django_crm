from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Like
from django.http import JsonResponse
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts_pro/main.html', context)


def load_data(request, number):
    # Get the ContentType for the Post model
    post_content_type = ContentType.objects.get_for_model(Post)
    comment_content_type = ContentType.objects.get_for_model(Comment)

    post_visible = 3
    upper = number
    lower = upper - post_visible
    size = Post.objects.all().count()

    posts = Post.objects.annotate(
        like_counts=Count('likes', filter=Q(likes__value=True)),
        unlike_counts=Count('likes', filter=Q(likes__value=False)),
        comment_counts=Count('comments')
    )[lower:upper]

    post_list = []
    for post_item in posts:
        post_items = {
            'id': post_item.id,
            'title': post_item.title,
            'description': post_item.description,
            'author': post_item.author.user.username,
            "liked": Like.objects.filter(content_type=post_content_type, object_id=post_item.id, value=True, user=request.user).exists(),# Now you can filter Like objects based on the content_type and object_id
            "unliked": Like.objects.filter(content_type=post_content_type, object_id=post_item.id, value=False, user=request.user).exists(),
            "liked_count": post_item.like_counts,
            "unliked_count": post_item.unlike_counts,
            "comments_count": post_item.comment_counts
        }

        comments_items_list = []
        all_comment = Comment.objects.filter(post=post_item)

        for comment_item in all_comment:
            comments_items = {
                "id": comment_item.id,
                "text": comment_item.text,
                "created_at": comment_item.created_at,
                "user": comment_item.user.username if comment_item.user else '',
                "liked": Like.objects.filter(content_type=comment_content_type, object_id=comment_item.id,value=True, user=request.user).exists(),
                "unliked": Like.objects.filter(content_type=comment_content_type, object_id=comment_item.id, value=False, user=request.user).exists(),
                "liked_count": Like.objects.filter(content_type=comment_content_type, object_id=comment_item.id, value=True).count(),
                "unliked_count": Like.objects.filter(content_type=comment_content_type, object_id=comment_item.id,value=False).count(),
                "subcomments": [{"user": replies.user.username, "text": replies.text, "created_at": replies.created_at,
                                 "liked": Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=replies.id,value=True, user=request.user).exists(),
                                 "unliked": Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=replies.id, value=False, user=request.user).exists(),
                                 "liked_count": Like.objects.filter(content_type=comment_content_type, object_id=replies.id, value=True).count(),
"unliked_count": Like.objects.filter(content_type=comment_content_type, object_id=replies.id, value=False).count(),
} for replies in comment_item.replies.all()]}
            comments_items_list.append(comments_items)

        post_items["comments"] = comments_items_list
        post_list.append(post_items)

    return JsonResponse({'post': post_list, 'size': size})


def like_post(request, id):
    if request.method == 'POST':
        #post = get_object_or_404(Post, id=id)
        post_content_type = ContentType.objects.get_for_model(Post)
        user_value, created = Like.objects.get_or_create(user=request.user, content_type=post_content_type, object_id=id)
        user_value.value = True
        user_value.save()
        posts = Post.objects.filter(id=id).annotate(
            like_counts=Count('likes', filter=Q(likes__value=True)),
            unlike_counts=Count('likes', filter=Q(likes__value=False)),
        ).first()
        return JsonResponse({'value': False, 'like_counts': posts.like_counts,
                             'unlike_counts': posts.unlike_counts, 'id': id})


def unlike_post(request, id):
    if request.method == 'POST' :#and request.user.is_authenticated:
        #post = get_object_or_404(Post, id=id)
        post_content_type = ContentType.objects.get_for_model(Post)
        user_value, created = Like.objects.get_or_create(user=request.user, content_type=post_content_type, object_id=id)
        user_value.value = False
        user_value.save()
        posts = Post.objects.filter(id=id).annotate(
            like_counts=Count('likes', filter=Q(likes__value=True)),
            unlike_counts=Count('likes', filter=Q(likes__value=False)),
        ).first()
        return JsonResponse({'value': False, 'like_counts': posts.like_counts,
                             'unlike_counts': posts.unlike_counts, 'id':id})