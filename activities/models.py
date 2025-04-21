from django.db import models
from users.models import Member, Church
import uuid
import hashlib
from utils.img import image_resize



# Create your models here.

def generate_random_key() -> str:
    """Generate a random encrypted ID."""
    
    random_uuid = uuid.uuid4().hex  # Generate a random UUID
    return hashlib.sha256(random_uuid.encode()).hexdigest()[:16]





class Donation(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('NGN', 'Nigerian Naira'),
        ('GHS', 'Ghanaian Cedi'),
        # Add more currencies as needed
    ]

    PRIVACY_CHOICES = [
        ('YES', 'Visible'),
        ('NO', 'Encrypted'),
    ]

    HIDE_REASON_CHOICES = [
        ('ANONYMOUS', "I don't want anyone to know what I am offering/donating."),
        ('SMALL_AMOUNT', "My offering is too small."),
        ('BIG_AMOUNT', "I don't want to intimidate others with my big donation."),
        ('LIMIT_EXCEED', "I want to donate beyond the PIDES limit."),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)  # Linking to Django's User model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    privacy = models.CharField(max_length=3, choices=PRIVACY_CHOICES, default='YES')
    donation_key = models.CharField(max_length=255, blank=True, default= generate_random_key)  
    privacy_reason = models.CharField(max_length=20, choices=HIDE_REASON_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{'Anonymous' if self.privacy == 'NO' else self.donor.get_full_name()} donated {self.amount} {self.currency}"


    
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    theme = models.CharField(max_length=50)
    caption = models.CharField(max_length=150, blank=True)
    minister = models.CharField(max_length=150, blank= True)
    venue = models.CharField(max_length=50, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    new = models.BooleanField(default=True) 
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.theme



class PrayerRequest(models.Model):
    PRAYER_STATUS = (
        ('PRAYED_FOR', 'Prayer For'),
        ('PENDING', 'PENDING'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    sender = models.ForeignKey(Member, on_delete= models.CASCADE,related_name="sender")
    status = models.CharField(max_length=10, choices=PRAYER_STATUS, default="PENDING", blank=True)
    created_at = models.DateField(auto_now_add=True) 
    new = models.BooleanField(default=True) 

    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.content[:50]} - {self.sender.get_full_name()}"
    
    
class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published= models.BooleanField(default=True)
    content = models.CharField(max_length=150)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.content[:50]


class Post(models.Model):
    POST_CATEGORY = (
        ('SERMON', "Sermon"),
        ('TESTIMONY', "Testimony"),
        ('NEWS', "News"),
        ('GENERAL', "General"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="posts/", blank= True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now= True)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=POST_CATEGORY, default="GENERAL")
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)


    @property
    def image_url(self):
        return self.get_image_url
    
    def get_image_url(self):
        if self.image:
            return self.image.url  # Return the uploaded file
        return ""  # Return the default file
    
    def save(self, *args, **kwargs):
        if self.image:
            image_resize(self.image, 640, 426)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

