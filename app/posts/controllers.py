from flask import request, render_template, send_from_directory, url_for
from pybooru import Danbooru, Moebooru, PybooruHTTPError

from app.posts import bp

clients = [(Moebooru('konachan'), False), (Moebooru('yandere'), False)]
# (Danbooru(site_url='http://gelbooru.com'), True)

def download_posts(tags, page):
    posts = []
    errors = []
    tag_count = {}
    for client, danbooru in clients:
        postList = []
        try:
            postList = client.post_list(tags=tags, limit=50, page=page) # change the limit to be user defined from config
        except PybooruHTTPError as err:
            errors.append("{} error: {}".format(client.site_url, err))
        
        preview = ""
        full = "file_url"
        list_of_tags = []
        
        if (danbooru == True):
            preview = "preview_file_url"
        else:
            preview = "preview_url"
        
        for post in postList:
            tag_string = post['tags']
            list_of_tags.extend(tag_string.split(" "))
            posts.append((post[preview], post[full]))
        for tag in list_of_tags:
            if tag in tag_count:
                tag_count[tag] += 1
            else:
                tag_count[tag] = 1
    ordered_set_of_tags = sorted(tag_count, key=lambda x: x[1], reverse=True)
    ordered_set_of_tags = sorted(ordered_set_of_tags[:50])
    return (ordered_set_of_tags, posts, errors)

@bp.route('')
def serve_posts():
    tags = request.args.get('tags',"", type=str)
    tag_args = tags.replace(" ", "+")
    page = request.args.get('page', 1, type=int)
    page = 1 if page < 1 else page
    info = download_posts(tags, page)
    next_url = url_for('posts.serve_posts', tags = tags, page = page + 1)
    prev_url = url_for('posts.serve_posts', tags = tags, page = page - 1)

    return render_template('posts.html', site_name="YABA", posts=info[1], tags=info[0][:50], page=page,
        current_tags=tags, tag_args=tag_args, next_url=next_url, prev_url=prev_url, errors=info[2])
