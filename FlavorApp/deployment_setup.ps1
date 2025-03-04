# FlavorApp Deployment Setup Script
# Automates authentication and configuration for web and mobile deployments

# Ensure execution policy allows running scripts
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Function to check and install Node.js and npm
function Install-NodeJS {
    # Check if Node.js is installed
    $nodePath = Get-Command node -ErrorAction SilentlyContinue
    if (-not $nodePath) {
        Write-Host "Node.js not found. Installing..."
        
        # Download Node.js installer
        $nodeVersion = "20.11.1"
        $nodeUrl = "https://nodejs.org/dist/v$nodeVersion/node-v$nodeVersion-x64.msi"
        $nodeInstallerPath = "$env:TEMP\node-installer.msi"
        
        # Download Node.js MSI
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstallerPath
        
        # Install Node.js silently
        Start-Process msiexec.exe -ArgumentList "/i $nodeInstallerPath /qn" -Wait
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "Node.js installed successfully!"
    }
    else {
        Write-Host "Node.js is already installed."
    }
}

# Function to authenticate Vercel
function Set-VercelAuthentication {
    Write-Host "Authenticating with Vercel..."
    
    # Install Vercel CLI globally
    npm install -g vercel
    
    # Prompt for Vercel login
    vercel login
}

# Function to authenticate Netlify
function Set-NetlifyAuthentication {
    Write-Host "Authenticating with Netlify..."
    
    # Install Netlify CLI globally
    npm install -g netlify-cli
    
    # Prompt for Netlify login
    netlify login
}

# Function to authenticate Expo
function Set-ExpoAuthentication {
    Write-Host "Authenticating with Expo..."
    
    # Install Expo CLI and EAS CLI globally
    npm install -g expo-cli eas-cli
    
    # Prompt for Expo login
    expo login
    
    # Set up EAS build
    eas build:configure
}

# Function to configure web project
function Set-WebProjectConfiguration {
    param (
        [string]$ProjectPath = "C:\Users\sbrea\Desktop\FlavorApp\frontend\web"
    )
    
    Write-Host "Configuring web project..."
    
    # Change to project directory
    Push-Location $ProjectPath
    
    # Initialize npm project if not exists
    if (-not (Test-Path "package.json")) {
        npm init -y
    }
    
    # Install React dependencies
    npm install react react-dom react-scripts
    
    # Add build script to package.json
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    $packageJson.scripts.build = "react-scripts build"
    $packageJson | ConvertTo-Json | Set-Content "package.json"
    
    # Create Vercel configuration
    $vercelConfig = @{
        version = 2
        name = "flavorapp-web"
        builds = @(
            @{
                src = "build/**"
                use = "@vercel/static"
            }
        )
        routes = @(
            @{
                src = "/(.*)"
                dest = "build/$1"
            }
        )
    }
    $vercelConfig | ConvertTo-Json | Set-Content "vercel.json"
    
    # Create Netlify configuration
    $netlifyConfig = @"
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"@
    $netlifyConfig | Set-Content "netlify.toml"
    
    # Link Netlify site
    netlify link
    
    Pop-Location
}

# Function to configure mobile project
function Set-MobileProjectConfiguration {
    param (
        [string]$ProjectPath = "C:\Users\sbrea\Desktop\FlavorApp\frontend\mobile"
    )
    
    Write-Host "Configuring mobile project..."
    
    # Change to project directory
    Push-Location $ProjectPath
    
    # Initialize npm project if not exists
    if (-not (Test-Path "package.json")) {
        npm init -y
    }
    
    # Install Expo dependencies
    npm install expo react-native
    
    # Create Expo configuration
    $expoConfig = @{
        expo = @{
            name = "FlavorApp"
            slug = "flavorapp"
            version = "1.0.0"
            orientation = "portrait"
            icon = "./assets/icon.png"
            splash = @{
                image = "./assets/splash.png"
                resizeMode = "contain"
                backgroundColor = "#ffffff"
            }
            updates = @{
                fallbackToCacheTimeout = 0
            }
            assetBundlePatterns = @(
                "**/*"
            )
            ios = @{
                supportsTablet = $true
                bundleIdentifier = "com.flavorapp.mobile"
            }
            android = @{
                adaptiveIcon = @{
                    foregroundImage = "./assets/adaptive-icon.png"
                    backgroundColor = "#FFFFFF"
                }
                package = "com.flavorapp.mobile"
            }
        }
    }
    $expoConfig | ConvertTo-Json -Depth 10 | Set-Content "app.json"
    
    # Create EAS configuration
    $easConfig = @{
        build = @{
            production = @{
                android = @{
                    gradleCommand = ":app:bundleRelease"
                    withoutCredentials = $true
                }
                ios = @{
                    buildType = "release"
                    withoutCredentials = $true
                }
            }
        }
    }
    $easConfig | ConvertTo-Json -Depth 10 | Set-Content "eas.json"
    
    Pop-Location
}

# Main deployment setup workflow
function Start-DeploymentSetup {
    # Install Node.js
    Install-NodeJS
    
    # Authenticate deployment services
    Set-VercelAuthentication
    Set-NetlifyAuthentication
    Set-ExpoAuthentication
    
    # Configure projects
    Set-WebProjectConfiguration
    Set-MobileProjectConfiguration
    
    Write-Host "Deployment setup completed successfully!"
}

# Run the deployment setup
Start-DeploymentSetup
