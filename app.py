from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- BLOG MODEL ----------------

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- COMMENT MODEL ----------------

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- GET ALL BLOGS ----------------

@app.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = Blog.query.all()

    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "content": b.content,
            "created_at": b.created_at.strftime("%d-%m-%Y %I:%M %p")
        }
        for b in blogs
    ])

# ---------------- ADD BLOG ----------------

@app.route("/blogs", methods=["POST"])
def add_blog():
    data = request.json

    new_blog = Blog(
        title=data["title"],
        content=data["content"]
    )

    db.session.add(new_blog)
    db.session.commit()

    return jsonify({"message": "Blog added successfully"})

# ---------------- DELETE BLOG ----------------

@app.route("/blogs/<int:id>", methods=["DELETE"])
def delete_blog(id):
    blog = Blog.query.get(id)

    if blog:
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"message": "Blog deleted"})

    return jsonify({"message": "Blog not found"})

# ---------------- UPDATE BLOG ----------------

@app.route("/blogs/<int:id>", methods=["PUT"])
def update_blog(id):
    blog = Blog.query.get(id)

    if not blog:
        return jsonify({"message": "Blog not found"})

    data = request.json

    blog.title = data["title"]
    blog.content = data["content"]

    db.session.commit()

    return jsonify({"message": "Blog updated"})

# ---------------- ADD COMMENT ----------------

@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.json

    comment = Comment(
        content=data["content"],
        blog_id=data["blog_id"]
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully"})

# ---------------- GET COMMENTS ----------------

@app.route("/comments/<int:blog_id>", methods=["GET"])
def get_comments(blog_id):

    comments = Comment.query.filter_by(
        blog_id=blog_id
    ).all()

    return jsonify([
        {
            "id": c.id,
            "content": c.content
        }
        for c in comments
    ])
    
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    existing_user = User.query.filter_by(
        username=data["username"]
    ).first()

    if existing_user:
        return jsonify({
            "message": "Username already exists"
        })

    user = User(
        username=data["username"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })
    
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(
        username=data["username"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({
            "message": "Login successful"
        })

    return jsonify({
        "message": "Invalid username or password"
    })

# ---------------- START SERVER ----------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)