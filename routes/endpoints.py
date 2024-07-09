from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, login_required, LoginManager
from helpers.forms import LoginForm, PostForm, JournalForm
from database.models import Admin, Post, Journal
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
        journals = Journal.query.order_by(Journal.date.desc()).all()
        return render_template('index.html', posts=posts, journals=journals)

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
                    category=form.category.data,
                    slug=form.slug.data,
                    image=form.image.data,
                    content=form.content.data
                )
                db.session.add(new_post)
                db.session.commit()
                flash('Post created successfully', category='success')
                return redirect(url_for('create_post'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating post: {str(e)}', category='danger')
        else:
            # Flash form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in the {getattr(form, field).label.text} field - {error}", category='danger')

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

    # Página para editar un post
    @app.route("/admin/mod_post/<int:post_id>", methods=['GET', 'POST'])
    @login_required
    def mod_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            flash('Post not found', category='error')
            return redirect(url_for('edit_post'))

        form = PostForm(obj=post)
        if form.validate_on_submit():
            # Validar la unicidad del slug
            existing_post = Post.query.filter_by(slug=form.slug.data).first()
            if existing_post and existing_post.id != post.id:
                flash('Slug must be unique. This slug is already in use.', category='error')
            else:
                post.author = form.author.data
                post.title = form.title.data
                post.category = form.category.data
                post.slug = form.slug.data
                post.image = form.image.data
                post.content = form.content.data
                db.session.commit()
                flash('Post updated successfully', category='success')
                return redirect(url_for('edit_post'))

        return render_template('mod-post.html', form=form, post=post)

    # Página para crear un nuevo journal
    @app.route("/admin/create-journal", methods=['GET', 'POST'])
    @login_required
    def create_journal():
        form = JournalForm()
        if form.validate_on_submit():
            try:
                new_journal = Journal(
                    date=form.date.data,
                    number=form.number.data,
                    year=form.year.data,
                    title=form.title.data,
                    url=form.url.data,
                    image=form.image.data
                )
                db.session.add(new_journal)
                db.session.commit()
                flash('Journal created successfully', category='success')
                return redirect(url_for('create_journal'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating journal: {str(e)}', category='danger')
        else:
            # Flash form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in the {getattr(form, field).label.text} field - {error}", category='danger')

        return render_template('create-journal.html', form=form)

    # Página para borrar un journal existente
    @app.route("/admin/erase-journal", methods=['GET', 'POST'])
    @login_required
    def erase_journal():
        page = request.args.get('page', 1, type=int)
        journals = Journal.query.order_by(Journal.date.desc()).paginate(page=page, per_page=20)
        return render_template('erase-journal.html', journals=journals)

    # Endpoint para eliminar un journal
    @app.route("/admin/delete_journal/<int:journal_id>", methods=['POST'])
    @login_required
    def delete_journal(journal_id):
        journal = Journal.query.get(journal_id)
        if journal:
            db.session.delete(journal)
            db.session.commit()
            flash('Journal deleted successfully', category='success')
        else:
            flash('Journal not found', category='error')
        return redirect(url_for('erase_journal'))

    # Página para editar un journal
    @app.route("/admin/edit-journal", methods=['GET'])
    @login_required
    def edit_journal():
        page = request.args.get('page', 1, type=int)
        journals = Journal.query.order_by(Journal.date.desc()).paginate(page=page, per_page=20)
        return render_template('edit-journal.html', journals=journals)

    # Página para modificar un journal existente
    @app.route("/admin/mod_journal/<int:journal_id>", methods=['GET', 'POST'])
    @login_required
    def mod_journal(journal_id):
        journal = Journal.query.get(journal_id)
        if not journal:
            flash('Journal not found', category='error')
            return redirect(url_for('mod-journal'))

        form = JournalForm(obj=journal)
        if form.validate_on_submit():
            journal.date = form.date.data
            journal.number = form.number.data
            journal.year = form.year.data
            journal.title = form.title.data
            journal.url = form.url.data
            journal.image = form.image.data
            db.session.commit()
            flash('Journal updated successfully', category='success')
            return redirect(url_for('edit_journal'))

        return render_template('mod-journal.html', form=form, journal=journal)

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

    @app.route("/api/posts/slug/<string:slug>", methods=['GET'])
    def get_post_by_slug(slug):
        post = Post.query.filter_by(slug=slug).first()
        if post:
            return jsonify(post.serialize())
        else:
            return jsonify({"error": "Post not found"}), 404

    # Endpoint API para obtener todos los journals
    @app.route("/api/journals", methods=['GET'])
    def get_journals():
        journals = Journal.query.all()
        return jsonify([journal.serialize() for journal in journals])

    # Endpoint API para obtener un journal por ID
    @app.route("/api/journals/<int:journal_id>", methods=['GET'])
    def get_journal(journal_id):
        journal = Journal.query.get(journal_id)
        if journal:
            return jsonify(journal.serialize())
        else:
            return jsonify({"error": "Journal not found"}), 404
