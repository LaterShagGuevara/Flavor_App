import os
import subprocess
import sys
import json
import shutil
import platform

class FlavorAppFrontendSetup:
    def __init__(self):
        self.project_root = r'c:\Users\sbrea\Desktop\FlavorApp'
        self.frontend_dir = os.path.join(self.project_root, 'frontend')
        self.web_dir = os.path.join(self.frontend_dir, 'web')
        self.mobile_dir = os.path.join(self.frontend_dir, 'mobile')
        self.env_name = 'flavorapp_env'
        self.python_version = '3.12.8'
        self.node_version = '20.x'

    def run_command(self, command, cwd=None, shell=True, capture_output=True):
        """Run a shell command and handle output."""
        try:
            result = subprocess.run(
                command, 
                cwd=cwd, 
                shell=shell, 
                capture_output=capture_output, 
                text=True
            )
            print(f"Command: {command}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return result
        except Exception as e:
            print(f"Error running command: {e}")
            return None

    def install_nodejs(self):
        """Install Node.js and npm"""
        # Download and install Node.js
        if platform.system() == 'Windows':
            import urllib.request
            import zipfile
            import os

            # Node.js download URL for Windows
            node_version = '20.11.1'
            node_url = f'https://nodejs.org/dist/v{node_version}/node-v{node_version}-win-x64.zip'
            node_zip_path = os.path.join(self.project_root, 'node.zip')
            node_extract_path = os.path.join(self.project_root, 'nodejs')

            # Download Node.js
            print("Downloading Node.js...")
            urllib.request.urlretrieve(node_url, node_zip_path)

            # Extract Node.js
            print("Extracting Node.js...")
            with zipfile.ZipFile(node_zip_path, 'r') as zip_ref:
                zip_ref.extractall(node_extract_path)

            # Add Node.js to PATH
            node_bin_path = os.path.join(node_extract_path, f'node-v{node_version}-win-x64')
            os.environ['PATH'] = f"{node_bin_path};{os.environ['PATH']}"

            # Remove downloaded zip
            os.remove(node_zip_path)

            print("Node.js installed successfully!")

    def setup_conda_environment(self):
        """Set up Conda environment with Python 3.12.8"""
        # Check if environment exists
        result = self.run_command(f'conda env list | findstr {self.env_name}')
        if result.returncode != 0:
            # Create new environment
            self.run_command(f'conda create -n {self.env_name} python={self.python_version} -y')
        
        # Activate environment and install dependencies
        self.run_command(f'conda run -n {self.env_name} pip install '
                         'react-scripts react-dom react-router-dom '
                         'axios redux react-redux redux-thunk '
                         'firebase expo')

    def setup_frontend_directories(self):
        """Create frontend directory structure."""
        os.makedirs(self.web_dir, exist_ok=True)
        os.makedirs(self.mobile_dir, exist_ok=True)

    def setup_web_frontend(self):
        """Set up React web frontend with modern UI components"""
        os.chdir(self.web_dir)
        
        # Create React app with TypeScript
        self.run_command('npx create-react-app . --template typescript')
        
        # Install additional dependencies
        dependencies = [
            'axios',
            'react-redux', 
            'redux-thunk',
            'firebase',
            '@mui/material', 
            '@emotion/react', 
            '@emotion/styled',
            'react-router-dom',
            '@types/react-redux'
        ]
        self.run_command(f'npm install {" ".join(dependencies)}')
        
        # Create UI component structure
        os.makedirs(os.path.join(self.web_dir, 'src', 'components'), exist_ok=True)
        os.makedirs(os.path.join(self.web_dir, 'src', 'pages'), exist_ok=True)
        
        # Create placeholder components
        components = [
            'HomePage', 'MealPlanPage', 'RecipePage', 
            'SocialFeedPage', 'LoginPage', 'ProfilePage'
        ]
        for component in components:
            with open(os.path.join(self.web_dir, 'src', 'components', f'{component}.tsx'), 'w') as f:
                f.write(f'''
import React from 'react';
import {{ ThemeProvider, createTheme }} from '@mui/material/styles';

const {component}: React.FC = () => {{
    const darkTheme = createTheme({{
        palette: {{
            mode: 'dark',
        }},
    }});

    return (
        <ThemeProvider theme={{darkTheme}}>
            <div>{component} works!</div>
        </ThemeProvider>
    );
}};

export default {component};
''')

    def setup_mobile_frontend(self):
        """Set up React Native mobile frontend with Expo"""
        os.chdir(self.mobile_dir)
        
        # Create Expo project
        self.run_command('npx create-expo-app .')
        
        # Install additional dependencies
        dependencies = [
            'axios',
            'react-redux', 
            'redux-thunk',
            'firebase',
            '@react-navigation/native',
            '@react-navigation/stack'
        ]
        self.run_command(f'npm install {" ".join(dependencies)}')
        
        # Create mobile component structure
        os.makedirs(os.path.join(self.mobile_dir, 'src', 'components'), exist_ok=True)
        os.makedirs(os.path.join(self.mobile_dir, 'src', 'screens'), exist_ok=True)

    def main(self):
        """Main setup method"""
        print("Starting FlavorApp Frontend Setup...")
        
        # Install Node.js
        self.install_nodejs()
        
        # Ensure Conda environment is set up
        self.setup_conda_environment()
        
        # Create frontend directories
        self.setup_frontend_directories()
        
        # Setup web frontend
        self.setup_web_frontend()
        
        # Setup mobile frontend
        self.setup_mobile_frontend()
        
        print("FlavorApp Frontend Setup Complete!")

if __name__ == '__main__':
    setup = FlavorAppFrontendSetup()
    setup.main()
