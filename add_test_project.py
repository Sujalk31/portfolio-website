import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from portfolio.documents import Project, ChallengeSolution

# Delete the old bare-bones test project if it exists
Project.objects(slug="test-project").delete()

Project(
    title="AI Medical Report Summarizer",
    slug="ai-medical-report-summarizer",
    short_summary="AI-powered tool that summarizes medical reports using OCR and LLMs.",
    detailed_description="A full-stack application that extracts text from scanned medical reports and generates concise, accurate summaries for doctors.",
    problem_statement="Doctors spend excessive time reading lengthy medical reports.",
    solution="An automated pipeline that extracts and summarizes key information.",
    objectives=["Reduce doctor reading time", "Improve report accessibility"],
    features=["OCR extraction", "LLM-based summarization", "PDF export"],
    workflow="Upload report -> OCR extraction -> LLM summarization -> Display result",
    challenges=[
        ChallengeSolution(problem="OCR accuracy on scanned documents", solution="Applied OpenCV preprocessing before OCR"),
        ChallengeSolution(problem="Slow LLM response times", solution="Implemented caching and async requests"),
    ],
    results="Reduced average report review time by 40% in testing.",
    future_improvements="Add multi-language support and voice summaries.",
    technologies=["Python", "Django", "OpenCV", "LLM", "MongoDB"],
    github_url="https://github.com/example/repo",
    category="AI/ML",
    featured=True,
    published=True,
    display_order=1
).save()

print("Project created successfully!")