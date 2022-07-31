from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext as _

from apps.account.employe_type import Employetype
from utils.base_model import BaseModel


class UserManager(BaseUserManager):
    def employes(self):
        return self.filter(type_user=Users.EMPLOYE)

    def clients(self):
        return self.filter(type_user=Users.CLIENT)

    def create_user(self, username, password, email=None, phone=None, is_admin=False, is_staff=False, is_active=False):
        if not username:
            raise ValueError(_("username is required"))
        if not password:
            raise ValueError(_("password is required"))
        if not phone or not email:
            raise ValueError(_("please use phone number or email"))

        user_object = self.model(
            username=username
        )
        user_object.set_password(password)
        user_object.staff = is_staff
        user_object.admin = is_admin
        user_object.active = is_active
        user_object.email = email
        user_object.phone = phone
        user_object.save(using=self._db)
        return user_object

    def create_staffuser(self, username, password, phone=None, email=None):
        return self.create_user(username=username, password=password, is_staff=True, phone=phone, email=email)

    def create_superuser(self, username, password, phone=None, email=None):
        return self.create_user(username=username, password=password, is_staff=True, is_admin=True, phone=phone, email=email, is_active=True)

    def get_by_natural_key(self, username):
        return self.get(username=username)


# user model


class Users(AbstractBaseUser):
    CLIENT = "Cl"
    EMPLOYE = "Ep"
    BOTH = "Bh"
    TYPE_USER = [
        (CLIENT, "Client"),
        (EMPLOYE, "Employe"),
        (BOTH, "Both"),
    ]
    email = models.EmailField(max_length=254, unique=True, null=True)
    phone = models.CharField(max_length=254, unique=True, null=True)
    username = models.CharField(
        max_length=254, unique=True)
    password = models.CharField(max_length=200)
    active = models.BooleanField(default=False)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)
    type_user = models.CharField(max_length=10, choices=TYPE_USER)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", 'phone']

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label):
        return True

    def natural_key(self) -> CharField:
        return self.username

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Company(BaseModel):
    """
        company model
    """
    nom = models.CharField(max_length=45)
    code = models.CharField(max_length=45)
    slogan = models.TextField(null=True, blank=True)
    mail = models.EmailField(max_length=250)
    responsable = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.pk}"

    def get_slogan(self):
        """return le slogan de la comapagnie"""
        return _(self.slogan)

    def get_responsable(self):
        """return le responsable..."""
        return self.responsable

    def get_code(self):
        """return le code """
        return self.code

    def get_mail(self):
        """return le email"""
        return self.mail


class PersonneGenderBase(models.Model):
    WOMAN = "F"
    MAN = "H"
    INDERTEMINAT = "I"
    _GENDERS = [
        (WOMAN, _("Woman")),
        (MAN, _("Man")),
        (INDERTEMINAT, _("Indeterminate")),
    ]
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        choices=_GENDERS,
        default=INDERTEMINAT
    )

    class Meta:
        abstract = True


class PersonalMixin(BaseModel):
    firstname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    birthDay = models.DateField()

    class Meta:
        abstract = True
        ordering = ['firstname']

    def fullname(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"

    def __str__(self):
        """ """
        return self.firstname


class Employe(Employetype, PersonalMixin):
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, related_name="employe")
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    type_employe = models.CharField(
        max_length=5, choices=Employetype.EMPLOYE_TYPE)


class Client(PersonalMixin):
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, related_name="client")
