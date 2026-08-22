from django.db import models
from utils.rands import slugify_new
from utils.images import resize_image
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment
from django.urls import reverse
from django.utils.html import strip_tags
from blog.security import sanitize_rich_text

class PostAttachment(AbstractAttachment):
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name        

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


class AuthorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='author_profile',
    )
    avatar = models.ImageField(
        upload_to='authors/%Y/%m/',
        blank=True,
        default='',
    )

    def save(self, *args, **kwargs):
        previous_avatar_name = None

        if self.pk:
            previous_avatar_name = (
                type(self).objects
                .filter(pk=self.pk)
                .values_list('avatar', flat=True)
                .first()
            )

        result = super().save(*args, **kwargs)

        if self.avatar and previous_avatar_name != self.avatar.name:
            resize_image(self.avatar, 300, True, 80)

        return result

    def __str__(self):
        return f'Perfil de {self.user.get_full_name() or self.user.username}'

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 3)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 3)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=50,)
    
    slug = models.SlugField(
        unique=True,
        default="",
        null=False,
        blank=True,
        max_length=255,
    )

    is_published = models.BooleanField(
        default = False,
        help_text='Este campo precisará estar marcado para a pagina ser exibida públicamente'
        )
    
    content = models.TextField()

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        safety_url = reverse('blog:page', args=(self.slug,))
        
        return safety_url

    def save(self, *args, **kwargs):
        self.content = sanitize_rich_text(self.content)

        if not self.slug:
            self.slug = slugify_new(self.title, 3)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    
class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-is_featured', '-pk')

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=50,)
    slug = models.SlugField(
        unique=True,
        default="",
        null=False,
        blank=True,
        max_length=255,
    )

    excerpt = models.CharField(max_length=150)

    is_published = models.BooleanField(
        default = True,
        help_text='Este campo precisará estar marcado para o post ser exibido públicamente'
        )
    is_featured = models.BooleanField(
        default=False,
        help_text='Exibe este post antes dos demais nas listagens.',
    )
    content = models.TextField()

    cover = models.ImageField(upload_to='posts/%Y/%m', blank=True, default='')

    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Deseja exibir imagem de capa no post?'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    # user.post_created_by.all
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True, related_name='post_created_by'
    )

    # user.post_updated_by.all
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True, related_name='post_updated_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        default=None,
    )

    tags = models.ManyToManyField(Tag, blank=True, default='')
    
    
    def __str__(self) -> str:
        return self.title

    @property
    def reading_time(self):
        words_per_minute = 200
        text_content = strip_tags(self.content)
        word_count = len(text_content.split())
        minutes = max(1, round(word_count / words_per_minute))
        return minutes
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        safety_url = reverse('blog:post', args=(self.slug,))
        
        return safety_url


    def save(self, *args, **kwargs):
        self.content = sanitize_rich_text(self.content)

        if not self.slug:
            self.slug = slugify_new(self.title, 3)
        
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name        

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save
    


