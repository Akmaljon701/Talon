from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, related_name='branch_organizations', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Talon(models.Model):
    TALON_NUMBER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('1, 2', '1, 2'),
        ('1, 3', '1, 3'),
        ('2, 3', '2, 3'),
        ('1, 2, 3', '1, 2, 3'),
    ]
    fullname = models.CharField(max_length=255, verbose_name="Ф.И.Ш.")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Филиал')
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Корхона', blank=True, null=True)
    position = models.CharField(max_length=255, verbose_name="Лавозими")
    date_received = models.DateField(verbose_name="Олинган санаси")
    talon_number = models.CharField(max_length=255, choices=TALON_NUMBER_CHOICES, verbose_name="Талон рақами")
    reason_received = models.CharField(max_length=255, verbose_name="Олинган сабаби")
    discipline_order = models.CharField(max_length=255, verbose_name="Интизомий жаза буйруқ рақами")
    discipline_order_date = models.DateField(verbose_name="Интизомий жаза буйруқ санаси")
    discipline_type = models.CharField(max_length=255, verbose_name="Интизомий жаза тури")
    consequence_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Интизомий жаза оқибатида олиб қолинган пул миқдори")
    note = models.TextField(blank=True, null=True, verbose_name="Изоҳ")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fullname
