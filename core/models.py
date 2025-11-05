"""
Models for the Spontime application based on domain schema.
"""
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import CITextField
from django.db import models


class UserManager(BaseUserManager):
    """Manager for User model."""
    
    def create_user(self, email, handle, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not handle:
            raise ValueError('Users must have a handle')
        
        email = self.normalize_email(email)
        user = self.model(email=email, handle=handle, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, handle, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, handle, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model with UUID primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    handle = CITextField(unique=True, max_length=255)
    display_name = models.TextField(null=True, blank=True)
    email = CITextField(unique=True, max_length=255)
    phone = models.TextField(null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    privacy_settings = models.JSONField(default=dict)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Required for Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['handle']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['handle']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.handle or self.email


class Device(models.Model):
    """Device model for push notifications."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    platform = models.CharField(max_length=20)  # ios|android|web|other
    push_token = models.TextField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    trust_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['push_token']),
        ]


class InterestTag(models.Model):
    """Interest tag for user preferences."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    slug = CITextField(unique=True, max_length=255)
    type = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'interest_tags'
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class UserInterestTag(models.Model):
    """Many-to-many through table for User and InterestTag."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(InterestTag, on_delete=models.CASCADE, related_name='user_tags')

    class Meta:
        db_table = 'user_interest_tags'
        unique_together = [['user', 'tag']]


class Place(models.Model):
    """Place model - user-created locations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    location = gis_models.PointField(srid=4326)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_places')
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'places'
        indexes = [
            models.Index(fields=['city', 'country']),
            gis_models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.name


class Partner(models.Model):
    """Partner/business entity."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_partners')
    legal_name = models.TextField()
    contact = models.JSONField(default=dict)  # {email, phone}
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'partners'

    def __str__(self):
        return self.legal_name


class Venue(models.Model):
    """Venue model - partner-owned locations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='venues')
    name = models.TextField()
    location = gis_models.PointField(srid=4326)
    address = models.TextField(null=True, blank=True)
    contact = models.JSONField(default=dict)
    categories = models.JSONField(default=list)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'venues'
        indexes = [
            gis_models.Index(fields=['location']),
            models.Index(fields=['partner']),
        ]

    def __str__(self):
        return self.name


class Cluster(models.Model):
    """Cluster model for grouping entities."""
    SCOPE_CHOICES = [
        ('places', 'Places'),
        ('plans', 'Plans'),
        ('venues', 'Venues'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.TextField()
    centroid = gis_models.PointField(srid=4326)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    plan_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clusters'
        indexes = [
            gis_models.Index(fields=['centroid']),
            models.Index(fields=['scope']),
        ]

    def __str__(self):
        return f"{self.label} ({self.scope})"


class Plan(models.Model):
    """Plan model for events."""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('restricted', 'Restricted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_plans')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name='plans')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name='plans')
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    tags = models.JSONField(default=list)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.IntegerField(default=10)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    is_active = models.BooleanField(default=True)
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True, blank=True, related_name='plans')
    rules = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'plans'
        indexes = [
            models.Index(fields=['host_user']),
            models.Index(fields=['starts_at']),
            models.Index(fields=['visibility']),
            models.Index(fields=['cluster']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(capacity__gte=1), name='capacity_positive')
        ]

    def __str__(self):
        return self.title


class Attendance(models.Model):
    """Attendance tracking for plans."""
    STATUS_CHOICES = [
        ('joined', 'Joined'),
        ('left', 'Left'),
        ('kicked', 'Kicked'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='joined')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'attendances'
        unique_together = [['plan', 'user']]
        indexes = [
            models.Index(fields=['plan']),
            models.Index(fields=['user']),
        ]


class JoinRequest(models.Model):
    """Join requests for restricted plans."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'join_requests'
        unique_together = [['plan', 'user']]
        indexes = [
            models.Index(fields=['plan', 'status']),
        ]


class CheckIn(models.Model):
    """Check-in tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkins')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='checkins')
    geo = gis_models.PointField(srid=4326, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    flags = models.JSONField(default=list)  # anti-abuse flags

    class Meta:
        db_table = 'check_ins'
        indexes = [
            gis_models.Index(fields=['geo']),
            models.Index(fields=['user', 'plan', 'created_at']),
        ]


class Message(models.Model):
    """Messages in plan chats."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        indexes = [
            models.Index(fields=['plan', 'created_at']),
        ]


class Offer(models.Model):
    """Special offers from venues."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='offers')
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    tags = models.JSONField(default=list)
    capacity = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'offers'
        indexes = [
            models.Index(fields=['venue', 'valid_from', 'valid_to']),
        ]


class Boost(models.Model):
    """Boost campaigns for content promotion."""
    TARGET_TYPE_CHOICES = [
        ('plan', 'Plan'),
        ('user', 'User'),
        ('venue', 'Venue'),
        ('message', 'Message'),
        ('offer', 'Offer'),
        ('cluster', 'Cluster'),
        ('report', 'Report'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    target_id = models.UUIDField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'boosts'
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
        ]


class RecoSnapshot(models.Model):
    """Recommendation snapshot."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reco_snapshots')
    generated_at = models.DateTimeField(auto_now_add=True)
    algo_version = models.TextField()
    explanations = models.JSONField(default=list)

    class Meta:
        db_table = 'reco_snapshots'
        indexes = [
            models.Index(fields=['user', 'generated_at']),
        ]


class RecoItem(models.Model):
    """Individual recommendation items."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    snapshot = models.ForeignKey(RecoSnapshot, on_delete=models.CASCADE, related_name='items')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='reco_items')
    score = models.DecimalField(max_digits=6, decimal_places=3)
    distance_m = models.IntegerField()
    shared_tags = models.IntegerField(default=0)

    class Meta:
        db_table = 'reco_items'
        indexes = [
            models.Index(fields=['snapshot']),
            models.Index(fields=['score']),
        ]


class PopularityCounter(models.Model):
    """Popularity tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_type = models.CharField(max_length=50)  # plan|tag|venue
    key_id = models.UUIDField(null=True, blank=True)
    window = models.CharField(max_length=10)  # 1d|7d|30d
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'popularity_counters'
        unique_together = [['key_type', 'key_id', 'window']]


class Report(models.Model):
    """Content reports."""
    TARGET_TYPE_CHOICES = Boost.TARGET_TYPE_CHOICES
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_made')
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    target_id = models.UUIDField()
    reason = models.TextField()
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='open')

    class Meta:
        db_table = 'reports'
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['status']),
        ]


class ModerationAction(models.Model):
    """Moderation actions log."""
    ACTION_CHOICES = [
        ('disable', 'Disable'),
        ('suspend', 'Suspend'),
        ('warn', 'Warn'),
        ('delete_content', 'Delete Content'),
    ]
    TARGET_TYPE_CHOICES = Boost.TARGET_TYPE_CHOICES
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_actions')
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    target_id = models.UUIDField()
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moderation_actions'
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['admin']),
        ]


class BlockList(models.Model):
    """User blocking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blocker_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks_made')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'block_lists'
        unique_together = [['blocker_user', 'blocked_user']]
        indexes = [
            models.Index(fields=['blocker_user']),
        ]


class AuditLog(models.Model):
    """Audit logging."""
    ACTOR_TYPE_CHOICES = [
        ('system', 'System'),
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    TARGET_TYPE_CHOICES = Boost.TARGET_TYPE_CHOICES
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_type = models.CharField(max_length=20, choices=ACTOR_TYPE_CHOICES)
    actor_id = models.UUIDField(null=True, blank=True)
    event = models.TextField()
    entity_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    entity_id = models.UUIDField()
    at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict)

    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['at']),
        ]


class Subscription(models.Model):
    """Subscriptions for users/partners."""
    TIER_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('business', 'Business'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    renewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'subscriptions'
        indexes = [
            models.Index(fields=['user', 'partner']),
        ]


class Invoice(models.Model):
    """Invoices for subscriptions."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('void', 'Void'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    provider_ref = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoices'
        indexes = [
            models.Index(fields=['subscription', 'status']),
        ]

