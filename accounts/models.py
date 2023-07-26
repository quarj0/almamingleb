from django.db import models
from django.contrib.auth.models import User

university_choices = (
    ("ucc", "University of Cape Coast"),
    ("ug", "University of Ghana"),
    ("knust", "Kwame Nkrumah University of Science and Technology"),
    ("uew", "University of Education, Winneba"),
    ("umat", "University of Mines and Technology"),
    ("uds", "University of Development Studies"),
    ("upsa", "University of Professional Studies, Accra"),
    ("uenr", "University of Energy and Natural Resources"),
    ("uhas", "University of Health and Allied Sciences"),
    ("gimpa", "Ghana Institute of Management and Public Administration"),
    ("atu", "Accra Technical University"),
    ("ashesi", "Ashesi University"),
    ("central", "Central University"),
    ("kstu", "Kumasi Technical University"),
)

basic_information_choices = {
    "Program": (
        ("bsc-cs", "BSc. Computer Science"),
        ("bsc-it", "BSc. Information Technology"),
        ("bsc-ict", "BSc. Information and Communication Technology"),
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
    "Level": (
        ("100", "100"),
        ("200", "200"),
        ("300", "300"),
        ("400", "400"),
    ),
    "Living": (
        ("hostel-friends", "Hostel with friends"),
        ("hall-friends", "Hall with friends"),
        ("hostel-alone", "Hostel alone"),
        ("hall-alone", "Hall alone"),
    ),
    "Height": (
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
}


gender_choices = [
        ("M", "Male"),
        ("F", "Female"),
    ]

def user_profile_picture_path(self, filename):
    return f"profile_picture/{self.username}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    username = models.CharField(max_length=100, unique=True)
    
    email = models.EmailField(max_length=100, unique=True)
    
    password = models.CharField(max_length=100, default="")
    
    university = models.CharField(max_length=255, choices=university_choices)
    
    gender = models.CharField(max_length=1, choices=gender_choices, null=True)
    
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)
    
    
    basic_information = models.JSONField(
        max_length=100, choices=basic_information_choices.items(), blank=True, null=True
    )
    
    passions = models.TextField(blank=True, null=True)
    
    about_section = models.TextField(blank=True, null=True)
    
    gallery = models.ImageField(upload_to="gallery/", blank=True, null=True, width_field='30', height_field='24')

    def __str__(self):
        return self.username
    fernet_key = models.CharField(max_length=44, blank=True, null=True)


class EmailVerification(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    otp = models.IntegerField()


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="viewed_profiles",
    )
    viewed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="viewed_by"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.viewer.username} viewed {self.viewed_user.username}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    favorite_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorited_by"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favorited {self.favorite_user.username}"


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
