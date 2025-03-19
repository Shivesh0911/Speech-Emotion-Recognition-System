from django.db import models

class EmotionModel(models.Model):
    pkl_file = models.FileField(upload_to='pkl_files/')

    def str(self):
        return self.pkl_file.name