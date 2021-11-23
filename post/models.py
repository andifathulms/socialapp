from django.db import models
from django.utils import timezone

from urlextract import URLExtract

from account.models import Account

class Post(models.Model):
    body = models.TextField()
    image = models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(Account, blank=True, related_name='dislikes')
    shared_body = models.TextField(blank=True, null=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    tags = models.ManyToManyField('Tag', blank=True)
    has_url = models.BooleanField(default=False, blank=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        extractor = URLExtract()
        if extractor.has_urls(self.body):
            self.has_url = True

            urls = extractor.find_urls(self.body)
            self.url = urls[0]

            replaced = self.body.replace(self.url, " ")
            self.body = replaced

        super(Post, self).save(*args, **kwargs)

    def create_tags(self):
        for word in self.body.split():
            if (word[0] == '#'):
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

        if self.shared_body:
            for word in self.shared_body.split():
                if (word[0] == '#'):
                    tag = Tag.objects.filter(name=word[1:]).first()
                    if tag:
                        self.tags.add(tag.pk)
                    else:
                        tag = Tag(name=word[1:])
                        tag.save()
                        self.tags.add(tag.pk)
                    self.save()

    class Meta:
        ordering = ['-created_on', '-shared_on']

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Account, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(Account, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ManyToManyField('Image', blank=True)

    def create_tags(self):
        for word in self.comment.split():
            if (word[0] == '#'):
                tag = Tag.objects.get(name=word[1:])
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photos/', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=255)