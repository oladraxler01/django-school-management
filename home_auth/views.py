from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, PasswordResetRequest
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')  # Get role from the form (student, teacher, or admin)
        
        # Create the user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Assign the appropriate role
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()  # Save the user with the assigned role
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('index')  # Redirect to the index or home page
    return render(request, 'authentication/register.html')  # Render signup template


from home_auth.models import CustomUser  # Make sure to import your CustomUser

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print(f"🔐 LOGIN ATTEMPT: Email={email}, Password={password}")
        
        # DEEP DEBUGGING
        try:
            user = CustomUser.objects.get(email=email)  # Using CustomUser instead of User
            print(f"✅ USER FOUND: {user.email}")
            print(f"📋 ROLES - Student:{user.is_student} Teacher:{user.is_teacher} Admin:{user.is_admin}")
            print(f"🔐 STORED PASSWORD HASH: {user.password}")
            print(f"👤 IS ACTIVE: {user.is_active}")
            
            # TEST 1: Manual password check
            password_valid = user.check_password(password)
            print(f"🔑 MANUAL check_password('{password}'): {password_valid}")
            
            # TEST 2: Try different password
            test_result = user.check_password('wrongpassword')
            print(f"🔑 TEST check_password('wrongpassword'): {test_result}")
            
            # TEST 3: Try empty password
            empty_result = user.check_password('')
            print(f"🔑 TEST check_password(''): {empty_result}")
            
            # TEST 4: What authenticate returns
            auth_user = authenticate(request, username=email, password=password)
            print(f"🔑 authenticate() result: {auth_user}")
            
            if password_valid:
                print("🎯 MANUAL AUTHENTICATION SUCCESS - Using manual login")
                login(request, user)
                messages.success(request, 'Login successful!')
                
                if user.is_admin:
                    return redirect('admin_dashboard')
                elif user.is_teacher:
                    return redirect('teacher_dashboard')
                elif user.is_student:
                    return redirect('dashboard')
            else:
                print("❌ MANUAL PASSWORD CHECK FAILED")
                messages.error(request, 'Invalid credentials')
                
        except CustomUser.DoesNotExist:  # Changed to CustomUser
            print("❌ USER NOT FOUND in CustomUser")
            
            # Check if user exists in default User model and migrate them
            try:
                from django.contrib.auth.models import User
                default_user = User.objects.get(email=email)
                print(f"⚠️  User found in default User model, migrating to CustomUser...")
                
                # Create corresponding CustomUser
                custom_user = CustomUser.objects.create_user(
                    email=email,
                    password=password,  # This will set the password properly
                    username=default_user.username,
                    first_name=default_user.first_name,
                    last_name=default_user.last_name,
                    is_teacher=True if hasattr(default_user, 'teacher') else False,
                    is_student=True if hasattr(default_user, 'student') else False,
                    is_active=default_user.is_active
                )
                print(f"✅ Migrated user to CustomUser: {custom_user.email}")
                messages.info(request, 'Account migrated, please try logging in again.')
                
            except User.DoesNotExist:
                print("❌ USER NOT FOUND in any model")
                messages.error(request, 'Invalid credentials')
                
        except Exception as e:
            print(f"💥 UNEXPECTED ERROR: {e}")
            messages.error(request, 'Login error')
    
    return render(request, 'authentication/login.html')


# def forgot_password_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         user = CustomUser.objects.filter(email=email).first()
        
#         if user:
#             token = get_random_string(32)
#             reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
#             reset_request.send_reset_email()
#             messages.success(request, 'Reset link sent to your email.')
#         else:
#             messages.error(request, 'Email not found.')
    
#     return render(request, 'authentication/forgot-password.html')  # Render forgot password template


def forgot_password_test_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            
            # TEMPORARY: DISABLE EMAIL COMPLETELY
            reset_link = f"http://127.0.0.1:8000/reset-password/{token}.html"
            print(f"📧 Password reset link: {reset_link}")
            
            messages.success(request, f'Reset link: {reset_link}')  # Show on page
        else:
            messages.error(request, 'Email not found.')
    
    return render(request, 'authentication/forgot-password.html')


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()
    
    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'authentication/reset_password.html', {'token': token})  # Render reset password template


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')