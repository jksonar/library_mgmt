from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag, blank=True)
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.title

class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(default=datetime.now() + timedelta(days=14))
    def fine_amount(self):
        today = date.today()
        if today > self.return_date:
            days_late = (today - self.return_date).days
            return days_late * 10  # Rs.10 per day
        return 0

    def __str__(self):
        return f'{self.book.title} issued to {self.user.username}'
