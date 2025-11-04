from django.db import models

from Neetechs import settings


# Create your models here.
class Experience(models.Model):
    """
    Represents a user's work experience entry.
    Swedish: Experience (Experience).
    """
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Link to the user this work experience belongs to.
    Added_at = models.DateTimeField( # Timestamp when the entry was created. Note: Name is not snake_case.
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at") # Timestamp when the entry was last updated.
    company = models.CharField(max_length=100)    # Name of the company.
    name = models.CharField(max_length=100) # Role or title held at the company.
    plats = models.CharField(max_length=100) # Field 'plats' (Swedish: place/location). Consider renaming to 'location'.
    content = models.TextField() # Detailed description of the work experience.
    started_at = models.CharField(max_length=100,verbose_name="started at") # Start date of the employment. Consider using DateField or a CharField with specific format validation for dates.
    ended_at = models.CharField(max_length=100,verbose_name="ended at") # End date of the employment. Consider using DateField or a CharField with specific format validation for dates.
    objects = models.Manager()  # Default model manager.

    class Meta:
        # TODO: Translate verbose_name and verbose_name_plural to English.
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['name'] # Default ordering for queries.

    def __str__(self):
        return self.name

class Study(models.Model):
    """
    Represents a user's educational background or study entry.
    Swedish: Study (Studies).
    """
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Link to the user this education entry belongs to.
    Added_at = models.DateTimeField( # Timestamp when the entry was created. Note: Name is not snake_case.
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at") # Timestamp when the entry was last updated.
    name = models.CharField(max_length=100) # Name of the educational institution or school.
    degree = models.CharField(max_length=100) # Degree or qualification obtained (e.g., Bachelor's, Master's).
    plats = models.CharField(max_length=100) # Field 'plats' (Swedish: place/location). Consider renaming to 'location' or 'institution_location'.
    objects = models.Manager()  # Default model manager.

    content = models.TextField() # Detailed description of the studies or achievements.
    started_at = models.CharField(max_length=100,verbose_name="started at") # Start date of the studies. Consider using DateField or a CharField with specific format validation for dates.
    ended_at = models.CharField(max_length=100,verbose_name="ended at") # End date of the studies. Consider using DateField or a CharField with specific format validation for dates.

    class Meta:
        # TODO: Translate verbose_name and verbose_name_plural to English.
        verbose_name = "Study"
        verbose_name_plural = "Studys"
        ordering = ['name'] # Default ordering for queries.

    def __str__(self):
        return self.name

class CompetenceCertificate(models.Model):
    """
    Represents a user's skill, competence, or certificate entry.
    Swedish: CompetenceCertificate (Skills/Certificates).
    This model is currently simple. Consider expanding with fields like
    issuing body, date achieved, level, etc. if more detail is needed for skills/certificates.
    """
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Link to the user this skill/certificate belongs to.
    Added_at = models.DateTimeField( # Timestamp when the entry was created. Note: Name is not snake_case.
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at") # Timestamp when the entry was last updated.
    name = models.CharField(max_length=100) # Name of the skill, competence, or certificate.
    objects = models.Manager()  # Default model manager.

    class Meta:
        # TODO: Translate verbose_name and verbose_name_plural to English.
        verbose_name = "Competence eller intyg"
        verbose_name_plural = "Competences och intygs"
        ordering = ['name'] # Default ordering for queries.

    def __str__(self):
        return self.name


class Interest(models.Model):
    """
    Represents a user's interests.
    Swedish: Interest (Interests).
    This model is very simple, primarily storing the name of an interest.
    """
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Link to the user this interest belongs to.
    Added_at = models.DateTimeField( # Timestamp when the entry was created. Note: Name is not snake_case.
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at") # Timestamp when the entry was last updated.
    name = models.CharField(max_length=100) # Name of the interest.
    objects = models.Manager()  # Default model manager.

    class Meta:
        # TODO: Translate verbose_name and verbose_name_plural to English.
        verbose_name = "Interest"
        verbose_name_plural = "Interests"
        ordering = ['name'] # Default ordering for queries.

    def __str__(self):
        return self.name