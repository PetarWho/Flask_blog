import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session, current_app
from app.models import Post, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt

from app.decorators import jwt_required

main = Blueprint('main', __name__)

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/")
@jwt_required
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    # Pass the current user to the template
    token = session.get("jwt_token")
    payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = payload.get("user_id")
    user = User.query.get_or_404(user_id)
    return render_template("index.html", posts=posts, user=user, title="Home")

@main.route("/post/<string:post_id>")
@jwt_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    token = session.get("jwt_token")
    payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = payload.get("user_id")
    user = User.query.get_or_404(user_id)
    post.views_count += 1
    post.save()
    return render_template("post.html", post=post, user=user, title=post.title)

@main.route("/new_post", methods=["GET", "POST"])
@jwt_required
def new_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        # Retrieve the current user from the JWT payload; here we simply use session["jwt_token"]
        token = session.get("jwt_token")
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        user_id = payload.get("user_id")

        cover_image_filename = None
        file = request.files.get("cover_image")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            cover_image_filename = filename
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
        
        new_post = Post(title=title, content=content, cover_image=cover_image_filename, user_id=user_id)
        new_post.save()
        flash("Post created successfully!", "success")
        return redirect(url_for("main.index"))
    
    return render_template("new_post.html", title="New Post")

@main.route("/post/<string:post_id>/edit", methods=["GET", "POST"])
@jwt_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    token = session.get("jwt_token")
    payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = payload.get("user_id")
    user = User.query.get_or_404(user_id)

    # Ensure the current user is the author of the post
    if post.user_id != user.id:
        abort(403)  # Forbidden access

    if request.method == "POST":
        post.title = request.form.get("title")
        post.content = request.form.get("content")
        file = request.files.get("cover_image")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            post.cover_image = filename
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
        post.save()
        flash("Post updated successfully!", "success")
        return redirect(url_for("main.post_detail", post_id=post.id))

    return render_template("edit_post.html", post=post, title="Edit Post")

@main.route("/post/<string:post_id>/delete", methods=["POST"])
@jwt_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    token = session.get("jwt_token")
    payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = payload.get("user_id")
    user = User.query.get_or_404(user_id)

    # Ensure the current user is the author of the post
    if post.user_id != user.id:
        abort(403)  # Forbidden access

    post.delete()

    flash("Post deleted successfully!", "success")
    return redirect(url_for("main.index"))

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if user already exists
        user = User.query.filter((User.email==email) | (User.username==username)).first()
        if user:
            flash("User with that email or username already exists.", "danger")
            return redirect(url_for("main.register"))
        
        # Create a new user with a hashed password
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        new_user.save()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("main.login"))
    
    return render_template("register.html", title="Register")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # Generate a JWT token valid for 1 hour
            payload = {
                "user_id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24)
            }

            token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
            session["jwt_token"] = token
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("main.login"))
    
    return render_template("login.html", title="Login")

@main.route("/logout")
@jwt_required
def logout():
    session.pop("jwt_token", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.login"))
