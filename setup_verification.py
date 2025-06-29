#!/usr/bin/env python3
"""
Setup Verification Script
Verifies that all components of the Enhanced PPC Client Tools are properly installed and configured
"""

import os
import sys
import subprocess
import importlib

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def check_node_version():
    """Check Node.js installation"""
    print("\n🟢 Checking Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - Available")
            return True
        else:
            print("❌ Node.js not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Node.js not found - Required for website verification")
        return False

def check_required_files():
    """Check that all required script files exist"""
    print("\n📄 Checking required files...")
    
    required_files = [
        'setup_client.sh',
        'claude_research_setup.py',
        'prompt_generator.py',
        'research_orchestrator.py',
        'main_research_workflow.py',
        'verify_tracking.js',
        'competitor_research.py',
        'requirements.txt',
        'config.yaml',
        'GUIDE.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def check_python_dependencies():
    """Check required Python packages"""
    print("\n📦 Checking Python dependencies...")
    
    required_packages = {
        'requests': '2.25.1',
        'beautifulsoup4': '4.9.3', 
        'lxml': '4.6.3',
        'click': '8.0.0',
        'jinja2': '3.0.0',
        'rich': '13.0.0',
        'yaml': '6.0.0'  # pyyaml imports as yaml
    }
    
    missing_packages = []
    for package, min_version in required_packages.items():
        try:
            if package == 'yaml':
                # pyyaml imports as yaml
                imported_package = importlib.import_module('yaml')
            else:
                imported_package = importlib.import_module(package)
            
            # Try to get version
            if hasattr(imported_package, '__version__'):
                version = imported_package.__version__
                print(f"✅ {package} {version}")
            else:
                print(f"✅ {package} (version unknown)")
                
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_file_permissions():
    """Check that script files have proper execute permissions"""
    print("\n🔐 Checking file permissions...")
    
    executable_files = [
        'setup_client.sh',
        'claude_research_setup.py',
        'research_orchestrator.py', 
        'main_research_workflow.py',
        'competitor_research.py'
    ]
    
    permission_issues = []
    for file in executable_files:
        if os.path.exists(file):
            if os.access(file, os.X_OK):
                print(f"✅ {file} - Executable")
            else:
                print(f"⚠️  {file} - Not executable (will fix)")
                permission_issues.append(file)
        else:
            print(f"❌ {file} - File missing")
    
    return len(permission_issues) == 0, permission_issues

def fix_permissions(files):
    """Fix file permissions"""
    print("\n🔧 Fixing file permissions...")
    for file in files:
        try:
            os.chmod(file, 0o755)
            print(f"✅ Fixed permissions for {file}")
        except Exception as e:
            print(f"❌ Failed to fix {file}: {str(e)}")

def check_directory_structure():
    """Check that templates and config directories exist"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        'templates'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ directory exists")
        else:
            print(f"⚠️  {directory}/ directory missing (will create)")
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created {directory}/ directory")

def install_missing_packages(packages):
    """Install missing Python packages"""
    print(f"\n📦 Installing missing packages...")
    
    try:
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {str(e)}")
        return False

def run_verification():
    """Run complete verification process"""
    print("🚀 Enhanced PPC Client Tools - Setup Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check Python version
    if not check_python_version():
        all_checks_passed = False
    
    # Check Node.js
    node_available = check_node_version()
    if not node_available:
        print("⚠️  Node.js missing - website verification will not work")
    
    # Check required files
    files_ok, missing_files = check_required_files()
    if not files_ok:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        all_checks_passed = False
    
    # Check Python dependencies
    deps_ok, missing_packages = check_python_dependencies()
    if not deps_ok:
        print(f"\n📦 Missing packages detected. Installing...")
        if install_missing_packages(missing_packages):
            print("✅ All packages installed successfully")
        else:
            print("❌ Package installation failed")
            all_checks_passed = False
    
    # Check file permissions
    perms_ok, permission_issues = check_file_permissions()
    if not perms_ok:
        fix_permissions(permission_issues)
    
    # Check directory structure
    check_directory_structure()
    
    # Final summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("🎉 Setup verification completed successfully!")
        print("\n✅ All components are properly configured")
        print("\n🚀 You can now run:")
        print("   python3 main_research_workflow.py \"Client Name\"")
        print("   or")
        print("   ./setup_client.sh \"Client Name\"")
        print("   python3 claude_research_setup.py \"Client Name\"")
    else:
        print("⚠️  Setup verification completed with issues")
        print("\n📋 Manual steps required:")
        if not files_ok:
            print(f"   - Ensure all required files are present")
        if not deps_ok:
            print(f"   - Install missing Python packages: pip3 install {' '.join(missing_packages)}")
        if not node_available:
            print(f"   - Install Node.js for website verification")
    
    print(f"\n📖 See GUIDE.md for detailed usage instructions")
    return all_checks_passed

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)