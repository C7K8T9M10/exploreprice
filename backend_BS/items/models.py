from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, unique=True)
    def __str__(self):
        return self.name


class SavedItem(models.Model):
    user = models.ForeignKey('auth.User', related_name='saved_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='saved_by_users', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username} saved {self.item.name}"

class PriceHistory(models.Model):
    item = models.ForeignKey(Item, related_name='price_histories', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.item.name} - {self.price} on {self.date}"

class PriceImg(models.Model):
    item = models.ForeignKey(Item, related_name='price_imgs', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='price_imgs/')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.item.name} - {self.date}"