import urllib.request
import os

from flask import request, render_template, send_from_directory, url_for
from pybooru import Danbooru, Moebooru

from app.posts import bp


client = Moebooru('konachan') # change this to be a list of clients from user config
danbooru = False # do we want to serve these guys?

def download_posts(tags, page):
    postList = client.post_list(tags=tags, limit=50, page=page) # change the limit to be user defined from config
    posts = []
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
    ordered_set_of_tags = sorted(list(set(list_of_tags)))
    return (ordered_set_of_tags, posts)


@bp.route('', methods=['GET'])
def serve_posts():
    tags = request.args.get('tags',"", type=str)
    page = request.args.get('page', 1, type=int)
    page = 1 if page < 1 else page
    info = download_posts(tags, page)
    next_url = url_for('posts.serve_posts', tags = tags, page = page + 1)
    prev_url = url_for('posts.serve_posts', tags = tags, page = page - 1)

    return render_template('posts.html', site_name="YABA", posts=info[1], tags=info[0][:50], page=page,
        current_tags=tags, next_url=next_url, prev_url=prev_url)
