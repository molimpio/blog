from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm
from .models import Post


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a pagina nao for um inteiro exibe a primeira
        posts = paginator.page(1)
    except EmptyPage:
        # Se a pagina estiver fora do intervalo
        # Exibe a ultima pagina de resultados
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Obtem a postagem com base no id
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False

    if request.method == 'POST':
        # Form submited
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos do form passaram pela validacao, cleaned_data obtem os valores do form
            cd = form.cleaned_data
            # Envia e-mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomenda a leitura de f{post.title}"
            message = f"Leitura do {post.title} as {post_url}\n\n f{cd['name']} \'s comments: {cd['comments']}"
            send_mail(subject, message, 'noreplyunnepay@gmail.com', [cd['to']])
            send = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'send': send})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
