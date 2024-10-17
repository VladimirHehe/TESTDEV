import pytest
from db_test import client


def test_create_post():
    """Тест создания поста"""
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/posts", json=post_data)
    assert response.status_code == 200
    assert response.json()["title"] == post_data["title"]


def test_get_post():
    """Тест показа поста"""
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/posts", json=post_data)
    post_id = response.json()["id"]

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == post_data["title"]


def test_update_post():
    """Тест изменения поста"""
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/posts", json=post_data)
    post_id = response.json()["id"]

    updated_data = {"title": "Updated Post", "content": "This is an updated test post."}
    response = client.put(f"/posts/{post_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]


def test_delete_post():
    """Тест удаления поста"""
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/posts", json=post_data)
    post_id = response.json()["id"]

    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == f"Post id {post_id} deleted successfully"


def test_get_all_posts():
    """Тест показа всех постов"""
    post_data_1 = {"title": "Post 1", "content": "Content 1"}
    post_data_2 = {"title": "Post 2", "content": "Content 2"}
    client.post("/posts", json=post_data_1)
    client.post("/posts", json=post_data_2)

    response = client.get("/posts")
    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_like_post():
    """Тест лайка поста"""
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/posts", json=post_data)
    post_id = response.json()["id"]

    response = client.post(f"/posts/{post_id}/like")
    assert response.status_code == 200
    assert response.json()["post_id"] == post_id


def test_delete_post_like():
    """Тест удаления поста"""
    post_data = {"title": "Test Post", "content": "This is a test post."}
    response = client.post("/posts", json=post_data)
    post_id = response.json()["id"]

    client.post(f"/posts/{post_id}/like")
    response = client.delete(f"/posts/{post_id}/like")
    assert response.status_code == 200
    assert response.json()["detail"] == f"Like in post {post_id} deleted successfully"
