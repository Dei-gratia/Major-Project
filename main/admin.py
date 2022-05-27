from django.contrib import admin
from .models import Home, HomeImage, About, Phone, Email, Social, Contact, \
    AboutImage, Address, SchoolLevel, Subject, Specialisation, Program

# Register your models here.


# ======HOME======
class HomeImageInline(admin.StackedInline):
    model = HomeImage
    extra = 1


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    inlines = [
        HomeImageInline,
    ]


# ======ABOUT======
class EmailInline(admin.StackedInline):
    model = Email
    extra = 1


class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1


class SocialInline(admin.StackedInline):
    model = Social
    extra = 0


class AboutImageInline(admin.StackedInline):
    model = AboutImage
    extra = 1


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [
        EmailInline,
        PhoneInline,
        AddressInline,
        SocialInline,
        AboutImageInline,
    ]


# ======CONTACT======
admin.site.register(Contact)


# ======SCHOOLLEVEL======
@admin.register(SchoolLevel)
class SchoolLevelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


# ======SPECIALISATION======
@admin.register(Specialisation)
class SpecialisationAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


# ======PROGRAM======
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


# ======SUBJECT======
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
