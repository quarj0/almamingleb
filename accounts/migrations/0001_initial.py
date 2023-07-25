# Generated by Django 4.2.2 on 2023-06-25 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "university_name",
                    models.CharField(
                        choices=[
                            ("ucc", "University of Cape Coast"),
                            ("ug", "University of Ghana"),
                            (
                                "knust",
                                "Kwame Nkrumah University of Science and Technology",
                            ),
                            ("uew", "University of Education, Winneba"),
                            ("umat", "University of Mines and Technology"),
                            ("uds", "University of Development Studies"),
                            ("upsa", "University of Professional Studies, Accra"),
                            ("uenr", "University of Energy and Natural Resources"),
                            ("uhas", "University of Health and Allied Sciences"),
                            (
                                "gimpa",
                                "Ghana Institute of Management and Public Administration",
                            ),
                            ("atu", "Accra Technical University"),
                            ("ashesi", "Ashesi University"),
                            ("central", "Central University"),
                            ("kstu", "Kumasi Technical University"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("profile_picture", models.ImageField(upload_to="profile_pics/")),
                ("age", models.IntegerField(blank=True, null=True)),
                (
                    "university_name",
                    models.CharField(
                        choices=[
                            ("ucc", "University of Cape Coast"),
                            ("ug", "University of Ghana"),
                            (
                                "knust",
                                "Kwame Nkrumah University of Science and Technology",
                            ),
                            ("uew", "University of Education, Winneba"),
                            ("umat", "University of Mines and Technology"),
                            ("uds", "University of Development Studies"),
                            ("upsa", "University of Professional Studies, Accra"),
                            ("uenr", "University of Energy and Natural Resources"),
                            ("uhas", "University of Health and Allied Sciences"),
                            (
                                "gimpa",
                                "Ghana Institute of Management and Public Administration",
                            ),
                            ("atu", "Accra Technical University"),
                            ("ashesi", "Ashesi University"),
                            ("central", "Central University"),
                            ("kstu", "Kumasi Technical University"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "basic_information",
                    models.JSONField(
                        blank=True,
                        choices=[
                            (
                                "Program",
                                (
                                    ("bsc-cs", "BSc. Computer Science"),
                                    ("bsc-it", "BSc. Information Technology"),
                                    (
                                        "bsc-ict",
                                        "BSc. Information and Communication Technology",
                                    ),
                                    ("bsc-nursing", "BSc. Nursing"),
                                    ("bsc-midwifery", "BSc. Midwifery"),
                                    ("bsc-pa", "BSc. Physician Assistantship"),
                                    ("bsc-mlt", "BSc. Medical Laboratory Technology"),
                                    ("bsc-mit", "BSc. Medical Imaging Technology"),
                                    ("bsc-dietetics", "BSc. Dietetics"),
                                    ("bsc-physiotherapy", "BSc. Physiotherapy"),
                                    ("bsc-math", "BSc. Mathematics"),
                                    ("bsc-lt", "BSc. Laboratory Technology"),
                                    ("bsc-chem", "BSc. Chemistry"),
                                    ("bsc-physics", "BSc. Physics"),
                                    ("bsc-actsci", "BSc. Actuarial Science"),
                                    ("bsc-stats", "BSc. Statistics"),
                                    ("bsc-law", "BSc. Law"),
                                    ("ba-comms", "BA. Communication Studies"),
                                    ("bed-basic", "BEd. Basic Education"),
                                    ("bed-early", "BEd. Early Childhood Education"),
                                    ("ba-english", "BA. English"),
                                    ("ba-french", "BA. French"),
                                    ("ba-econ", "BA. Economics"),
                                    ("bed-social", "BEd. Social Studies"),
                                    ("bed-polsci", "BEd. Political Science"),
                                    ("ba-polsci", "BA. Political Science"),
                                    ("ba-sociology", "BA. Sociology"),
                                    ("bed-mgt", "BEd. Management"),
                                    ("bed-acc", "BEd. Accounting"),
                                    ("bed-math", "BEd. Mathematics"),
                                    ("bed-science", "BEd. Science"),
                                ),
                            ),
                            (
                                "Level",
                                (
                                    ("100", "100"),
                                    ("200", "200"),
                                    ("300", "300"),
                                    ("400", "400"),
                                ),
                            ),
                            (
                                "Living",
                                (
                                    ("hostel-friends", "Hostel with friends"),
                                    ("hall-friends", "Hall with friends"),
                                    ("hostel-alone", "Hostel alone"),
                                    ("hall-alone", "Hall alone"),
                                ),
                            ),
                            (
                                "Height",
                                (
                                    ("4'0''", "4' 0''"),
                                    ("4'1''", "4' 1''"),
                                    ("4'2''", "4' 2''"),
                                    ("4'3''", "4' 3''"),
                                    ("4'4''", "4' 4''"),
                                    ("4'5''", "4' 5''"),
                                    ("4'6''", "4' 6''"),
                                    ("4'7''", "4' 7''"),
                                    ("4'8''", "4' 8''"),
                                    ("4'9''", "4' 9''"),
                                    ("4'10''", "4' 10''"),
                                    ("4'11''", "4' 11''"),
                                    ("5'0''", "5' 0''"),
                                    ("5'1''", "5' 1''"),
                                    ("5'2''", "5' 2''"),
                                    ("5'3''", "5' 3''"),
                                    ("5'4''", "5' 4''"),
                                    ("5'5''", "5' 5''"),
                                    ("5'6''", "5' 6''"),
                                    ("5'7''", "5' 7''"),
                                    ("5'8''", "5' 8''"),
                                    ("5'9''", "5'9''"),
                                    ("5'10''", "5'10''"),
                                    ("5'11''", "5'11''"),
                                    ("6'0''", "6'0''"),
                                ),
                            ),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("passions", models.TextField(blank=True, null=True)),
                ("about_section", models.TextField(blank=True, null=True)),
                (
                    "gallery",
                    models.ImageField(blank=True, null=True, upload_to="gallery/"),
                ),
                ("program", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailVerification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("otp", models.IntegerField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
                    ),
                ),
            ],
        ),
    ]
