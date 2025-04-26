from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from user_mgmt.models import User
from location.models import Province, District, Ward, Street

class PropertyType(models.TextChoices):
    ROOM = 'room', 'Room'
    APARTMENT = 'apartment', 'Apartment'
    HOUSE = 'house', 'House'

class ListingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class Listing(models.Model):
    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    property_type = models.CharField(
        max_length=10,
        choices=PropertyType.choices
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        related_name='listings'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name='listings'
    )
    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        related_name='listings'
    )
    street = models.ForeignKey(
        Street,
        on_delete=models.SET_NULL,
        null=True,
        related_name='listings'
    )
    specific_address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=ListingStatus.choices,
        default=ListingStatus.PENDING
    )
    posting_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

    class Meta:
        indexes = [
            models.Index(fields=['status', 'posting_date']),
            models.Index(fields=['property_type']),
        ]

class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.listing.title}"

class Review(models.Model):
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review_text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.tenant.email}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update landlord's average rating
            landlord = self.listing.landlord.landlord
            if landlord:
                ratings = Review.objects.filter(
                    listing__landlord=self.listing.landlord
                ).aggregate(
                    avg=Avg('rating'),
                    count=models.Count('id')
                )
                
                landlord.average_rating = ratings['avg'] or 0
                landlord.number_of_reviews = ratings['count'] or 0
                landlord.save()

    class Meta:
        unique_together = ['tenant', 'listing']
        indexes = [
            models.Index(fields=['rating']),
        ] 