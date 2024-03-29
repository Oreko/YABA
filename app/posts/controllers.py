from flask import request, render_template, send_from_directory, url_for
from pybooru import Danbooru, Moebooru, PybooruHTTPError
from booru_extension import Safebooru, Gelbooru

from app.posts import bp

# Commas on the left for easy commenting
clients = [(Moebooru('konachan'), False)
           , (Moebooru('yandere'), False)
           , (Safebooru(), True)
           #,(Gelbooru(), True) # Currently, Gelbooru commonly 404s on its own images
           ]


def download_posts(tags, page):
    posts = []
    errors = []
    tag_count = {}
    for client, altbooru in clients:
        postList = []
        try:
            postList = client.post_list(tags=tags, limit=50, page=page) # change the limit to be user defined from config
        except PybooruHTTPError as err:
            errors.append("{0} error: {1}".format(client.site_url, err))
            continue
        
        list_of_tags = []
        
        for post in postList:
            tag_string = post['tags']
            list_of_tags.extend(tag_string.split(" "))
            if(altbooru == True):
                image_url = client.get_image_url(post)
                posts.append((image_url, image_url))
            else:
                posts.append((post["preview_url"], post["file_url"]))

        for tag in list_of_tags:
            if tag in tag_count:
                tag_count[tag] += 1
            else:
                tag_count[tag] = 1
    
    # Sort to have the highest count tags for a page first, then grab the top 50 tags
    ordered_set_of_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:50]

    # Return the list sorted alphabetically by tag name
    ordered_set_of_tags = [tag for tag, _ in sorted(ordered_set_of_tags)]
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

    return render_template('posts.html', site_name="YABA", posts=info[1], tags=info[0], page=page,
        current_tags=tags, tag_args=tag_args, next_url=next_url, prev_url=prev_url, errors=info[2])
