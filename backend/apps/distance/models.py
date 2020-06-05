from django.db import models


class Distance(models.Model):
    start = models.TextField()
    end = models.TextField()
    kilometers = models.DecimalField(decimal_places=2, max_digits=7)
    miles = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return 'Start: {}; End: {}'.format(self.start[:30].strip(), self.end[:30].strip())
