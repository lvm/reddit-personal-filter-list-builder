# server.py
import datetime
from flask import Flask, render_template, request

# Adblock/UBlock Filters
FILTER_SUBREDDIT = """! Blocks /r/{replace}
||reddit.com/r/{replace}^$document"
reddit.com##div[data-subreddit="{replace}"]

"""

FILTER_USERNAME = """! Blocks /u/{replace}
! Comments on New Reddit
reddit.com#?#.Comment:-abp-has(a[href="/user/{replace}"])
! Posts on New Reddit
reddit.com#?#.Post:-abp-has(a[href="/user/{replace}"])
! Comments on Old Reddit
reddit.com#?#.entry:-abp-has(a[href="/user/{replace}"])
! Posts on Old Reddit
reddit.com#?#.thing[data-author="/user/{replace}"])
! Comments on Reddit Mobile
reddit.com#?#article:-abp-has(.PostHeader__author-link[href="/user/{replace}"])
! Posts on Reddit Mobile
reddit.com#?#.Comment:-abp-has(.CommentHeader__username:-abp-contains(/^{replace}$/))

"""

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


def build_filter(data, template):
    data = list(map(lambda s: s.strip(), data.split(",")))
    clean_r = lambda s: s.replace("/r/", "")
    clean_usr = lambda s: s.replace("/user/", "").replace("/u/", "")

    response = ""
    for value in data:
        value = clean_r(value)
        value = clean_usr(value)
        response += template.format(replace=value)

    return response


@app.route('/filter', methods=['POST'])
def create_filterlist():
    filter_subreddit = ""
    filter_username = ""

    if request.form.get('subreddit', None):
        filter_subreddit = build_filter(
            request.form.get('subreddit'),
            FILTER_SUBREDDIT
        )

    if request.form.get('username', None):
        filter_username = build_filter(
            request.form.get('username'),
            FILTER_USERNAME
        )

    response = """
! [Adblock Plus / Ublock Origins]
! Title: ⛔ Reddit Personal Filter list.
! Version: {today}v0.23
!
! Built using https://reddit-personal-filter-list-builder.glitch.me/

{filter_subreddit}
{filter_username}
""".format(today=datetime.datetime.now().strftime("%d%b%Y"),
           filter_subreddit=filter_subreddit,
           filter_username=filter_username)

    return response

if __name__ == "__main__":
    from os import environ
    app.run(host='0.0.0.0', port=int(environ['PORT']))
