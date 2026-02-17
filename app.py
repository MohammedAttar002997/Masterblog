from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

def read_json_file(filename):
    with open(filename,"r") as f:
        blog_posts = json.load(f)
        return blog_posts


def write_json_file(filename,json_data):
    with open(filename,"w") as file:
        json.dump(json_data, file)
@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=read_json_file('blog_post.json'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    data = {}
    list_of_json_data = read_json_file('blog_post.json')
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        data['id'] = len(list_of_json_data)+1
        data["author"]= author
        data["title"] = title
        data["content"] = content
        list_of_json_data.append(data)
        write_json_file('blog_post.json', list_of_json_data)
        # Add the code that handles adding a new blog
        ...
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)