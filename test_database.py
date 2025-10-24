"""
Tests for database operations and data access layer.
"""
import pytest
import sqlite3
import os
import DAL


def test_database_initialization(app):
    """Test that init_db creates the projects table."""
    # The database should be initialized by the app fixture
    db_path = DAL.get_db_path()
    assert os.path.exists(db_path)
    
    # Check that the table exists
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects';")
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    assert result[0] == 'projects'


def test_database_table_structure(app):
    """Test that the projects table has the correct structure."""
    db_path = DAL.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table schema
    cursor.execute("PRAGMA table_info(projects);")
    columns = cursor.fetchall()
    conn.close()
    
    # Check that all expected columns exist
    column_names = [col[1] for col in columns]
    expected_columns = ['id', 'Title', 'Description', 'ImageFileName', 'CreatedAt']
    
    for expected_col in expected_columns:
        assert expected_col in column_names


def test_save_project_basic(app):
    """Test saving a basic project."""
    project_id = DAL.save_project("Test Project", "Test Description", "test.jpg")
    assert project_id is not None
    assert isinstance(project_id, int)
    assert project_id > 0


def test_save_project_without_image(app):
    """Test saving a project without an image."""
    project_id = DAL.save_project("Test Project", "Test Description")
    assert project_id is not None
    assert isinstance(project_id, int)


def test_save_project_empty_strings(app):
    """Test saving a project with empty strings."""
    project_id = DAL.save_project("Test Project", "", "")
    assert project_id is not None
    assert isinstance(project_id, int)


def test_save_project_none_image(app):
    """Test saving a project with None image."""
    project_id = DAL.save_project("Test Project", "Test Description", None)
    assert project_id is not None
    assert isinstance(project_id, int)


def test_get_all_projects_empty(app):
    """Test getting all projects from empty database."""
    projects = DAL.get_all_projects()
    assert projects == []
    assert isinstance(projects, list)


def test_get_all_projects_with_data(app, sample_projects):
    """Test getting all projects with data."""
    # Add projects to database
    for project in sample_projects:
        DAL.save_project(project['title'], project['description'], project['image'])
    
    projects = DAL.get_all_projects()
    assert len(projects) == len(sample_projects)
    
    # Check that projects are returned in descending order by id
    for i in range(len(projects) - 1):
        assert projects[i]['id'] > projects[i + 1]['id']


def test_get_project_by_id_existing(app, sample_project):
    """Test getting a project by existing ID."""
    project_id = DAL.save_project(
        sample_project['title'],
        sample_project['description'],
        sample_project['image']
    )
    
    retrieved_project = DAL.get_project_by_id(project_id)
    assert retrieved_project is not None
    assert retrieved_project['id'] == project_id
    assert retrieved_project['Title'] == sample_project['title']
    assert retrieved_project['Description'] == sample_project['description']
    assert retrieved_project['ImageFileName'] == sample_project['image']


def test_get_project_by_id_nonexistent(app):
    """Test getting a project by non-existent ID."""
    retrieved_project = DAL.get_project_by_id(99999)
    assert retrieved_project is None


def test_get_project_by_id_invalid(app):
    """Test getting a project with invalid ID."""
    retrieved_project = DAL.get_project_by_id(-1)
    assert retrieved_project is None


def test_delete_project_existing(app, sample_project):
    """Test deleting an existing project."""
    project_id = DAL.save_project(
        sample_project['title'],
        sample_project['description'],
        sample_project['image']
    )
    
    # Verify project exists
    retrieved_project = DAL.get_project_by_id(project_id)
    assert retrieved_project is not None
    
    # Delete project
    DAL.delete_project(project_id)
    
    # Verify project is deleted
    retrieved_project = DAL.get_project_by_id(project_id)
    assert retrieved_project is None


def test_delete_project_nonexistent(app):
    """Test deleting a non-existent project."""
    # This should not raise an exception
    DAL.delete_project(99999)


def test_project_data_integrity(app):
    """Test that project data is stored and retrieved correctly."""
    title = "Special Characters: !@#$%^&*()"
    description = "Description with\nnewlines and\ttabs"
    image = "image with spaces.jpg"
    
    project_id = DAL.save_project(title, description, image)
    retrieved_project = DAL.get_project_by_id(project_id)
    
    assert retrieved_project['Title'] == title
    assert retrieved_project['Description'] == description
    assert retrieved_project['ImageFileName'] == image


def test_multiple_projects_same_title(app):
    """Test saving multiple projects with the same title."""
    title = "Duplicate Title"
    project_id1 = DAL.save_project(title, "Description 1", "image1.jpg")
    project_id2 = DAL.save_project(title, "Description 2", "image2.jpg")
    
    assert project_id1 != project_id2
    
    projects = DAL.get_all_projects()
    titles = [p['Title'] for p in projects]
    assert titles.count(title) == 2


def test_project_created_at_timestamp(app, sample_project):
    """Test that CreatedAt timestamp is set."""
    project_id = DAL.save_project(
        sample_project['title'],
        sample_project['description'],
        sample_project['image']
    )
    
    retrieved_project = DAL.get_project_by_id(project_id)
    assert retrieved_project['CreatedAt'] is not None
    assert retrieved_project['CreatedAt'] != ''


def test_get_db_path(app):
    """Test that get_db_path returns a valid path."""
    db_path = DAL.get_db_path()
    assert isinstance(db_path, str)
    assert os.path.exists(db_path)


def test_database_isolation(app):
    """Test that each test gets its own isolated database."""
    # This test verifies that the database is properly isolated between tests
    # by checking that we start with an empty database
    projects = DAL.get_all_projects()
    assert len(projects) == 0

