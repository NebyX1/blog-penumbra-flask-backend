from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, login_required, LoginManager
from helpers.forms import LoginForm, PostForm
from database.models import Admin, Post
from database.db import db

login_manager = LoginManager()


def init_app(app: Flask):

    login_manager.init_app(app)

    # Página de inicio, muestra todos los posts
    @app.route("/")
    @app.route("/index")
    @app.route("/home")
    def home_page():
        posts = Post.query.order_by(Post.date.desc()).all()
        return render_template('index.html', posts=posts)

    # Página de inicio de sesión, maneja el login de administradores
    @app.route("/login", methods=['GET', 'POST'])
    def login_page():
        form = LoginForm()
        if form.validate_on_submit():
            attempted_user = Admin.query.filter_by(name=form.name.data).first()
            if attempted_user and attempted_user.check_password(password_attempt=form.password.data):
                login_user(attempted_user)
                flash(f'You are logged in as: {attempted_user.name}', category='success')
                return redirect(url_for('home_page'))
            else:
                flash('Username or password incorrect', category='danger')
        return render_template('login.html', form=form)

    # Maneja el cierre de sesión de administradores
    @app.route("/logout")
    def logout_page():
        logout_user()
        flash('You are now Logged Out, See you soon!', category='info')
        return redirect(url_for('home_page'))

    # Página para crear un nuevo post
    @app.route("/admin/create", methods=['GET', 'POST'])
    @login_required
    def create_post():
        form = PostForm()
        if form.validate_on_submit():
            try:
                new_post = Post(
                    author=form.author.data,
                    title=form.title.data,
                    image=form.image.data,
                    content=form.content.data
                )
                db.session.add(new_post)
                db.session.commit()
                flash('Post created successfully', category='success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating post: {str(e)}', category='error')
            return redirect(url_for('create_post'))

        return render_template('create-post.html', form=form)

    # Página para borrar un post existente con paginación
    @app.route("/admin/erase", methods=['GET', 'POST'])
    @login_required
    def erase_post():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=20)
        return render_template('erase-post.html', posts=posts)

    # Endpoint para eliminar un post
    @app.route("/admin/delete_post/<int:post_id>", methods=['POST'])
    @login_required
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully', category='success')
        else:
            flash('Post not found', category='error')
        return redirect(url_for('erase_post'))

    # Página para listar los posts a editar
    @app.route("/admin/edit", methods=['GET'])
    @login_required
    def edit_post():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=20)
        return render_template('edit-post.html', posts=posts)

    # Página para modificar un post existente
    @app.route("/admin/mod_post/<int:post_id>", methods=['GET', 'POST'])
    @login_required
    def mod_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            flash('Post not found', category='error')
            return redirect(url_for('edit_post'))

        form = PostForm(obj=post)
        if form.validate_on_submit():
            post.author = form.author.data
            post.title = form.title.data
            post.image = form.image.data
            post.content = form.content.data
            db.session.commit()
            flash('Post updated successfully', category='success')
            return redirect(url_for('edit_post'))

        return render_template('mod-post.html', form=form, post=post)

    # Maneja el error 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template('notfound.html')

    # Carga un usuario por su ID
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Maneja accesos no autorizados
    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template('forbidden.html')

    # Endpoint API para obtener todos los posts
    @app.route("/api/posts", methods=['GET'])
    def get_posts():
        posts = Post.query.all()
        return jsonify([post.serialize() for post in posts])

    # Endpoint API para obtener un post por ID
    @app.route("/api/posts/<int:post_id>", methods=['GET'])
    def get_post(post_id):
        post = Post.query.get(post_id)
        if post:
            return jsonify(post.serialize())
        else:
            return jsonify({"error": "Post not found"}), 404
