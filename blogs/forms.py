from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class Meta:
    model = Post
    fields = ['title', 'content', 'featured_image']


class PostForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[],
        required=True,
        help_text="Select a category for your post"
    )
    new_category = forms.CharField(
        max_length=50,
        required=False,
        help_text="Want to create a new category? Type it here"
    )
    tags = forms.CharField(
        required=False,
        help_text="Add tags separated by commas (e.g. python, django, web)"
    )
    featured_image = forms.ImageField(
        required=False,
        help_text="Add a cover image for your post (optional)",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = list(Category.objects.all())
        category_choices = [(str(category.id), category.name) for category in categories]
        category_choices.append(('other', '+ Add New Category'))
        self.fields['category'].choices = category_choices
        # If no categories, default to 'other' and show new category input
        if not categories:
            self.initial['category'] = 'other'
        # If editing, prepopulate tags as comma-separated
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def clean(self):
        cleaned_data = super().clean()
        category_choice = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        if category_choice == 'other':
            if not new_category:
                raise forms.ValidationError("Please enter a new category name when selecting 'Other'")
        elif category_choice:
            try:
                category = Category.objects.get(id=int(category_choice))
                cleaned_data['category_instance'] = category
            except (Category.DoesNotExist, ValueError):
                raise forms.ValidationError("Invalid category selected")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('category') == 'other':
            category, created = Category.objects.get_or_create(
                name=self.cleaned_data.get('new_category')
            )
        else:
            category = self.cleaned_data.get('category_instance')
        instance.category = category
        if commit:
            instance.save()
        # Do NOT handle tags here; let the view handle it after instance is saved and has an ID
        return instance

    class Meta:
        model = Post
        fields = ['title', 'content']  # Remove category from here since we handle it specially

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
