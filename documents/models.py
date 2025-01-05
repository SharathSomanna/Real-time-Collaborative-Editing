# models.py
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Document(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='documents')
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document for group: {self.group.name}"
