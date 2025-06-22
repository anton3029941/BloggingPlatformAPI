from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=True)
    tags = db.Column(JSON, nullable=True, default=list)
    createTime = db.Column(db.DateTime, default=datetime.now)
    updateTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content,
                "category": self.category, "tags": self.tags,
                 "createTime": self.createTime.strftime('%Y-%m-%d %H:%M:%S'), "updateTime": self.updateTime.strftime('%Y-%m-%d %H:%M:%S')}

@app.route('/posts', methods=['GET'])
def get_posts():
    term = request.args.get('term')
    if term:
        # If search term is provided, filter by title or content (case-insensitive)
        posts = Post.query.filter(
            or_(
                Post.title.ilike(f"%{term}%"),
                Post.category.ilike(f"%{term}%"),
                Post.tags.contains(term),
            )
        ).all()
    else:
        # Otherwise, return all posts
        posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    print(data)
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    new_post = Post(title=data['title'], content=data['content'],
                    category=data.get('category', 'None'), tags=data.get('tags', []))
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully', 'data': new_post.to_dict()}), 201


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    post = Post.query.get_or_404(post_id)
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.category = data.get('category', post.category)
    post.tags = data.get('tags', post.tags)
    db.session.commit()

    return jsonify({'message': 'Post updated successfully', 'data': data}), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': f'Post {post_id} deleted successfully'}), 200

with app.app_context():
    db.create_all()

app.run()