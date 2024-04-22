from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Define models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(db.String(200), nullable=True)
    posted_by = db.Column(db.String(50), nullable=False)

# Define routes
@app.route('/')
def index():
    banner_image_url = 'static/banner.png'
    posts = Post.query.all()
    return render_template('index.html', posts=posts, banner_image_url=banner_image_url)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        short_description = request.form['short_description']
        content = request.form['content']
        image_url = request.form['image_url']
        posted_by = request.form['posted_by']
        new_post = Post(title=title, short_description=short_description, content=content, image_url=image_url, posted_by=posted_by)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
