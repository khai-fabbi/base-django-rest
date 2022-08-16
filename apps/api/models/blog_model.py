from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL


class BaseAction(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BaseItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseItem):
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]
        db_table = "tbl_category"

    @classmethod
    def save(self, *args, **kwargs):
        if self.name is not None or self.name != "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(BaseItem):
    content = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        ordering = ["name"]
        db_table = "tbl_tag"


class Post(BaseItem):
    title = models.CharField(max_length=255, default="")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="post_category"
    )
    is_hot = models.BooleanField(default=False)
    view = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    slug = models.SlugField(unique=True)
    tag = models.ManyToManyField(Tag, blank=True, null=True, related_name="tags")
    content = models.TextField(default="")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_post"
    )
    published = models.DateField("Published", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published"]
        db_table = "tbl_post"

    @classmethod
    def save(self, *args, **kwargs):
        if self.title is not None or self.title != "":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductComment(BaseAction):
    content = models.TextField(default=None)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment_post"
    )

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.post.name


class Action(BaseAction):
    like, haha, angry = range(0, 3)
    actions = [(like, "like"), (haha, "haha"), (angry, "angry")]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="action")
    type = models.PositiveSmallIntegerField(choices=actions, default=like)


class Rating(BaseAction):
    rate = models.PositiveSmallIntegerField(
        blank=True, validators=[MaxValueValidator(5)]
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="rating_post")

    def __str__(self):
        return self.rate
