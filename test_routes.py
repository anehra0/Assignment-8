"""
Tests for Flask application routes and HTTP endpoints.
"""
import pytest
from flask import url_for


def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Ankush Nehra' in response.data


def test_index_route_alternative(client):
    """Test the alternative index route."""
    response = client.get('/index')
    assert response.status_code == 200
    assert b'Ankush Nehra' in response.data


def test_about_route(client):
    """Test the about route."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data


def test_contact_route(client):
    """Test the contact route."""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact' in response.data


def test_resume_route(client):
    """Test the resume route."""
    response = client.get('/resume')
    assert response.status_code == 200
    assert b'Resume' in response.data


def test_thankyou_route(client):
    """Test the thankyou route."""
    response = client.get('/thankyou')
    assert response.status_code == 200
    assert b'Thank' in response.data


def test_projects_route_get(client):
    """Test the projects route GET request."""
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'Projects' in response.data
    assert b'Add New Project' in response.data


def test_projects_add_route_get(client):
    """Test the add project route GET request."""
    response = client.get('/projects/add')
    assert response.status_code == 200
    assert b'Add a New Project' in response.data
    assert b'form' in response.data


def test_projects_add_route_post_valid(client, sample_project):
    """Test the add project route POST request with valid data."""
    response = client.post('/projects/add', data=sample_project)
    assert response.status_code == 302  # Redirect after successful submission
    assert response.location.endswith('/projects')


def test_projects_add_route_post_invalid(client):
    """Test the add project route POST request with invalid data."""
    invalid_data = {
        'title': '',  # Empty title should fail validation
        'description': 'Some description',
        'image': 'test.jpg'
    }
    response = client.post('/projects/add', data=invalid_data)
    assert response.status_code == 200  # Should re-render form with error
    assert b'Title is required' in response.data


def test_projects_add_route_post_whitespace_title(client):
    """Test the add project route POST request with whitespace-only title."""
    invalid_data = {
        'title': '   ',  # Whitespace-only title should fail validation
        'description': 'Some description',
        'image': 'test.jpg'
    }
    response = client.post('/projects/add', data=invalid_data)
    assert response.status_code == 200  # Should re-render form with error
    assert b'Title is required' in response.data


def test_projects_add_route_post_missing_fields(client):
    """Test the add project route POST request with missing fields."""
    partial_data = {
        'title': 'Test Project'
        # Missing description and image fields
    }
    response = client.post('/projects/add', data=partial_data)
    assert response.status_code == 302  # Should still succeed as description and image are optional


def test_projects_route_with_projects(client, populated_database):
    """Test the projects route when projects exist in database."""
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'Project 1' in response.data
    assert b'Project 2' in response.data
    assert b'Project 3' in response.data


def test_projects_route_empty_database(client):
    """Test the projects route when no projects exist."""
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'No projects found' in response.data


def test_static_files(client):
    """Test that static files are accessible."""
    response = client.get('/static/styles.css')
    assert response.status_code == 200


def test_nonexistent_route(client):
    """Test accessing a non-existent route."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_projects_add_form_fields(client):
    """Test that the add project form contains all required fields."""
    response = client.get('/projects/add')
    assert response.status_code == 200
    assert b'name="title"' in response.data
    assert b'name="description"' in response.data
    assert b'name="image"' in response.data
    assert b'required' in response.data  # Title field should be required


def test_projects_table_structure(client, populated_database):
    """Test that the projects table has correct structure."""
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'<table' in response.data
    assert b'<th>Image</th>' in response.data
    assert b'<th>Title</th>' in response.data
    assert b'<th>Description</th>' in response.data


def test_navigation_links(client):
    """Test that navigation links are present on pages."""
    response = client.get('/')
    assert b'href="/index"' in response.data
    assert b'href="/about"' in response.data
    assert b'href="/resume"' in response.data
    assert b'href="/projects"' in response.data
    assert b'href="/contact"' in response.data

