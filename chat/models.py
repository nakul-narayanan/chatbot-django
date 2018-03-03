from django.db import models

class UserTracking(models.Model):
    FAT = "ft"
    STUPID = "sd"
    DUMB = "db"

    BUTTON_CHOICES = (
        (FAT , "FAT" ),
	    (STUPID , "STUPID"),
        (DUMB ,"DUMB"),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    button_type = models.CharField(max_length=2, choices=BUTTON_CHOICES,default=FAT)
    count = models.PositiveIntegerField(null=False, blank=False, default=0)
    
   
    class Meta:
        verbose_name = 'UserTracking'
        verbose_name_plural = 'UserTrackings'

    def __str__(self):
        return self.user.get_full_name() if self.user.get_full_name() else str(self.user.id)
