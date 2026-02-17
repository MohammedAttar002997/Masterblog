from flask import Flask,render_template
import json
app = Flask(__name__)


with open('blog_post.json') as f:
    blog_posts = json.load(f)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)