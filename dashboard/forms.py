from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return upload


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProjectForm(forms.Form):
    title = forms.CharField(max_length=200)
    slug = forms.SlugField(max_length=200, help_text="URL-friendly version, e.g. my-cool-project")
    short_summary = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'rows': 2}))
    detailed_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))

    problem_statement = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    solution = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    objectives = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}),
                                  help_text="One objective per line")
    features = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}),
                                help_text="One feature per line")
    workflow = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    challenges = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="One challenge per line, formatted as: Problem :: Solution"
    )
    results = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    future_improvements = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    technologies = forms.CharField(required=False, help_text="Comma-separated, e.g. Python, Django, MongoDB")
    github_url = forms.URLField(required=False)
    live_demo_url = forms.URLField(required=False)
    demo_video_url = forms.URLField(required=False,
                                     help_text="Google Drive link — set sharing to 'Anyone with the link: Viewer'")

    thumbnail = forms.ImageField(required=False, help_text="Card image shown on homepage")
    remove_thumbnail = forms.BooleanField(required=False, help_text="Check to remove the current thumbnail")

    architecture_image = forms.ImageField(required=False, help_text="System architecture diagram")
    remove_architecture_image = forms.BooleanField(required=False, help_text="Check to remove the current architecture image")    
    screenshots = MultipleFileField(
        required=False,
        help_text="Select multiple images (hold Cmd/Ctrl while choosing files). Adding new ones keeps existing screenshots."
    )
    category = forms.CharField(max_length=100, required=False)
    featured = forms.BooleanField(required=False)
    published = forms.BooleanField(required=False, initial=True)
    display_order = forms.IntegerField(required=False, initial=0)



class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=150, help_text="e.g. AI/ML Engineer & Software Developer")
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))
    profile_image = forms.ImageField(required=False)
    remove_profile_image = forms.BooleanField(required=False)
    resume = forms.FileField(required=False, help_text="Upload your resume PDF")
    remove_resume = forms.BooleanField(required=False)
    github_url = forms.URLField(required=False)
    linkedin_url = forms.URLField(required=False)
    email = forms.EmailField(required=False)


class SkillForm(forms.Form):
    name = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100, help_text="e.g. Programming Languages, AI/ML, Cloud")
    proficiency = forms.IntegerField(min_value=0, max_value=100, initial=80,
                                      help_text="0-100")
    display_order = forms.IntegerField(required=False, initial=0)


class ExperienceForm(forms.Form):
    company = forms.CharField(max_length=200)
    role = forms.CharField(max_length=200)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    technologies = forms.CharField(required=False, help_text="Comma-separated")
    start_date = forms.CharField(max_length=50, help_text="e.g. Jan 2024")
    end_date = forms.CharField(max_length=50, help_text="e.g. Present")
    display_order = forms.IntegerField(required=False, initial=0)


class EducationForm(forms.Form):
    degree = forms.CharField(max_length=200)
    institution = forms.CharField(max_length=200)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    start_date = forms.CharField(max_length=50)
    end_date = forms.CharField(max_length=50)
    display_order = forms.IntegerField(required=False, initial=0)