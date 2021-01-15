from django.db import models


# Book genre (Science Fiction, French Poetry etc.)
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Book author (Lev Tolstoy, Philip Dik etc.)
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    info = models.TextField(max_length=2000)

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


# Book ("Nose", "Harry Potter and Prisoner of Django" etc.)
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    description = models.TextField(max_length=2000)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

