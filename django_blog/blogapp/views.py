from django.shortcuts import render, redirect
from .models import Banner, Post, FriendlyLink, BlogCategory, Comment, Tags
from django.views.generic.base import View
from django.db.models import Q
from django.core.urlresolvers import reverse


# 基于类的视图
class SearchView(View):

    # post  get
    def post(self, request):
        # 如果要搜索的话  前段必然是要传一个关键字进来
        # 　根据这个关键字　去　　数据库里面查找
        kw = request.POST.get('keyword')
        # 拿到这个keyword就要　　去数据库里面找

        #  你要找什么　　　找博客名字＋博客内容
        # Q
        post_list = Post.objects.filter(Q(title__contains=kw) | Q(content__contains=kw))

        ctx = {
            'post_list': post_list
        }

        return render(request, 'search_list.html', ctx)


def blog_list(request, tid):
    # 说白了　　这个bloglist这个视图函数的第二个参数　　我们用来做判断
    # 　如果传过来的是０　　表示　默认的列表页面
    #  如果传过来的不是０　　传过来　是一个具体的数字　　　这个数字　表示的数据库里面的那个标签的ｉｄ

    b_list = []
    # 判断　　
    if tid != '0':
        #  get 是　获取标签　　　　　　id = tid 　
        tag = Tags.objects.get(id=tid)
        #  已经找到标签　　　通过标签　找这个标签下面的所有博客
        # 一对多关系　　　１的那一方　直接去调用多的一方　　　　一的那一方.多的那一方__set
        b_list = tag.post_set.all()

        pass
    else:
        # list页面　　是找所有的博客
        b_list = Post.objects.all()

    # 标签云 找到所有标签不为空的博客
    # tag_list = Post.objects.filter(tags__name__isnull=False)

    # 取出所有标签
    tag_list = Tags.objects.all()

    ctx = {
        'blog_list': b_list,
        'new_comment_list': get_new_comment_list(),
        'tag_list': tag_list
    }

    return render(request, 'list.html', ctx)


# 基于函数的视图
# Create your views here.
def index(request):
    # 取出所有的幻灯片
    banner_list = Banner.objects.all()
    # 取出所有被推荐的博客
    recomment_list = Post.objects.filter(recommend=True)
    # 取出所有博客  按照时间倒叙排列
    post_list = Post.objects.order_by('-pub_date').all()

    # 取出友情链接
    friend_link = FriendlyLink.objects.all()

    # 取出博客分类里面的数据
    categary_list = BlogCategory.objects.all()

    ctx = {
        'banner_list': banner_list,
        'recomment_list': recomment_list,
        'post_list': post_list,
        'friend_list': friend_link,
        'categary_list': categary_list,
        'new_comment_list': get_new_comment_list()
    }

    return render(request, 'index.html', ctx)


def comment_post(request):
    # 取到昵称
    nickname = request.POST.get('nickname')
    # 取到邮箱
    email = request.POST.get('email')
    # 取到评论内容
    comment = request.POST.get('comment-textarea')

    # 拿到博客的id
    blog_id = request.POST.get('post_id')

    # 假设我这个评论　邮箱可以不填　　昵称和　内容必须填
    if nickname is not None and comment is not None:
        cm = Comment.objects.get(pk=1)
        cm.post.id = blog_id
        cm.user.nickname = nickname
        cm.content = comment
        cm.save()
    else:
        pass

    # 重定向

    # return redirect('blogapp:show', page=blog_id)

    return redirect(reverse('blogapp:show', args=(blog_id,)))


# 详情页
def show(request, page):
    # page  其实就是博客id
    page = int(page)
    blog = Post.objects.get(id=page)
    # 记录浏览量
    blog.views += 1
    blog.save()

    # 推荐相关博文－－－－＞　你的需求　　我现在的逻辑　　只要　字一样　就推荐

    # 博客标题
    kw = blog.title
    # 去数据库里面找　　　但是我现在找逻辑是这样: 其他文章标题　或者　内容　　里面
    recomment_list = Post.objects.filter(Q(title__contains=kw) | Q(content__contains=kw))

    # 去重
    # recomment_list = list(recomment_list).remove(blog)

    recomment_list1 = []
    for p in recomment_list:
        if p.id == blog.id:
            pass
        else:
            recomment_list1.append(p)

    # 找到　当前这篇博客下面的评论
    comment_list = Comment.objects.filter(post__id=blog.id)

    ctx = {
        'blog': blog,
        'new_comment_list': get_new_comment_list(),
        'recomment_list': recomment_list1,
        'comment_list': comment_list
    }

    return render(request, 'show.html', ctx)


def get_new_comment_list():
    # 最新评论文章
    new_comment_list = Post.objects.filter(comment__content__isnull=False).order_by('-pub_date')

    new_comment_list2 = []

    # 循环遍历我们之前取出来的博客　　
    # 然后每一次取出来的博客我们进行一次判断　如果在新列表存在　那就是重复
    for post in new_comment_list:
        if post in new_comment_list2:
            pass
        else:
            new_comment_list2.append(post)

    return new_comment_list2
