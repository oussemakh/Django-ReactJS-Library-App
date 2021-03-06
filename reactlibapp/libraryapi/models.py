from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProxy(User):
    """Class defined to create a proxy for the user model.

        Changes made to this model directly affects the User model
        and vice-versa. Model allows methods to be defined on the User model
        without altering the user model itself.
        https://docs.djangoproject.com/en/1.11/topics/db/models/
    """
    class Meta:
        proxy = True
        auto_created = True

    def check_diff(self, idinfo):
        """
        Check for differences between request/idinfo and model data.

            Args:
                idinfo: data passed in from post method.
        """
        data = {
                "username": idinfo['name'],
                "email" : idinfo["email"],
                "first_name" :idinfo['given_name'],
                "last_name" :idinfo['family_name']
            }
            
        for field in data:
            if getattr(self, field) != data[field] and data[field] != '':
                setattr(self, field, data[field])
        self.save()

class BaseInfo(models.Model):
    """Base class containing all models common information."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Define Model as abstract."""

        abstract = True


class GoogleUser(models.Model):
    google_id = models.CharField(max_length=60, unique=True)

    app_user = models.OneToOneField(User, related_name='user',
                                    on_delete=models.CASCADE)
    appuser_picture = models.TextField()


    def check_diff(self, idinfo):
        """Check for differences between request/idinfo and model data.
            Args:
                idinfo: data passed in from post method.
        """
        data = {
                "appuser_picture": idinfo['picture']
            }

        for field in data:
            if getattr(self, field) != data[field] and data[field] != '':
                setattr(self, field, data[field])
        self.save()


    def __unicode__(self):
        return "%s %s" % (self.app_user.first_name,
                          self.app_user.last_name)


class Author(BaseInfo):
    """Book author models defined."""

    name = models.CharField(max_length=200)

    class Meta:
        """Define odering below."""

        ordering = ['name']

    def __unicode__(self):
        return "{}" .format(self.name)


class Category(BaseInfo):
    """Book category model defined."""

    name = models.CharField(max_length=200)

    class Meta:
        """Define odering below."""

        ordering = ['name']

    def __unicode__(self):
        return "Category : {}" .format(self.name)


class Book(BaseInfo):
    """Book model defined."""

    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    edition = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def _check_status(self):
        if self.quantity <= 0:
            return "Not Available"
        else:
            return "Available"
    status = property(_check_status)

    class Meta:
        """Define odering below."""

        ordering = ['title']

    def __unicode__(self):
        return "Book title: {}" .format(self.title)


class Ratings(BaseInfo):
    """Book review model defined."""

    comment = models.TextField()
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __unicode__(self):
        return "Review by user : {}" .format(self.user)


class History(BaseInfo):
    """User history model defined."""

    lending_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(auto_now_add=False,
                                       auto_now=False,
                                       blank=True, null=True)
    returned = models.BooleanField(default=False)

    def _expected_return_date(self):
        import datetime
        present_day = datetime.date.today()
        day_14 = datetime.timedelta(weeks=2)
        return_date = present_day + day_14
        return return_date

    exptdreturn_date = property(_expected_return_date)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return "History for user : {}" .format(self.user)


class Interest(BaseInfo):
    """User Interest Model defined."""

    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return "User {} interested in book {}" .format(self.user.username,
                                                       self.book.title)


class Quote(models.Model):
    """Model used to define homepage quotes"""

    author = models.CharField(max_length=100)
    statement = models.TextField()

    def __unicode__(self):
        return "{}" .format(self.author)
