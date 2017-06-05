import twitter


class User():
    def __init(self, **kwargs):
        def __init__(self):
            self.name = kwargs.get('name', '')
            self.screen_name = kwargs.get('screen_name', '')
            self.profile_image_url = kwargs.get('profile_image_url', '')


class Tweet(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.id = kwargs.get('id', '')
        self.created_at = kwargs.get('created_at', '')
        self.text = kwargs.get('text', '')
        self.user = kwargs.get('user')
        if self.user is None or not isinstance(self.user, User):
            self.user = User()

    def set_created_at(self, text):
        text = text.split()
        if len(text) > 2:
            self.created_at = text[0] + " " + text[1] + " " + text[2]
        else:
            self.created_at = 'N/A'


def search_for_mentions(term, count=20, max_id=None):
    api = twitter.Api(consumer_key='WpK8e6IYKfUonFm6B1PhhAoA3',
                      consumer_secret='jz4txZwz2CEc8x7z0lbVlfmuV1Sk6OZqVnzJUyDIgdXIOvDXUi', application_only_auth=True)
    results = api.GetSearch(term, count=count, max_id=max_id)
    tweets = list()
    for result in results:
        tweet = Tweet()
        tweet.set_created_at(result.created_at)
        tweet.id = int(result.id)
        tweet.text = result.text

        user = User()
        user.name = result.user.name
        user.profile_image_url = result.user.profile_image_url
        user.screen_name = result.user.screen_name

        tweet.user = user
        tweets.append(tweet)
    return tweets


def get_min_id(tweets):
    if len(tweets) == 0:
        return -1
    min_id = tweets[0].id
    for i in range(1, len(tweets)):
        tweet = tweets[i]
        min_id = min(min_id, tweet.id)
    return min_id


def get_max_id(tweets):
    if len(tweets) == 0:
        return -1
    max_id = tweets[0].id
    for i in range(1, len(tweets)):
        tweet = tweets[i]
        max_id = max(max_id, tweet.id)
    return max_id
