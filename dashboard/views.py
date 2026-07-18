from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from portfolio.documents import Project, Screenshot, ChallengeSolution, Profile, Skill, Experience, Education
from .forms import ProjectForm, ProfileForm, SkillForm, ExperienceForm, EducationForm


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


@login_required(login_url='dashboard_login')
def dashboard_home(request):
    all_projects = Project.objects()
    context = {
        'total_projects': all_projects.count(),
        'published_count': all_projects.filter(published=True).count(),
        'draft_count': all_projects.filter(published=False).count(),
        'featured_count': all_projects.filter(featured=True).count(),
        'projects': all_projects.order_by('display_order'),
    }
    return render(request, 'dashboard/home.html', context)


def _split_lines(text):
    """Turn textarea input (one item per line) into a clean list of strings."""
    if not text:
        return []
    return [line.strip() for line in text.split('\n') if line.strip()]


def _split_commas(text):
    """Turn comma-separated input into a clean list of strings."""
    if not text:
        return []
    return [item.strip() for item in text.split(',') if item.strip()]


def _parse_challenges(text):
    """Turn 'Problem :: Solution' lines into a list of ChallengeSolution objects.
    Skips any line that doesn't contain the :: separator."""
    if not text:
        return []
    result = []
    for line in text.split('\n'):
        line = line.strip()
        if '::' in line:
            problem, solution = line.split('::', 1)
            problem = problem.strip()
            solution = solution.strip()
            if problem and solution:
                result.append(ChallengeSolution(problem=problem, solution=solution))
    return result


def _challenges_to_text(challenges):
    """Turn a list of ChallengeSolution objects back into editable textarea text."""
    if not challenges:
        return ''
    return '\n'.join(f"{c.problem} :: {c.solution}" for c in challenges)

def _save_uploaded_image(image_file, subfolder):
    """Save an uploaded image to media/<subfolder>/ and return its relative path."""
    if not image_file:
        return None
    from django.core.files.storage import default_storage
    path = default_storage.save(f'{subfolder}/{image_file.name}', image_file)
    return path


@login_required(login_url='dashboard_login')
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            if Project.objects(slug=data['slug']).first():
                messages.error(request, f"A project with slug '{data['slug']}' already exists.")
                return render(request, 'dashboard/project_form.html', {'form': form, 'mode': 'Add'})

            thumbnail_path = _save_uploaded_image(data['thumbnail'], 'thumbnails')
            architecture_path = _save_uploaded_image(data['architecture_image'], 'architecture')

            from .forms import ProjectForm as _PF  # no-op, keeps import area unchanged
            screenshot_files = data['screenshots'] or []
            screenshot_docs = []
            for f in screenshot_files:
                path = _save_uploaded_image(f, 'screenshots')
                if path:
                    screenshot_docs.append(Screenshot(image=path, caption=''))
            Project(
                title=data['title'],
                slug=data['slug'],
                short_summary=data['short_summary'],
                detailed_description=data['detailed_description'],
                problem_statement=data['problem_statement'],
                solution=data['solution'],
                objectives=_split_lines(data['objectives']),
                features=_split_lines(data['features']),
                workflow=data['workflow'],
                challenges=_parse_challenges(data['challenges']),
                results=data['results'],
                future_improvements=data['future_improvements'],
                technologies=_split_commas(data['technologies']),
                github_url=data['github_url'] or None,
                live_demo_url=data['live_demo_url'] or None,
                demo_video_url=data['demo_video_url'] or None,
                thumbnail=thumbnail_path,
                architecture_image=architecture_path,
                screenshots=screenshot_docs,
                category=data['category'],
                featured=data['featured'],
                published=data['published'],
                display_order=data['display_order'] or 0,
            ).save()

            messages.success(request, f"Project '{data['title']}' created successfully.")
            return redirect('dashboard_home')
    else:
        form = ProjectForm()

    return render(request, 'dashboard/project_form.html', {'form': form, 'mode': 'Add'})

@login_required(login_url='dashboard_login')
def edit_project(request, slug):
    project = Project.objects(slug=slug).first()
    if project is None:
        messages.error(request, "Project not found.")
        return redirect('dashboard_home')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # If slug changed, make sure the new one isn't already taken by ANOTHER project
            existing = Project.objects(slug=data['slug']).first()
            if existing and existing.id != project.id:
                messages.error(request, f"A project with slug '{data['slug']}' already exists.")
                return render(request, 'dashboard/project_form.html', {'form': form, 'mode': 'Edit', 'project': project})

            project.title = data['title']
            project.slug = data['slug']
            project.short_summary = data['short_summary']
            project.detailed_description = data['detailed_description']
            project.problem_statement = data['problem_statement']
            project.solution = data['solution']
            project.objectives = _split_lines(data['objectives'])
            project.features = _split_lines(data['features'])
            project.workflow = data['workflow']
            project.challenges = _parse_challenges(data['challenges'])
            project.results = data['results']
            project.future_improvements = data['future_improvements']
            project.technologies = _split_commas(data['technologies'])
            project.github_url = data['github_url'] or None
            project.live_demo_url = data['live_demo_url'] or None
            project.demo_video_url = data['demo_video_url'] or None

            # Handle thumbnail: remove takes priority over a fresh upload in the same submit
            if data['remove_thumbnail']:
                project.thumbnail = None
            elif data['thumbnail']:
                project.thumbnail = _save_uploaded_image(data['thumbnail'], 'thumbnails')

            # Handle architecture image the same way
            if data['remove_architecture_image']:
                project.architecture_image = None
            elif data['architecture_image']:
                project.architecture_image = _save_uploaded_image(data['architecture_image'], 'architecture')

            # New screenshots are ADDED to the existing list, not replacing it
            new_screenshot_files = data['screenshots'] or []
            for f in new_screenshot_files:
                path = _save_uploaded_image(f, 'screenshots')
                if path:
                    project.screenshots.append(Screenshot(image=path, caption=''))
            project.category = data['category']
            project.featured = data['featured']
            project.published = data['published']
            project.display_order = data['display_order'] or 0

            import datetime
            project.updated_at = datetime.datetime.utcnow()
            project.save()

            messages.success(request, f"Project '{data['title']}' updated successfully.")
            return redirect('dashboard_home')
    else:
        # Pre-fill the form with the project's current data
        form = ProjectForm(initial={
            'title': project.title,
            'slug': project.slug,
            'short_summary': project.short_summary,
            'detailed_description': project.detailed_description,
            'problem_statement': project.problem_statement,
            'solution': project.solution,
            'objectives': '\n'.join(project.objectives or []),
            'features': '\n'.join(project.features or []),
            'workflow': project.workflow,
            'challenges': _challenges_to_text(project.challenges),
            'results': project.results,
            'future_improvements': project.future_improvements,
            'technologies': ', '.join(project.technologies or []),
            'github_url': project.github_url,
            'live_demo_url': project.live_demo_url,
            'demo_video_url': project.demo_video_url,
            'category': project.category,
            'featured': project.featured,
            'published': project.published,
            'display_order': project.display_order,
        })

    return render(request, 'dashboard/project_form.html', {'form': form, 'mode': 'Edit', 'slug': slug, 'project': project})


@login_required(login_url='dashboard_login')
def delete_project(request, slug):
    project = Project.objects(slug=slug).first()
    if project is None:
        messages.error(request, "Project not found.")
        return redirect('dashboard_home')

    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' deleted.")
        return redirect('dashboard_home')

    return render(request, 'dashboard/confirm_delete.html', {'project': project})


@login_required(login_url='dashboard_login')
def delete_screenshot(request, slug, index):
    project = Project.objects(slug=slug).first()
    if project is None:
        messages.error(request, "Project not found.")
        return redirect('dashboard_home')

    if request.method == 'POST':
        if 0 <= index < len(project.screenshots):
            project.screenshots.pop(index)
            project.save()
            messages.success(request, "Screenshot deleted.")
        else:
            messages.error(request, "Screenshot not found.")

    return redirect('edit_project', slug=slug)


# ---------- PROFILE ----------

@login_required(login_url='dashboard_login')
def edit_profile(request):
    profile = Profile.objects().first()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            if profile is None:
                profile = Profile(name=data['name'], title=data['title'])

            profile.name = data['name']
            profile.title = data['title']
            profile.bio = data['bio']
            profile.github_url = data['github_url'] or None
            profile.linkedin_url = data['linkedin_url'] or None
            profile.email = data['email'] or None

            if data['remove_profile_image']:
                profile.profile_image = None
            elif data['profile_image']:
                profile.profile_image = _save_uploaded_image(data['profile_image'], 'profile')

            if data['remove_resume']:
                profile.resume = None
            elif data['resume']:
                profile.resume = _save_uploaded_image(data['resume'], 'resume')

            profile.save()
            messages.success(request, "Profile updated.")
            return redirect('dashboard_home')
    else:
        initial = {}
        if profile:
            initial = {
                'name': profile.name,
                'title': profile.title,
                'bio': profile.bio,
                'github_url': profile.github_url,
                'linkedin_url': profile.linkedin_url,
                'email': profile.email,
            }
        form = ProfileForm(initial=initial)

    return render(request, 'dashboard/profile_form.html', {'form': form, 'profile': profile})


# ---------- SKILLS ----------

@login_required(login_url='dashboard_login')
def manage_skills(request):
    skills = Skill.objects().order_by('display_order')
    return render(request, 'dashboard/manage_skills.html', {'skills': skills})


@login_required(login_url='dashboard_login')
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Skill(
                name=data['name'],
                category=data['category'],
                proficiency=data['proficiency'],
                display_order=data['display_order'] or 0,
            ).save()
            messages.success(request, "Skill added.")
            return redirect('manage_skills')
    else:
        form = SkillForm()

    return render(request, 'dashboard/simple_form.html', {'form': form, 'title': 'Add Skill', 'back_url': 'manage_skills'})


@login_required(login_url='dashboard_login')
def edit_skill(request, skill_id):
    skill = Skill.objects(id=skill_id).first()
    if skill is None:
        messages.error(request, "Skill not found.")
        return redirect('manage_skills')

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            skill.name = data['name']
            skill.category = data['category']
            skill.proficiency = data['proficiency']
            skill.display_order = data['display_order'] or 0
            skill.save()
            messages.success(request, "Skill updated.")
            return redirect('manage_skills')
    else:
        form = SkillForm(initial={
            'name': skill.name, 'category': skill.category,
            'proficiency': skill.proficiency, 'display_order': skill.display_order,
        })

    return render(request, 'dashboard/simple_form.html', {'form': form, 'title': 'Edit Skill', 'back_url': 'manage_skills'})


@login_required(login_url='dashboard_login')
def delete_skill(request, skill_id):
    skill = Skill.objects(id=skill_id).first()
    if skill and request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted.")
    return redirect('manage_skills')


# ---------- EXPERIENCE ----------

@login_required(login_url='dashboard_login')
def manage_experience(request):
    experience = Experience.objects().order_by('display_order')
    return render(request, 'dashboard/manage_experience.html', {'experience': experience})


@login_required(login_url='dashboard_login')
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Experience(
                company=data['company'],
                role=data['role'],
                description=data['description'],
                technologies=_split_commas(data['technologies']),
                start_date=data['start_date'],
                end_date=data['end_date'],
                display_order=data['display_order'] or 0,
            ).save()
            messages.success(request, "Experience added.")
            return redirect('manage_experience')
    else:
        form = ExperienceForm()

    return render(request, 'dashboard/simple_form.html', {'form': form, 'title': 'Add Experience', 'back_url': 'manage_experience'})


@login_required(login_url='dashboard_login')
def edit_experience(request, exp_id):
    exp = Experience.objects(id=exp_id).first()
    if exp is None:
        messages.error(request, "Experience not found.")
        return redirect('manage_experience')

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            exp.company = data['company']
            exp.role = data['role']
            exp.description = data['description']
            exp.technologies = _split_commas(data['technologies'])
            exp.start_date = data['start_date']
            exp.end_date = data['end_date']
            exp.display_order = data['display_order'] or 0
            exp.save()
            messages.success(request, "Experience updated.")
            return redirect('manage_experience')
    else:
        form = ExperienceForm(initial={
            'company': exp.company, 'role': exp.role, 'description': exp.description,
            'technologies': ', '.join(exp.technologies or []),
            'start_date': exp.start_date, 'end_date': exp.end_date,
            'display_order': exp.display_order,
        })

    return render(request, 'dashboard/simple_form.html', {'form': form, 'title': 'Edit Experience', 'back_url': 'manage_experience'})


@login_required(login_url='dashboard_login')
def delete_experience(request, exp_id):
    exp = Experience.objects(id=exp_id).first()
    if exp and request.method == 'POST':
        exp.delete()
        messages.success(request, "Experience deleted.")
    return redirect('manage_experience')


# ---------- EDUCATION ----------

@login_required(login_url='dashboard_login')
def manage_education(request):
    education = Education.objects().order_by('display_order')
    return render(request, 'dashboard/manage_education.html', {'education': education})


@login_required(login_url='dashboard_login')
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Education(
                degree=data['degree'],
                institution=data['institution'],
                description=data['description'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                display_order=data['display_order'] or 0,
            ).save()
            messages.success(request, "Education added.")
            return redirect('manage_education')
    else:
        form = EducationForm()

    return render(request, 'dashboard/simple_form.html', {'form': form, 'title': 'Add Education', 'back_url': 'manage_education'})


@login_required(login_url='dashboard_login')
def edit_education(request, edu_id):
    edu = Education.objects(id=edu_id).first()
    if edu is None:
        messages.error(request, "Education not found.")
        return redirect('manage_education')

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            edu.degree = data['degree']
            edu.institution = data['institution']
            edu.description = data['description']
            edu.start_date = data['start_date']
            edu.end_date = data['end_date']
            edu.display_order = data['display_order'] or 0
            edu.save()
            messages.success(request, "Education updated.")
            return redirect('manage_education')
    else:
        form = EducationForm(initial={
            'degree': edu.degree, 'institution': edu.institution, 'description': edu.description,
            'start_date': edu.start_date, 'end_date': edu.end_date, 'display_order': edu.display_order,
        })

    return render(request, 'dashboard/simple_form.html', {'form': form, 'title': 'Edit Education', 'back_url': 'manage_education'})


@login_required(login_url='dashboard_login')
def delete_education(request, edu_id):
    edu = Education.objects(id=edu_id).first()
    if edu and request.method == 'POST':
        edu.delete()
        messages.success(request, "Education deleted.")
    return redirect('manage_education')