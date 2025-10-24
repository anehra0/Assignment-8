"""
Tests for project CRUD operations and business logic.
"""
import pytest
import DAL


def test_create_project_complete_data(app):
    """Test creating a project with complete data."""
    title = "Complete Project"
    description = "This is a complete project description"
    image = "complete_project.jpg"
    
    project_id = DAL.save_project(title, description, image)
    assert project_id is not None
    
    # Verify the project was created correctly
    project = DAL.get_project_by_id(project_id)
    assert project is not None
    assert project['Title'] == title
    assert project['Description'] == description
    assert project['ImageFileName'] == image


def test_create_project_minimal_data(app):
    """Test creating a project with minimal required data."""
    title = "Minimal Project"
    description = ""  # Empty description
    
    project_id = DAL.save_project(title, description)
    assert project_id is not None
    
    # Verify the project was created correctly
    project = DAL.get_project_by_id(project_id)
    assert project is not None
    assert project['Title'] == title
    assert project['Description'] == ''
    assert project['ImageFileName'] == ''


def test_read_project_by_id(app, sample_project):
    """Test reading a project by ID."""
    project_id = DAL.save_project(
        sample_project['title'],
        sample_project['description'],
        sample_project['image']
    )
    
    project = DAL.get_project_by_id(project_id)
    assert project is not None
    assert project['id'] == project_id
    assert project['Title'] == sample_project['title']
    assert project['Description'] == sample_project['description']
    assert project['ImageFileName'] == sample_project['image']


def test_read_all_projects(app, sample_projects):
    """Test reading all projects."""
    # Add multiple projects
    for project in sample_projects:
        DAL.save_project(project['title'], project['description'], project['image'])
    
    all_projects = DAL.get_all_projects()
    assert len(all_projects) == len(sample_projects)
    
    # Verify all projects are present
    titles = [p['Title'] for p in all_projects]
    for project in sample_projects:
        assert project['title'] in titles


def test_read_projects_ordering(app):
    """Test that projects are returned in correct order (newest first)."""
    # Create projects with delays to ensure different timestamps
    project1_id = DAL.save_project("First Project", "First description")
    project2_id = DAL.save_project("Second Project", "Second description")
    project3_id = DAL.save_project("Third Project", "Third description")
    
    all_projects = DAL.get_all_projects()
    assert len(all_projects) == 3
    
    # Should be ordered by ID descending (newest first)
    assert all_projects[0]['id'] == project3_id
    assert all_projects[1]['id'] == project2_id
    assert all_projects[2]['id'] == project1_id


def test_delete_project(app, sample_project):
    """Test deleting a project."""
    project_id = DAL.save_project(
        sample_project['title'],
        sample_project['description'],
        sample_project['image']
    )
    
    # Verify project exists
    project = DAL.get_project_by_id(project_id)
    assert project is not None
    
    # Delete the project
    DAL.delete_project(project_id)
    
    # Verify project is deleted
    project = DAL.get_project_by_id(project_id)
    assert project is None


def test_delete_nonexistent_project(app):
    """Test deleting a project that doesn't exist."""
    # Should not raise an exception
    DAL.delete_project(99999)


def test_project_lifecycle(app):
    """Test complete project lifecycle: create, read, delete."""
    # Create
    title = "Lifecycle Project"
    description = "Testing complete lifecycle"
    image = "lifecycle.jpg"
    
    project_id = DAL.save_project(title, description, image)
    assert project_id is not None
    
    # Read
    project = DAL.get_project_by_id(project_id)
    assert project is not None
    assert project['Title'] == title
    assert project['Description'] == description
    assert project['ImageFileName'] == image
    
    # Verify it appears in all projects
    all_projects = DAL.get_all_projects()
    project_ids = [p['id'] for p in all_projects]
    assert project_id in project_ids
    
    # Delete
    DAL.delete_project(project_id)
    
    # Verify deletion
    project = DAL.get_project_by_id(project_id)
    assert project is None
    
    # Verify it no longer appears in all projects
    all_projects = DAL.get_all_projects()
    project_ids = [p['id'] for p in all_projects]
    assert project_id not in project_ids


def test_multiple_projects_management(app):
    """Test managing multiple projects."""
    # Create multiple projects
    projects_data = [
        {"title": "Project A", "description": "Description A", "image": "a.jpg"},
        {"title": "Project B", "description": "Description B", "image": "b.jpg"},
        {"title": "Project C", "description": "Description C", "image": "c.jpg"}
    ]
    
    project_ids = []
    for project_data in projects_data:
        project_id = DAL.save_project(
            project_data["title"],
            project_data["description"],
            project_data["image"]
        )
        project_ids.append(project_id)
    
    # Verify all projects exist
    all_projects = DAL.get_all_projects()
    assert len(all_projects) == len(projects_data)
    
    # Delete middle project
    middle_id = project_ids[1]
    DAL.delete_project(middle_id)
    
    # Verify only 2 projects remain
    all_projects = DAL.get_all_projects()
    assert len(all_projects) == 2
    
    # Verify correct projects remain
    remaining_titles = [p['Title'] for p in all_projects]
    assert "Project A" in remaining_titles
    assert "Project C" in remaining_titles
    assert "Project B" not in remaining_titles


def test_project_data_types(app):
    """Test that project data is stored with correct types."""
    title = "Type Test Project"
    description = "Testing data types"
    image = "type_test.jpg"
    
    project_id = DAL.save_project(title, description, image)
    project = DAL.get_project_by_id(project_id)
    
    # Check data types
    assert isinstance(project['id'], int)
    assert isinstance(project['Title'], str)
    assert isinstance(project['Description'], str)
    assert isinstance(project['ImageFileName'], str)
    assert isinstance(project['CreatedAt'], str)


def test_empty_string_handling(app):
    """Test handling of empty strings in project data."""
    project_id = DAL.save_project("", "", "")
    project = DAL.get_project_by_id(project_id)
    
    assert project is not None
    assert project['Title'] == ""
    assert project['Description'] == ""
    assert project['ImageFileName'] == ""


def test_unicode_handling(app):
    """Test handling of unicode characters in project data."""
    title = "Unicode Project: 测试项目 🚀"
    description = "Description with émojis and spéciál châracters"
    image = "unicode_image_测试.jpg"
    
    project_id = DAL.save_project(title, description, image)
    project = DAL.get_project_by_id(project_id)
    
    assert project is not None
    assert project['Title'] == title
    assert project['Description'] == description
    assert project['ImageFileName'] == image


def test_long_text_handling(app):
    """Test handling of long text in project data."""
    long_title = "A" * 1000  # 1000 character title
    long_description = "B" * 5000  # 5000 character description
    image = "long_text_test.jpg"
    
    project_id = DAL.save_project(long_title, long_description, image)
    project = DAL.get_project_by_id(project_id)
    
    assert project is not None
    assert project['Title'] == long_title
    assert project['Description'] == long_description
    assert project['ImageFileName'] == image

