#!/usr/bin/env python
"""
Framework Verification Script
验证框架是否正确安装和配置
"""
import sys
import os
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_python_version():
    """Check Python version"""
    print("\n✓ Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")
        return False
    return True


def check_dependencies():
    """Check if dependencies are installed"""
    print("\n✓ Checking dependencies...")
    
    required = {
        'pytest': 'pytest',
        'playwright': 'playwright',
        'pytest_bdd': 'pytest-bdd',
        'pydantic': 'pydantic',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_project_structure():
    """Check if project structure is correct"""
    print("\n✓ Checking project structure...")
    
    required_dirs = [
        'core',
        'pages',
        'features',
        'step_defs',
        'utils',
        'tests',
    ]
    
    required_files = [
        'config.py',
        'conftest.py',
        'pytest.ini',
        'requirements.txt',
        'run_tests.py',
    ]
    
    all_good = True
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ (missing)")
            all_good = False
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (missing)")
            all_good = False
    
    return all_good


def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    print("\n✓ Checking Playwright browsers...")
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Try to launch chromium
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("  ✓ Chromium browser installed")
                return True
            except Exception as e:
                print(f"  ✗ Chromium browser not installed")
                print(f"    Run: python -m playwright install chromium")
                return False
    except ImportError:
        print("  ✗ Playwright not installed")
        return False


def verify_fsm():
    """Verify FSM implementation"""
    print("\n✓ Verifying FSM implementation...")
    try:
        from douyu_test_framework.core.fsm import FSM, PageState
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            fsm = FSM(page, PageState.INITIAL)
            fsm.transition("navigate_home")
            
            assert fsm.current_state == PageState.HOME
            assert len(fsm.history) == 2
            
            browser.close()
        
        print("  ✓ FSM working correctly")
        return True
    except Exception as e:
        print(f"  ✗ FSM test failed: {e}")
        return False


def verify_page_objects():
    """Verify page objects can be imported"""
    print("\n✓ Verifying page objects...")
    try:
        from douyu_test_framework.pages.home_page import HomePage
        from douyu_test_framework.pages.category_page import CategoryPage
        from douyu_test_framework.pages.live_room_page import LiveRoomPage
        from douyu_test_framework.pages.search_results_page import SearchResultsPage
        
        print("  ✓ HomePage")
        print("  ✓ CategoryPage")
        print("  ✓ LiveRoomPage")
        print("  ✓ SearchResultsPage")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def main():
    """Main verification function"""
    os.chdir(Path(__file__).parent)
    
    print_header("Douyu Test Framework - Verification")
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies()[0],
        'Project Structure': check_project_structure(),
        'Playwright Browsers': check_playwright_browsers(),
        'FSM Implementation': verify_fsm(),
        'Page Objects': verify_page_objects(),
    }
    
    # Summary
    print_header("Verification Summary")
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! Framework is ready to use.")
        print("\nQuick start:")
        print("  python run_tests.py")
        print("  or")
        print("  pytest -v --headed")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        print("  python -m playwright install chromium")
        return 1


if __name__ == "__main__":
    sys.exit(main())
