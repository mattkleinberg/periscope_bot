import praw
import prawoauth2
from oauth import app_key, app_secret, access_token, refresh_token


class RedditBot:
    def __init__(self):
        self.r = praw.Reddit('Periscope youtube converter test by /u/periscope_thing v1.0')
        scopes = ['edit', 'identity','read', 'submit']
        self.o = prawoauth2.PrawOAuth2Mini(self.r, app_key=app_key,
                                           app_secret=app_secret,
                                           access_token=access_token,
                                           refresh_token=refresh_token,
                                           scopes=scopes)

    def reddit_search(self):
        url_list = []
        try:
            subreddit = self.r.get_subreddit('criticalrole')
            print('bot is running')
            subreddit.refresh()

            for post in subreddit.get_hot(limit=10):
                if post.is_self is False:
                    if 'periscope' in post.url:
                        # check to see if the bot has already been to this post/posted to this post
                        # follow link to get video
                        post_id = post.id
                        url = post.url
                        print('periscope found: ' + url)
                        # When video is done downloading post to reddit thread with link to youtube video???
                        # check for if the url is already in the list
                        url_list.append(url)
                    else:
                        print('not periscope url: ' + post.url)
                        # check for if the url is already in the list (though shouldnt need it here)
                        url_list.append(post.url)
        except praw.errors.OAuthInvalidToken:
            self.o.refresh()

        return url_list

if __name__ == '__main__':
    testing = RedditBot()
    testing.reddit_search()
