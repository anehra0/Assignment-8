"""
Integration tests for the complete Flask application workflow.
"""
import pytest
import DAL


def test_complete_project_workflow(client, app):
    """Test the complete workflow: view projects -> add project -> view updated projects."""
    # Step 1: View empty projects page
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'No projects found' in response.data
    
    # Step 2: Navigate to add project page
    response = client.get('/projects/add')
    assert response.status_code == 200
    assert b'Add a New Project' in response.data
    
    # Step 3: Add a new project
    project_data = {
        'title': 'Integration Test Project',
        'description': 'This project tests the complete workflow',
        'image': 'integration_test.jpg'
    }
    response = client.post('/projects/add', data=project_data)
    assert response.status_code == 302  # Redirect after successful submission
    
    # Step 4: Verify project appears on projects page
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'Integration Test Project' in response.data
    assert b'This project tests the complete workflow' in response.data


def test_project_form_validation_workflow(client, app):
    """Test the workflow with form validation errors."""
    # Step 1: Try to submit form with empty title
    invalid_data = {
        'title': '',  # Empty title should fail
        'description': 'Some description',
        'image': 'test.jpg'
    }
    response = client.post('/projects/add', data=invalid_data)
    assert response.status_code == 200  # Should re-render form
    assert b'Title is required' in response.data
    
    # Step 2: Fix the title and submit again
    valid_data = {
        'title': 'Fixed Title',
        'description': 'Some description',
        'image': 'test.jpg'
    }
    response = client.post('/projects/add', data=valid_data)
    assert response.status_code == 302  # Should redirect on success
    
    # Step 3: Verify project was created
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'Fixed Title' in response.data


def test_multiple_projects_display(client, app, sample_projects):
    """Test displaying multiple projects on the projects page."""
    # Add multiple projects to database
    for project in sample_projects:
        DAL.save_project(project['title'], project['description'], project['image'])
    
    # View projects page
    response = client.get('/projects')
    assert response.status_code == 200
    
    # Verify all projects are displayed
    for project in sample_projects:
        assert project['title'].encode() in response.data
        assert project['description'].encode() in response.data


def test_navigation_workflow(client, app):
    """Test navigation between different pages."""
    # Test navigation from home to projects
    response = client.get('/')
    assert response.status_code == 200
    
    # Navigate to projects
    response = client.get('/projects')
    assert response.status_code == 200
    
    # Navigate to add project
    response = client.get('/projects/add')
    assert response.status_code == 200
    
    # Navigate back to projects
    response = client.get('/projects')
    assert response.status_code == 200


def test_static_files_integration(client, app):
    """Test that static files are properly served."""
    # Test CSS file
    response = client.get('/static/styles.css')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/css; charset=utf-8'


def test_project_with_image_display(client, app):
    """Test project display with image."""
    # Add project with image
    project_data = {
        'title': 'Project with Image',
        'description': 'This project has an image',
        'image': 'test_image.jpg'
    }
    DAL.save_project(project_data['title'], project_data['description'], project_data['image'])
    
    # View projects page
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'Project with Image' in response.data
    assert b'test_image.jpg' in response.data


def test_project_without_image_display(client, app):
    """Test project display without image."""
    # Add project without image
    project_data = {
        'title': 'Project without Image',
        'description': 'This project has no image',
        'image': ''
    }
    DAL.save_project(project_data['title'], project_data['description'], project_data['image'])
    
    # View projects page
    response = client.get('/projects')
    assert response.status_code == 200
    assert b'Project without Image' in response.data
    assert b'placeholder.png' in response.data  # Should show placeholder


def test_form_persistence_on_error(client, app):
    """Test that form data persists when validation fails."""
    # Submit form with invalid data
    invalid_data = {
        'title': '',  # Invalid: empty title
        'description': 'This description should persist',
        'image': 'persistent_image.jpg'
    }
    response = client.post('/projects/add', data=invalid_data)
    assert response.status_code == 200
    assert b'Title is required' in response.data
    
    # Check that form fields retain their values
    assert b'This description should persist' in response.data
    assert b'persistent_image.jpg' in response.data


def test_database_persistence_across_requests(client, app):
    """Test that database changes persist across multiple requests."""
    # Add a project
    project_data = {
        'title': 'Persistence Test Project',
        'description': 'Testing database persistence',
        'image': 'persistence.jpg'
    }
    DAL.save_project(project_data['title'], project_data['description'], project_data['image'])
    
    # Make multiple requests to verify persistence
    for _ in range(3):
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'Persistence Test Project' in response.data


def test_error_handling_integration(client, app):
    """Test error handling in the integrated application."""
    # Test 404 error
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    
    # Test invalid method on existing route
    response = client.put('/projects')
    assert response.status_code == 405  # Method not allowed


def test_project_table_integration(client, app, sample_projects):
    """Test the complete project table integration."""
    # Add projects
    for project in sample_projects:
        DAL.save_project(project['title'], project['description'], project['image'])
    
    # View projects page
    response = client.get('/projects')
    assert response.status_code == 200
    
    # Verify table structure
    assert b'<table' in response.data
    assert b'<thead>' in response.data
    assert b'<tbody>' in response.data
    
    # Verify table headers
    assert b'<th>Image</th>' in response.data
    assert b'<th>Title</th>' in response.data
    assert b'<th>Description</th>' in response.data
    
    # Verify project rows
    for project in sample_projects:
        assert project['title'].encode() in response.data
        assert project['description'].encode() in response.data


def test_add_project_button_integration(client, app):
    """Test the 'Add New Project' button integration."""
    # View projects page
    response = client.get('/projects')
    assert response.status_code == 200
    
    # Verify 'Add New Project' button/link is present
    assert b'Add New Project' in response.data
    assert b'href="/projects/add"' in response.data


def test_redirect_after_successful_submission(client, app):
    """Test that successful form submission redirects correctly."""
    project_data = {
        'title': 'Redirect Test Project',
        'description': 'Testing redirect after submission',
        'image': 'redirect.jpg'
    }
    
    response = client.post('/projects/add', data=project_data)
    assert response.status_code == 302
    assert response.location.endswith('/projects')
    
    # Follow the redirect
    response = client.get(response.location)
    assert response.status_code == 200
    assert b'Redirect Test Project' in response.data

