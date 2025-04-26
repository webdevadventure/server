from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='cities'
    )

    def __str__(self):
        return f"{self.name}, {self.province.name}"

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'cities'

class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='districts'
    )

    def __str__(self):
        return f"{self.name}, {self.city.name}"

    class Meta:
        ordering = ['name']

class Ward(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='wards'
    )

    def __str__(self):
        return f"{self.name}, {self.district.name}"

    class Meta:
        ordering = ['name']

class Street(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        related_name='streets'
    )

    def __str__(self):
        return f"{self.name}, {self.ward.name}"

    class Meta:
        ordering = ['name']

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ] 