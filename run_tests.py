#!/usr/bin/env python
"""
Test runner script for the Creative Backend project.

This script provides various options for running tests:
- Run all tests
- Run specific test categories
- Run tests with coverage
- Run tests for specific models or endpoints
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests(test_labels=None, verbosity=1, interactive=True, failfast=False, keepdb=False):
    """Run tests with specified parameters"""
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=interactive,
        failfast=failfast,
        keepdb=keepdb
    )
    
    if test_labels is None:
        test_labels = ['core.tests']
    
    failures = test_runner.run_tests(test_labels)
    
    if failures:
        sys.exit(1)

def main():
    """Main function with command line options"""
    
    print("=== Creative Backend Test Runner ===\n")
    
    # Test categories
    test_categories = {
        '1': ('All Tests', ['core.tests']),
        '2': ('Model Tests Only', ['core.tests.ModelTests']),
        '3': ('API Endpoint Tests Only', [
            'core.tests.BlogPostAPITests',
            'core.tests.PortfolioItemAPITests', 
            'core.tests.ServiceAPITests',
            'core.tests.TeamMemberAPITests',
            'core.tests.TestimonialAPITests',
            'core.tests.ContactInquiryAPITests'
        ]),
        '4': ('Translation Tests Only', ['core.tests.TranslationTests']),
        '5': ('Blog Post Tests', ['core.tests.BlogPostAPITests']),
        '6': ('Portfolio Tests', ['core.tests.PortfolioItemAPITests']),
        '7': ('Service Tests', ['core.tests.ServiceAPITests']),
        '8': ('Team Member Tests', ['core.tests.TeamMemberAPITests']),
        '9': ('Testimonial Tests', ['core.tests.TestimonialAPITests']),
        '10': ('Contact Inquiry Tests', ['core.tests.ContactInquiryAPITests']),
    }
    
    print("Available test categories:")
    for key, (name, _) in test_categories.items():
        print(f"{key}. {name}")
    
    print("\nOptions:")
    print("v: Verbose output")
    print("f: Fail fast (stop on first failure)")
    print("k: Keep test database")
    print("c: Run with coverage report")
    print("\nExamples:")
    print("1v - Run all tests with verbose output")
    print("3fk - Run API tests with fail fast and keep database")
    print("4c - Run translation tests with coverage")
    
    choice = input("\nEnter your choice (or 'q' to quit): ").strip().lower()
    
    if choice == 'q':
        print("Goodbye!")
        return
    
    # Parse options
    verbosity = 2 if 'v' in choice else 1
    failfast = 'f' in choice
    keepdb = 'k' in choice
    coverage = 'c' in choice
    
    # Extract test category number
    test_num = ''.join(filter(str.isdigit, choice))
    
    if test_num not in test_categories:
        print("Invalid choice!")
        return
    
    test_name, test_labels = test_categories[test_num]
    
    print(f"\n=== Running {test_name} ===")
    print(f"Verbosity: {verbosity}")
    print(f"Fail Fast: {failfast}")
    print(f"Keep DB: {keepdb}")
    print(f"Coverage: {coverage}")
    print()
    
    if coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
            
            run_tests(
                test_labels=test_labels,
                verbosity=verbosity,
                failfast=failfast,
                keepdb=keepdb
            )
            
            cov.stop()
            cov.save()
            
            print("\n=== Coverage Report ===")
            cov.report()
            cov.html_report(directory='htmlcov')
            print("\nHTML coverage report generated in 'htmlcov' directory")
            
        except ImportError:
            print("Coverage package not installed. Install with: pip install coverage")
            print("Running tests without coverage...")
            run_tests(
                test_labels=test_labels,
                verbosity=verbosity,
                failfast=failfast,
                keepdb=keepdb
            )
    else:
        run_tests(
            test_labels=test_labels,
            verbosity=verbosity,
            failfast=failfast,
            keepdb=keepdb
        )

if __name__ == '__main__':
    main()
