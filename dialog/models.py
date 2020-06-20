from django.db import models
import uuid
# Create your models here.


class Page(models.Model):
    __PAGE_TYPES = (
        ('help','Strona pomocy'),
        ('subpage','Podstrona'),
        ('info','Strona informacyjna'),
    )
    title = models.CharField(max_length=64)
    slug = models.SlugField()
    text = models.TextField(verbose_name="Wypowiedź")
    type = models.CharField(max_length=16,choices=__PAGE_TYPES)
    def __str__(self): return self.title

class Statement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(verbose_name="Wypowiedź")
    entry = models.BooleanField(verbose_name="Czy może zaczynać dialog",default=False)
    anwsers = models.ManyToManyField(to="Anwser",verbose_name="Możliwe odpowiedzi")

    def add_option(self,label,target,accepted=True):
        option = Anwser()
        option.text = label
        option.goto = target
        option.accepted = accepted
        option.save()
        self.anwsers.add(option)
        self.save()
        return option

    def possible_anwser(self):
        return self.anwsers.filter(accepted=True)

    def __str__(self):
        if len(self.text) < 50:
            return "{}[{}]".format(self.text,len(self.anwsers.all()))
        alt = ""
        for word in self.text.split():
            alt += word + ' '
            if len(alt) > 50:
                break
        return "{}[{}]".format(alt[:-1]+'...',len(self.anwsers.all()))

class Anwser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(verbose_name="Odpowiedź")
    goto = models.ForeignKey("Statement",verbose_name="Przejdź do", on_delete=models.PROTECT)
    accepted = models.BooleanField(verbose_name="Zatwierdzona",default=True)

    def __str__(self):
        if len(self.text) < 50:
            return "{}".format(self.text)
        alt = ""
        for word in self.text.split():
            alt += word + ' '
            if len(alt) > 50:
                break
        return alt[:-1]+'...'
