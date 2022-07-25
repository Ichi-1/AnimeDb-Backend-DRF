from unicodedata import category
from django.test import TestCase
from django.contrib.auth.models import User
from apps.blog.models import Post, Category

class TestCreatePost(TestCase):
    
    @classmethod
    def set_up_test_data(cls):
        test_category = Category.objects.create(name='django')
        testuser1 = User.objects.creat_user(
            username='test_user1',
            password='0123456789'
        )
        test_post = Post.objects.create(
            category_id=1,
            title='Post Title',
            annotation='Lomer Ipsum',
            content='####',
            slug='post-title',
            author_id=1,
            status='published',

        )
    
    def test_blog_content(self):
        post = Post.custom_objects.get(id=1)
        cat = Category.objects.get(id=1)

        author = f'{post.author}'
        annotation = f'{post.annotation}'
        title = f'{post.title}'
        content = f'{post.content}'
        status = f'{post.status}'

        self.assertEqual(author, 'test_user1')
        self.assertEqual(title, 'Post Title')
        self.assertEqual(annotation, 'Lomer Ipsum')
        self.assertEqual(content, '###')
        self.assertEqual(status, 'published')
        self.assertEqual(str(post), 'Post Title')
        self.assertEqual(str(cat), 'django')