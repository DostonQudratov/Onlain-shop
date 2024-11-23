from django.db import models

class Categories(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="project-photos",
                              default='project-photos/project-default.png',
                              null=True,
                              blank=True)
    
    def __str__(self):
        return f'{self.title} - {self.description}'




class Product(models.Model):
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product-image',
                              default='product-photos/project-default.png',
                              null=True,
                              blank=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=10, blank=False)
    new_price = models.DecimalField(decimal_places=2, max_digits=10)
    create = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.title} - {self.description}-{self.old_price} - {self.new_price}'
    
