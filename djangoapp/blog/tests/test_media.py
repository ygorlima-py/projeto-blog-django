from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from blog.models import Post


class MediaUploadTests(TestCase):
    def setUp(self):
        self.media_directory = TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)
        self.addCleanup(self.media_directory.cleanup)

        self.author = User.objects.create_user(
            username='autor-com-foto',
            password='senha-segura',
        )

    def image_upload(self, name, width, height):
        image_bytes = BytesIO()
        Image.new('RGB', (width, height), color='#1d4f4a').save(
            image_bytes,
            format='JPEG',
        )

        return SimpleUploadedFile(
            name,
            image_bytes.getvalue(),
            content_type='image/jpeg',
        )

    def image_size(self, field_file):
        with Image.open(field_file.path) as image:
            return image.size

    def test_post_cover_is_resized_to_a_maximum_width_of_900_pixels(self):
        post = Post.objects.create(
            title='Capa vertical',
            slug='capa-vertical',
            excerpt='Post com foto de capa.',
            content='Conteúdo do post.',
            created_by=self.author,
            cover=self.image_upload('cover.jpg', 1200, 1800),
        )

        self.assertEqual(self.image_size(post.cover), (900, 1350))

    def test_author_avatar_is_resized_and_rendered_on_post_card(self):
        profile = self.author.author_profile
        profile.avatar = self.image_upload('avatar.jpg', 600, 900)
        profile.save()

        post = Post.objects.create(
            title='Post com autor',
            slug='post-com-autor',
            excerpt='Post com avatar do autor.',
            content='Conteúdo do post.',
            created_by=self.author,
        )
        response = self.client.get(reverse('blog:index'))

        self.assertEqual(self.image_size(profile.avatar), (300, 450))
        self.assertContains(response, profile.avatar.url)
        self.assertContains(response, post.title)

    def test_cover_can_be_hidden_from_the_article_body(self):
        post = Post.objects.create(
            title='Capa apenas na listagem',
            slug='capa-apenas-listagem',
            excerpt='Post sem capa no conteúdo.',
            content='Conteúdo do post.',
            created_by=self.author,
            cover=self.image_upload('cover-oculta.jpg', 900, 1200),
            cover_in_post_content=False,
        )

        response = self.client.get(post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f'Capa do artigo {post.title}')
