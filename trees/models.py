# apps/trees/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

User = get_user_model()

class Tree(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_trees")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class TreeShare(models.Model):
    ROLE_CHOICES = (("owner","owner"),("editor","editor"),("viewer","viewer"))
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name="shares")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tree_shares")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Member(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name="members")
    given_name = models.CharField(max_length=120)
    family_name = models.CharField(max_length=120, blank=True)
    middle_names = models.CharField(max_length=120, blank=True)
    suffix = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    birthplace = models.CharField(max_length=200, blank=True)
    deathplace = models.CharField(max_length=200, blank=True)
    photo_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    location_text = models.CharField(max_length=200, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)
    is_living = models.BooleanField(default=True)
    privacy_level = models.CharField(max_length=10, default="private")  # private/shared/public

    class Meta:
        indexes = [GinIndex(fields=["custom_fields"])]

class Relationship(models.Model):
    TYPE_CHOICES = (
        ("parent","parent"), ("child","child"),
        ("spouse","spouse"), ("ex_spouse","ex_spouse"),
        ("partner","partner"), ("sibling","sibling"),
        ("guardian","guardian"), ("adoptive_parent","adoptive_parent"),
    )
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name="relationships")
    from_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="rels_from")
    to_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="rels_to")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    certainty = models.FloatField(default=1.0)

class Media(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name="media")
    member = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL, related_name="media")
    url = models.URLField()
    caption = models.CharField(max_length=200, blank=True)
    taken_at = models.DateField(null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
