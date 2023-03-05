from django.db import models


class DataArticle(models.Model):

    class Meta:
        db_table = "data_article"

    article = models.IntegerField()
    brand_name = models.CharField(max_length=200)
    product_title = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name
