from flask import render_template, request, redirect, url_for
from flask_security import login_required, current_user

from models.models import Post, Tag, Category
from models import db
from utils.utils import get_option_value
from .forms import PostForm
from . import blog


@blog.route('/search/<query>')
def post_search(query):
    q = request.args.get('q')
    if q:
        return redirect(url_for('blog.post_search', query=q))
    posts = db.session.execute(db.select(Post).filter(
            Post.title.contains(query) | Post.text.contains(query)
    )).scalars().all()
    return render_template('blog/post_search.html', posts=posts, favicon=get_option_value('favicon'),
                            blog_title=get_option_value('title'), query=query)

@blog.route('/')
def index():
    q = request.args.get('q')
    if q:
        return redirect(url_for('blog.post_search', query=q))

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    page = db.paginate(db.select(Post).order_by(Post.created.desc()), page=page,
                       per_page=int(get_option_value('posts_per_page')))

    return render_template('blog/posts.html', page=page, favicon=get_option_value('favicon'),
                           max=max, min=min, blog_title=get_option_value('title'))

@blog.route('/<slug>')
def post_detail(slug):
    q = request.args.get('q')
    if q:
        return redirect(url_for('blog.post_search', query=q))

    post = db.one_or_404(db.select(Post).filter_by(slug=slug))
    category = db.one_or_404(db.select(Category).filter_by(id=post.category_id))
    return render_template('blog/post_detail.html', post=post, category=category,
                           blog_title=get_option_value('title'), favicon=get_option_value('favicon'))

@blog.route('/tags/<slug>')
def tag_detail(slug):
    q = request.args.get('q')
    if q:
        return redirect(url_for('blog.post_search', query=q))
    tag = db.one_or_404(db.select(Tag).filter_by(slug=slug))
    return render_template('blog/tag_detail.html', tag=tag, title=tag.name,
                           blog_title=get_option_value('title'), favicon=get_option_value('favicon'))

@blog.route('/categories/<id>')
def category_detail(id):
    q = request.args.get('q')
    if q:
        return redirect(url_for('blog.post_search', query=q))
    category = db.one_or_404(db.select(Category).filter_by(id=id))
    return render_template('blog/category_detail.html', category=category, title=category.name,
                           blog_title=get_option_value('title'), favicon=get_option_value('favicon'))

# @blog.route('/create', methods=['POST', 'GET'])
# @login_required
# def post_create():
#     form = PostForm() 
    
#     if request.method == 'POST':
#         title = request.form.get('title')
#         text = request.form.get('text')
        
#         try:
#             post = Post(title=title, text=text)
#             db.session.add(post)
#             db.session.commit()
#             return redirect(url_for('posts.post_detail', slug=post.slug))
#         except:
#             print('cannot create a post!!!')

#     return render_template('blog/post_create.html', form=form, blog_title=get_option_value('title'))

# @blog.route('/<slug>/edit', methods=['POST', 'GET'])
# @login_required
# def post_update(slug):
#     q = request.args.get('q')
#     if q:
#         return redirect(url_for('blog.post_search', query=q))
#     post = db.one_or_404(db.select(Post).filter_by(slug=slug))

#     if request.method == 'POST':
#         form = PostForm(formdata=request.form, obj=post)
#         form.populate_obj(post)
#         db.session.commit()
#         return redirect(url_for('blog.post_detail', slug=post.slug))
    
#     form = PostForm(obj=post)
#     return render_template('blog/post_edit.html', post=post, form=form,
#                            blog_title=get_option_value('title'), favicon=get_option_value('favicon'))
