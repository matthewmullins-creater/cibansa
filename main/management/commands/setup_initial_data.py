from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from main.models import CbCategory, CbTopic, CbTag
from articles.models import CbArticle
from courses.models import CbCourses
from accounts.models import CbUserProfile
import random
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates initial data: 1 superuser with profile, 10 courses, and 10 articles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the superuser (default: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for the superuser (default: admin@example.com)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='adminpass123',
            help='Password for the superuser (default: adminpass123)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        with transaction.atomic():
            # Create superuser if it doesn't exist
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser: {username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Superuser already exists: {username}')
                )

            # Create user profile if it doesn't exist
            profile, profile_created = CbUserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'phone': '1234567890',
                    'dob': date(1990, 1, 1),
                    'country': 'Nigeria',
                    'city': 'Lagos',
                    'gender': 'male',
                    'has_photo': 0,
                    'is_visible': True,
                }
            )

            if profile_created:
                self.stdout.write(
                    self.style.SUCCESS('Successfully created user profile')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('User profile already exists')
                )

            # Create categories if they don't exist
            categories_data = [
                {'name': 'Programming', 'description': 'Learn programming languages and frameworks'},
                {'name': 'Data Science', 'description': 'Data analysis, machine learning, and AI'},
                {'name': 'Web Development', 'description': 'Frontend and backend web development'},
                {'name': 'Mobile Development', 'description': 'iOS and Android app development'},
                {'name': 'DevOps', 'description': 'Infrastructure, deployment, and automation'},
            ]

            categories = []
            for cat_data in categories_data:
                category, created = CbCategory.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={
                        'description': cat_data['description'],
                        'owner': user,
                        'meta_data': {},
                        'is_visible': True,
                    }
                )
                categories.append(category)
                if created:
                    self.stdout.write(f'Created category: {category.name}')

            # Create tags
            tags_data = [
                'Python', 'JavaScript', 'React', 'Django', 'Machine Learning',
                'Data Analysis', 'Web Design', 'Mobile Apps', 'Cloud Computing', 'AI'
            ]

            tags = []
            for tag_name in tags_data:
                tag, created = CbTag.objects.get_or_create(name=tag_name)
                tags.append(tag)
                if created:
                    self.stdout.write(f'Created tag: {tag.name}')

            # Create topics for categories
            topics = []
            for category in categories:
                for i in range(2):  # 2 topics per category
                    topic, created = CbTopic.objects.get_or_create(
                        title=f'{category.name} Topic {i+1}',
                        category=category,
                        defaults={
                            'description': f'Learn about {category.name.lower()} concepts and practices',
                            'owner': user,
                            'meta_data': {},
                            'is_visible': True,
                        }
                    )
                    topics.append(topic)
                    if created:
                        self.stdout.write(f'Created topic: {topic.title}')

            # Create 10 courses
            courses_data = [
                {'title': 'Complete Python Bootcamp', 'category': 'Programming'},
                {'title': 'React.js for Beginners', 'category': 'Web Development'},
                {'title': 'Data Science with Python', 'category': 'Data Science'},
                {'title': 'iOS App Development', 'category': 'Mobile Development'},
                {'title': 'Django Web Framework', 'category': 'Programming'},
                {'title': 'Machine Learning Fundamentals', 'category': 'Data Science'},
                {'title': 'JavaScript ES6+', 'category': 'Web Development'},
                {'title': 'Docker and Kubernetes', 'category': 'DevOps'},
                {'title': 'Android Development with Kotlin', 'category': 'Mobile Development'},
                {'title': 'Advanced Data Analytics', 'category': 'Data Science'},
            ]

            for i, course_data in enumerate(courses_data):
                category = next((cat for cat in categories if cat.name == course_data['category']), categories[0])
                course, created = CbCourses.objects.get_or_create(
                    title=course_data['title'],
                    defaults={
                        'category': category,
                        'content': f'<p>This is a comprehensive course on {course_data["title"]}. '
                                  f'You will learn all the essential concepts and practical skills needed '
                                  f'to excel in this field.</p>',
                        'user': user,
                        'meta_data': {},
                        'is_visible': True,
                    }
                )
                if created:
                    self.stdout.write(f'Created course: {course.title}')

            # Create 10 articles
            articles_data = [
                {'title': '10 Python Tips for Beginners', 'category': 'Programming'},
                {'title': 'Understanding React Hooks', 'category': 'Web Development'},
                {'title': 'Introduction to Machine Learning', 'category': 'Data Science'},
                {'title': 'Mobile App Design Principles', 'category': 'Mobile Development'},
                {'title': 'Django Best Practices', 'category': 'Programming'},
                {'title': 'Data Visualization with Python', 'category': 'Data Science'},
                {'title': 'CSS Grid vs Flexbox', 'category': 'Web Development'},
                {'title': 'CI/CD Pipeline Setup', 'category': 'DevOps'},
                {'title': 'Flutter vs React Native', 'category': 'Mobile Development'},
                {'title': 'Deep Learning Basics', 'category': 'Data Science'},
            ]

            for i, article_data in enumerate(articles_data):
                category = next((cat for cat in categories if cat.name == article_data['category']), categories[0])
                article, created = CbArticle.objects.get_or_create(
                    title=article_data['title'],
                    defaults={
                        'category': category,
                        'content': f'<p>Welcome to this comprehensive article about {article_data["title"]}.</p>'
                                  f'<p>In this article, we will explore the key concepts and provide '
                                  f'practical examples that will help you understand the topic better.</p>'
                                  f'<h2>Introduction</h2>'
                                  f'<p>This topic is essential for anyone looking to advance their skills '
                                  f'in {category.name.lower()}.</p>'
                                  f'<h2>Key Points</h2>'
                                  f'<ul>'
                                  f'<li>Understanding the fundamentals</li>'
                                  f'<li>Practical applications</li>'
                                  f'<li>Best practices and tips</li>'
                                  f'<li>Common pitfalls to avoid</li>'
                                  f'</ul>'
                                  f'<h2>Conclusion</h2>'
                                  f'<p>By following the guidelines in this article, you will be well-equipped '
                                  f'to apply these concepts in your own projects.</p>',
                        'user': user,
                        'meta_data': {},
                        'is_visible': True,
                    }
                )
                if created:
                    self.stdout.write(f'Created article: {article.title}')

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created initial data:\n'
                    f'- 1 superuser: {username}\n'
                    f'- 1 user profile\n'
                    f'- {len(categories)} categories\n'
                    f'- {len(tags)} tags\n'
                    f'- {len(topics)} topics\n'
                    f'- 10 courses\n'
                    f'- 10 articles'
                )
            )
