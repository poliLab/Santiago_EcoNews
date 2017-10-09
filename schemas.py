class Page():

    def __init__(self, url, parentUrl, level, title, links = [], tags = [], imgs = []):
        self.url = url
        self.parentUrl = parentUrl
        self.level = level
        self.title = title
        self.links = links
        self.tags = tags
        self.imgs = imgs

    def returnLikeObject(self):
        return {
            'url': self.url,
            'parentUrl': self.parentUrl,
            'level': self.level,
            'title': self.title,
            'links': self.links,
            'tags': self.tags,
            'imgs': self.imgs
        }

class PageNode():
    def __init__(self, url, level):
        self.url = url
        self.level = level
