import mongoengine as me
import datetime


class ChallengeSolution(me.EmbeddedDocument):
    """A single challenge paired with how it was solved.
    Embedded means this data lives INSIDE the Project document,
    not in its own separate collection."""
    problem = me.StringField(required=True)
    solution = me.StringField(required=True)


class Screenshot(me.EmbeddedDocument):
    """A single screenshot image with an optional caption."""
    image = me.StringField(required=True)
    caption = me.StringField(blank=True)


class Project(me.Document):
    # Basic info
    title = me.StringField(required=True, max_length=200)
    slug = me.StringField(required=True, unique=True, max_length=200)
    short_summary = me.StringField(required=True, max_length=300)
    detailed_description = me.StringField()

    # Story fields
    problem_statement = me.StringField()
    solution = me.StringField()
    objectives = me.ListField(me.StringField())
    features = me.ListField(me.StringField())
    workflow = me.StringField()
    challenges = me.EmbeddedDocumentListField(ChallengeSolution)
    results = me.StringField()
    future_improvements = me.StringField()

    # Tech + links
    technologies = me.ListField(me.StringField(max_length=50))
    github_url = me.URLField(blank=True)
    live_demo_url = me.URLField(blank=True)
    demo_video_url = me.URLField(blank=True)

    # Media (local file paths for now — Phase 5 covers uploads properly)
    # Media (local file paths)
    thumbnail = me.StringField(blank=True)
    architecture_image = me.StringField(blank=True)
    screenshots = me.EmbeddedDocumentListField(Screenshot)

    # Organization
    category = me.StringField(max_length=100)
    featured = me.BooleanField(default=False)
    published = me.BooleanField(default=True)
    display_order = me.IntField(default=0)

    # Timestamps
    created_at = me.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'projects',
        'ordering': ['display_order']
    }

    def __str__(self):
        return self.title


class Profile(me.Document):
    name = me.StringField(required=True, max_length=100)
    title = me.StringField(required=True, max_length=150)
    bio = me.StringField()
    profile_image = me.StringField(blank=True)
    resume = me.StringField(blank=True)
    github_url = me.URLField(blank=True)
    linkedin_url = me.URLField(blank=True)
    email = me.EmailField(blank=True)

    meta = {'collection': 'profile'}

    def __str__(self):
        return self.name


class Skill(me.Document):
    name = me.StringField(required=True, max_length=100)
    category = me.StringField(max_length=100)
    proficiency = me.IntField(default=80, min_value=0, max_value=100)
    display_order = me.IntField(default=0)

    meta = {
        'collection': 'skills',
        'ordering': ['display_order']
    }

    def __str__(self):
        return self.name


class Experience(me.Document):
    company = me.StringField(required=True, max_length=200)
    role = me.StringField(required=True, max_length=200)
    description = me.StringField()
    technologies = me.ListField(me.StringField(max_length=50))
    start_date = me.StringField(max_length=50, help_text="e.g. Jan 2024")
    end_date = me.StringField(max_length=50, help_text="e.g. Present")
    display_order = me.IntField(default=0)

    meta = {
        'collection': 'experience',
        'ordering': ['display_order']
    }

    def __str__(self):
        return f"{self.role} at {self.company}"


class Education(me.Document):
    degree = me.StringField(required=True, max_length=200)
    institution = me.StringField(required=True, max_length=200)
    description = me.StringField()
    start_date = me.StringField(max_length=50)
    end_date = me.StringField(max_length=50)
    display_order = me.IntField(default=0)

    meta = {
        'collection': 'education',
        'ordering': ['display_order']
    }

    def __str__(self):
        return self.degree