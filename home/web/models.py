from django.db import models


# Create your models here.
class Title(models.Model):
    rep_id = models.AutoField(primary_key=True)
    rep_url = models.CharField(max_length=500)
    rep_title = models.CharField(max_length=500)
    publish_date = models.CharField(max_length=50)
    pages = models.IntegerField()
    rep_category_id = models.CharField(max_length=10)

    def __str__(self):
        return self.rep_title


class Datatable(models.Model):
    data_id = models.AutoField(primary_key=True)  # This should be auto-generated
    rep_id = models.ForeignKey(Title, on_delete=models.CASCADE)  # Foreign key to Title
    overview = models.TextField()
    table_content = models.TextField()
    list_content = models.TextField()

    def __str__(self):
        return f'Data for Report: {self.rep_id}'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)  # Change cat_name to category_name
    rep_category_id = models.CharField(max_length=10, null=True, blank=True)  # Allow null values for existing data

    def __str__(self):
        return self.category_name


class Report_price(models.Model):
    price_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=60)
    price = models.CharField(max_length=20)

    def __str__(self):
        return self.label


class Cart(models.Model):
    rep_id = models.ForeignKey(Title, on_delete=models.CASCADE)  # Link to Title model
    rep_title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.rep_title} - {self.label} - {self.price}'
