import os
import sys
import subprocess
import json
import platform
import shutil

class FlavorAppDeployment:
    def __init__(self):
        self.project_root = r'c:\Users\sbrea\Desktop\FlavorApp'
        self.backend_dir = os.path.join(self.project_root, 'backend')
        self.frontend_dir = os.path.join(self.project_root, 'frontend')
        self.web_dir = os.path.join(self.frontend_dir, 'web')
        self.mobile_dir = os.path.join(self.frontend_dir, 'mobile')
        self.deployment_dir = os.path.join(self.project_root, 'deployment')
        self.env_name = 'flavorapp_env'

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

    def setup_deployment_environment(self):
        """Prepare deployment environment and tools"""
        # Ensure Node.js and npm are installed
        self.ensure_nodejs_npm()
        
        # Install deployment tools
        deployment_tools = [
            'vercel',
            'netlify-cli',
            'expo-cli',
            '@expo/ngrok'
        ]
        
        # Install globally using npm
        self.run_command(f'npm install -g {" ".join(deployment_tools)}')

    def ensure_nodejs_npm(self):
        """Ensure Node.js and npm are properly installed"""
        # Check if Node.js is installed
        node_check = self.run_command('node --version', capture_output=True)
        npm_check = self.run_command('npm --version', capture_output=True)
        
        # If Node.js or npm are not found, install them
        if node_check.returncode != 0 or npm_check.returncode != 0:
            print("Node.js or npm not found. Installing...")
            
            # Download and install Node.js
            node_version = '20.11.1'
            node_url = f'https://nodejs.org/dist/v{node_version}/node-v{node_version}-win-x64.zip'
            node_zip_path = os.path.join(self.project_root, 'node.zip')
            node_extract_path = os.path.join(self.project_root, 'nodejs')

            # Download Node.js
            import urllib.request
            import zipfile
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

            # Verify installation
            node_version_check = self.run_command('node --version')
            npm_version_check = self.run_command('npm --version')
            
            if node_version_check.returncode != 0 or npm_version_check.returncode != 0:
                raise RuntimeError("Failed to install Node.js and npm")

    def prepare_web_deployment(self):
        """Prepare web app for deployment"""
        os.chdir(self.web_dir)
        
        # Create package.json if not exists
        if not os.path.exists('package.json'):
            package_json = {
                "name": "flavorapp-web",
                "version": "1.0.0",
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                },
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "react-scripts": "^5.0.1"
                }
            }
            with open('package.json', 'w') as f:
                json.dump(package_json, f, indent=2)
        
        # Install dependencies
        self.run_command('npm install')
        
        # Build React app
        self.run_command('npm run build')
        
        # Create Vercel configuration
        vercel_config = {
            "version": 2,
            "name": "flavorapp-web",
            "builds": [
                {"src": "build/**", "use": "@vercel/static"}
            ],
            "routes": [
                {"src": "/(.*)", "dest": "build/$1"}
            ]
        }
        
        with open('vercel.json', 'w') as f:
            json.dump(vercel_config, f, indent=2)
        
        # Create Netlify configuration
        netlify_config = '''
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
'''
        
        with open('netlify.toml', 'w') as f:
            f.write(netlify_config)

    def deploy_web_app(self):
        """Deploy web app to Vercel and Netlify"""
        os.chdir(self.web_dir)
        
        # Deploy to Vercel
        vercel_deploy = self.run_command('vercel --prod --yes')
        
        # Deploy to Netlify
        netlify_deploy = self.run_command('netlify deploy --prod')
        
        return vercel_deploy, netlify_deploy

    def prepare_mobile_deployment(self):
        """Prepare mobile app for deployment"""
        os.chdir(self.mobile_dir)
        
        # Install Expo locally
        self.run_command('npm install expo-cli --save-dev')
        
        # Create package.json if not exists
        if not os.path.exists('package.json'):
            package_json = {
                "name": "flavorapp-mobile",
                "version": "1.0.0",
                "scripts": {
                    "start": "expo start",
                    "android": "expo start --android",
                    "ios": "expo start --ios",
                    "web": "expo start --web"
                },
                "dependencies": {
                    "expo": "^49.0.0",
                    "react": "^18.2.0",
                    "react-native": "^0.72.0"
                }
            }
            with open('package.json', 'w') as f:
                json.dump(package_json, f, indent=2)
        
        # Install dependencies
        self.run_command('npm install')
        
        # Configure Expo build
        expo_config = {
            "expo": {
                "name": "FlavorApp",
                "slug": "flavorapp",
                "version": "1.0.0",
                "orientation": "portrait",
                "icon": "./assets/icon.png",
                "splash": {
                    "image": "./assets/splash.png",
                    "resizeMode": "contain",
                    "backgroundColor": "#ffffff"
                },
                "updates": {
                    "fallbackToCacheTimeout": 0
                },
                "assetBundlePatterns": [
                    "**/*"
                ],
                "ios": {
                    "supportsTablet": True,
                    "bundleIdentifier": "com.flavorapp.mobile"
                },
                "android": {
                    "adaptiveIcon": {
                        "foregroundImage": "./assets/adaptive-icon.png",
                        "backgroundColor": "#FFFFFF"
                    },
                    "package": "com.flavorapp.mobile"
                }
            }
        }
        
        with open('app.json', 'w') as f:
            json.dump(expo_config, f, indent=2)

    def build_mobile_app(self):
        """Build mobile app for Android and iOS using Expo EAS"""
        os.chdir(self.mobile_dir)
        
        # Install EAS CLI
        self.run_command('npm install -g eas-cli')
        
        # Create EAS configuration
        eas_config = {
            "build": {
                "production": {
                    "android": {
                        "gradleCommand": ":app:bundleRelease",
                        "withoutCredentials": True
                    },
                    "ios": {
                        "buildType": "release",
                        "withoutCredentials": True
                    }
                }
            }
        }
        
        with open('eas.json', 'w') as f:
            json.dump(eas_config, f, indent=2)
        
        # Build Android APK
        android_build = self.run_command('eas build -p android --non-interactive')
        
        # Build iOS IPA for TestFlight
        ios_build = self.run_command('eas build -p ios --non-interactive')
        
        return android_build, ios_build

    def optimize_performance(self):
        """Implement performance optimizations"""
        # Web Performance Optimization
        web_optimization_config = {
            "performance": {
                "hints": {
                    "maxAssetSize": 250000,  # 250 KB
                    "maxEntrypointSize": 250000  # 250 KB
                },
                "optimization": {
                    "splitChunks": {
                        "chunks": "all",
                        "minSize": 20000,
                        "maxSize": 250000
                    }
                }
            }
        }
        
        # Write web performance config
        with open(os.path.join(self.web_dir, 'webpack.config.js'), 'w') as f:
            f.write(f'module.exports = {json.dumps(web_optimization_config, indent=2)}')
        
        # Mobile Performance Optimization
        mobile_optimization_config = {
            "expo": {
                "performance": {
                    "lazyLoading": True,
                    "codeCache": True
                }
            }
        }
        
        # Update mobile app.json with performance settings
        with open(os.path.join(self.mobile_dir, 'app.json'), 'r+') as f:
            config = json.load(f)
            config.update(mobile_optimization_config)
            f.seek(0)
            json.dump(config, f, indent=2)

    def main(self):
        """Execute full deployment process"""
        print("Starting FlavorApp Deployment...")
        
        # Setup deployment environment
        self.setup_deployment_environment()
        
        # Prepare web app
        self.prepare_web_deployment()
        
        # Deploy web app
        web_deployment = self.deploy_web_app()
        
        # Prepare mobile app
        self.prepare_mobile_deployment()
        
        # Build mobile app
        mobile_builds = self.build_mobile_app()
        
        # Optimize performance
        self.optimize_performance()
        
        print("FlavorApp Deployment Complete!")
        
        return {
            'web_deployment': web_deployment,
            'mobile_builds': mobile_builds
        }

if __name__ == '__main__':
    deployment = FlavorAppDeployment()
    deployment.main()
