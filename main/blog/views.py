from django.shortcuts import render

from blog.models import BlogSettings, Post

def blog(request):
  articles = Post.objects.filter(status=True)
  try:
    setup = BlogSettings.objects.get()
  except:
    setup = BlogSettings()
  
  context = {
    "articles": articles,
    "setup": setup
  }
  return render(request, "pages/blog/blog.html", context)

def blog_detail(request, slug):
  pass

def post(request, slug):
  article = Post.objects.get(slug=slug) 
  articles = Post.objects.filter(status=True).exclude(slug=slug)
  viewed_articles = request.session.get('viewed_articles', [])
    
  # Проверяем, просматривал ли пользователь эту статью ранее.
  if slug not in viewed_articles:
      # Увеличиваем счетчик просмотров, если статья просматривается впервые.
      article.view_count += 1
      article.save()
      
      # Добавляем идентификатор статьи в список просмотренных.
      viewed_articles.append(slug)
      
      # Обновляем сессию, сохраняя в ней обновленный список.
      request.session['viewed_articles'] = viewed_articles
      
  
  context = {
    "article": article,
    "articles": articles,
  }
  
  return render(request, "pages/blog/blog_detail.html", context)