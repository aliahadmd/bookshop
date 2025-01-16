from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True)
    pdf_file = models.FileField(upload_to='books/pdfs/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=100)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')