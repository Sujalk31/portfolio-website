from django.shortcuts import render, get_object_or_404
from .documents import Project, Profile, Skill, Experience, Education

def home(request):
    projects = Project.objects(published=True).order_by('display_order')
    profile = Profile.objects().first()
    skills = Skill.objects().order_by('display_order')
    experience = Experience.objects().order_by('display_order')
    education = Education.objects().order_by('display_order')

    # Group skills by category so the template can show "Programming Languages", "AI/ML", etc. as headers
    skills_by_category = {}
    for skill in skills:
        category = skill.category or 'Other'
        skills_by_category.setdefault(category, []).append(skill)

    context = {
        'projects': projects,
        'profile': profile,
        'skills_by_category': skills_by_category,
        'experience': experience,
        'education': education,
    }
    return render(request, 'portfolio/home.html', context)


def project_detail(request, slug):
    project = Project.objects(slug=slug, published=True).first()
    if project is None:
        from django.http import Http404
        raise Http404("Project not found")
    context = {
        'project': project
    }
    return render(request, 'portfolio/project_detail.html', context)