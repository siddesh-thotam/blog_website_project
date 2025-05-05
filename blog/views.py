from django.shortcuts import render, redirect , get_object_or_404
from blog.models import Post , Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def landing_page(request):
    return render(request, 'blog/landing.html')


def home(request):
    # Get category from URL parameters
    category = request.GET.get('category')
    
    # Filter posts if category is specified
    if category:
        posts = Post.objects.filter(tags__icontains=category).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    context = {
        'posts': posts,
        'current_category': category,
        'total_posts': posts.count()
    }
    return render(request, 'blog/dashboard.html', context)

@login_required
def form(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        tags = request.POST.getlist("tags")
        image = request.FILES.get("image")

        if not title or not description:
            messages.error(request, "Title and description are required.")
            return render(request, "blog/form.html")

        try:
            # Create post with the logged-in user as author
            post = Post.objects.create(
                author=request.user,  # Use the logged-in user
                title=title,
                description=description,
                tags=", ".join(tags) if tags else "",
                image=image
            )
            messages.success(request, "Post created successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error creating post: {str(e)}")
            return render(request, "blog/form.html")

    return render(request, "blog/form.html")

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "blog/login.html")

        try:
            # Check if user exists first
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                messages.error(request, "Username does not exist.")
                return render(request, "blog/login.html")

            # Try to authenticate
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid password.")
                return render(request, "blog/login.html")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, "blog/login.html")

    return render(request, "blog/login.html")

def logout_page(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validate input fields
        if not username or not password or not confirm_password:
            messages.error(request, "All Fields are required to be Filled.")
            return render(request, "blog/register.html")
        
        if confirm_password != password:
            messages.error(request, "The Confirm Password Does not Match.")
            return render(request, "blog/register.html")
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "The Username Already Exists.")
            return render(request, "blog/register.html")

        try:
            # Create and save the user, and set password properly
            user = User.objects.create_user(
                username=username,
            )
            user.set_password(password)  # This properly hashes the password
            user.save()
            
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, "Account Created Successfully!")
            return redirect('home')  # Redirect to home instead of login
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, "blog/register.html")

    return render(request, "blog/register.html")

@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        
        if profile_pic:
            # Get or create profile for the user
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.profile_pic = profile_pic
            profile.save()
            
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'Please select an image to upload')
        
        return redirect('home')
    return redirect('home')


@login_required
def my_posts(request):
    # Get posts for the current user
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': user_posts})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        tags = request.POST.getlist("tags")
        image = request.FILES.get("image")
        
        if not title or not description:
            messages.error(request, "Title and description are required.")
            return render(request, "blog/edit_post.html", {'post': post})
            
        post.title = title
        post.description = description
        post.tags = ", ".join(tags) if tags else ""
        if image:
            post.image = image
        post.save()
        
        messages.success(request, "Post updated successfully!")
        return redirect('my_posts')
        
    return render(request, "blog/edit_post.html", {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('my_posts')
        
    return render(request, "blog/delete_post.html", {'post': post})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
        'tags': [tag.strip() for tag in post.tags.split(',')] if post.tags else []
    }
    return render(request, 'blog/post_detail.html', context)



