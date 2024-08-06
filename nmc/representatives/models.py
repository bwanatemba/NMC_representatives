from django.db import models


class County(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='wards')

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Representative(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    id_number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.name
