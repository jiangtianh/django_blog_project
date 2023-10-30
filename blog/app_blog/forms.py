from django import forms 
from .models import Post, Category, Comment

# category_choices = [(x.name, x.name) for x in list(Category.objects.all())] # used for the choices drop down for category
# use x.name here because the Category model has a name field

class PostForm(forms.ModelForm):

    snippet = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter snippet'}), 
        required=False, 
        initial='Click on the title to read more...')
    class Meta:
        model = Post 
        fields = ['title', 'title_tag', 'category', 'body', 'snippet', 'header_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title tag'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post body'}),
            'header_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['title', 'title_tag', 'category', 'body', 'snippet']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title tag'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post body'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter snippet'}),
        }



class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }
   


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment'}),
        }