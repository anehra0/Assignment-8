"""
Test configuration and fixtures for Flask application tests.
"""
import os
import tempfile
import pytest
import sqlite3
from flask import Flask
import sys

# Add the flask_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from app import app as flask_app
import DAL


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # Override the database path in DAL module
    original_get_db_path = DAL.get_db_path
    DAL.get_db_path = lambda: db_path
    
    # Initialize the database
    DAL.init_db()
    
    yield flask_app
    
    # Cleanup
    DAL.get_db_path = original_get_db_path
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_project():
    """Sample project data for testing."""
    return {
        'title': 'Test Project',
        'description': 'This is a test project description',
        'image': 'test_image.jpg'
    }


@pytest.fixture
def sample_projects():
    """Multiple sample projects for testing."""
    return [
        {
            'title': 'Project 1',
            'description': 'Description for project 1',
            'image': 'image1.jpg'
        },
        {
            'title': 'Project 2',
            'description': 'Description for project 2',
            'image': 'image2.jpg'
        },
        {
            'title': 'Project 3',
            'description': 'Description for project 3',
            'image': ''
        }
    ]


@pytest.fixture
def populated_database(app, sample_projects):
    """Database populated with sample projects."""
    for project in sample_projects:
        DAL.save_project(
            project['title'],
            project['description'],
            project['image']
        )
    return sample_projects
