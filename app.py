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
        if list_of_json_data:
            data["id"] = max(post['id'] for post in list_of_json_data) + 1
        else:
            data["id"] = 1
        data["author"]= author
        data["title"] = title
        data["content"] = content

        list_of_json_data.append(data)

        write_json_file('blog_post.json', list_of_json_data)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>',methods=['POST'])
def delete(post_id):
    print(post_id)
    list_of_json_data = read_json_file('blog_post.json')
    removed_data = [d for d in list_of_json_data if d.get('id') != post_id]
    list_of_json_data = removed_data
    write_json_file('blog_post.json', list_of_json_data)
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    list_of_json_data = read_json_file('blog_post.json')
    # Find the post with the matching ID
    post_to_update = next((post for post in list_of_json_data if post['id'] == post_id), None)
    if post_to_update is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the dictionary values with form data
        post_to_update['author'] = request.form.get('author')
        post_to_update['title'] = request.form.get('title')
        post_to_update['content'] = request.form.get('content')

        write_json_file('blog_post.json', list_of_json_data)
        return redirect(url_for('index'))

    # For GET, render a form pre-filled with the current post data
    return render_template('update.html', post=post_to_update)


@app.route('/like/<int:post_id>', methods=['POST'])
def likes_increment(post_id):
    list_of_json_data = read_json_file('blog_post.json')
    # Find the post with the matching ID
    post_to_update = next((post for post in list_of_json_data if post['id'] == post_id), None)


    if request.method == 'POST':
        # Update the dictionary values with form data
        post_to_update['likes'] = post_to_update.get('likes',0) + 1

        write_json_file('blog_post.json', list_of_json_data)
    return redirect(url_for('index'))

    # For GET, render a form pre-filled with the current post data
    # return render_template('update.html', post=post_to_update)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)