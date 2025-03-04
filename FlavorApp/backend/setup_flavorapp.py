import os
import sys
import subprocess
import platform

class FlavorAppSetup:
    def __init__(self):
        self.project_root = r'c:\Users\sbrea\Desktop\FlavorApp'
        self.backend_dir = os.path.join(self.project_root, 'backend')
        self.env_name = 'flavorapp_env'
        self.python_version = '3.12.8'
        
    def run_command(self, command, cwd=None, shell=True):
        """Run a shell command and print output."""
        try:
            result = subprocess.run(
                command, 
                cwd=cwd, 
                shell=shell, 
                capture_output=True, 
                text=True
            )
            print(f"Command: {command}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return result
        except Exception as e:
            print(f"Error running command: {e}")
            return None

    def verify_conda(self):
        """Verify Conda is installed and working."""
        conda_check = self.run_command('conda --version')
        if conda_check.returncode != 0:
            print("Conda is not installed. Please install Anaconda or Miniconda.")
            sys.exit(1)
        return True

    def create_conda_environment(self):
        """Create Conda environment with specific Python version."""
        create_env_cmd = f'conda create -n {self.env_name} python={self.python_version} -y'
        self.run_command(create_env_cmd)

    def activate_environment(self):
        """Activate the Conda environment."""
        activate_cmd = f'conda activate {self.env_name}'
        self.run_command(activate_cmd)

    def install_dependencies(self):
        """Install required Python packages."""
        dependencies = [
            'django', 
            'djangorestframework', 
            'firebase-admin', 
            'openai', 
            'python-dotenv', 
            'google-auth-oauthlib', 
            'Pillow', 
            'PyJWT', 
            'requests'
        ]
        
        pip_install_cmd = f'pip install {" ".join(dependencies)}'
        self.run_command(pip_install_cmd)

    def setup_django_project(self):
        """Set up Django project structure."""
        os.makedirs(os.path.join(self.backend_dir, 'flavorapp'), exist_ok=True)
        os.chdir(os.path.join(self.backend_dir, 'flavorapp'))

        # Create Django project
        self.run_command('django-admin startproject backend .')
        
        # Create Django apps
        apps = [
            'authentication', 
            'recipes', 
            'mealplans', 
            'challenges', 
            'notifications'
        ]
        
        for app in apps:
            self.run_command(f'python manage.py startapp {app}')

    def configure_settings(self):
        """Configure Django settings."""
        settings_path = os.path.join(self.backend_dir, 'flavorapp', 'backend', 'settings.py')
        
        with open(settings_path, 'r') as f:
            settings_content = f.read()

        updated_settings = settings_content.replace(
            "INSTALLED_APPS = [",
            "INSTALLED_APPS = [\n    'rest_framework',\n    'rest_framework.authtoken',\n    'authentication',\n    'recipes',\n    'mealplans',\n    'challenges',\n    'notifications',"
        )

        with open(settings_path, 'w') as f:
            f.write(updated_settings)

    def create_env_file(self):
        """Create .env file for sensitive configurations."""
        env_path = os.path.join(self.backend_dir, 'flavorapp', '.env')
        env_config = """
# Django Secret Key
SECRET_KEY=your_very_secret_key_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=path/to/firebase_credentials.json

# Database Configuration
DB_NAME=flavorapp_db
DB_USER=flavorapp_user
DB_PASSWORD=your_secure_password

# JWT Configuration
JWT_SECRET=your_jwt_secret_key
"""
        
        with open(env_path, 'w') as f:
            f.write(env_config)

    def run_migrations(self):
        """Run Django database migrations."""
        migrate_cmd = 'python manage.py makemigrations && python manage.py migrate'
        self.run_command(migrate_cmd)

    def main(self):
        """Main setup method."""
        print("Starting FlavorApp Backend Setup...")
        
        # Verify and set up Conda environment
        self.verify_conda()
        self.create_conda_environment()
        self.activate_environment()
        
        # Install dependencies
        self.install_dependencies()
        
        # Set up Django project
        self.setup_django_project()
        self.configure_settings()
        self.create_env_file()
        self.run_migrations()
        
        print("FlavorApp Backend Setup Completed Successfully!")

if __name__ == '__main__':
    setup = FlavorAppSetup()
    setup.main()
