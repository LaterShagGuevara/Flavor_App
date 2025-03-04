
            # Install Chocolatey if not exists
            if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
                Set-ExecutionPolicy Bypass -Scope Process -Force
                [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
                iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            }

            # Install Node.js
            choco install nodejs-lts -y
            