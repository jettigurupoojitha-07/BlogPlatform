from app import app, db, Blog

with app.app_context():
    blogs = Blog.query.all()

    for b in blogs:
        print(b.id, b.title)

    # delete all junk blogs manually
    for b in blogs:
        if b.title == "hytgct":
            db.session.delete(b)

    db.session.commit()
    print("Deleted junk blogs")