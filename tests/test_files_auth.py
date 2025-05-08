# from tests.conftest import client, login


# def test_get_tasks_authorized(test_task, client):
#     token = login(client)
#     url = "/tasks"
#     response = client.get(
#         url,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
#
# def test_get_tasks_status(test_task, client):
#     token = login(client)
#     status = "pending"
#     url = f'/tasks?status={status}'
#     response = client.get(
#         url,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()[0]['title'] == "Test Task"
#     assert response.json()[0]['description'] == "This is a test task"
#     assert response.json()[0]['status'] == "pending"
#     assert response.json()[0]['priority'] == 2
#     assert response.json()[0]['id'] == 1
#     assert response.json()[0]['owner_id'] == 1
#
#
# def test_get_tasks_priority(test_task, client):
#     token = login(client)
#     priority = 2
#     url = f'/tasks?priority={priority}'
#     response = client.get(
#         url,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()[0]['title'] == "Test Task"
#     assert response.json()[0]['description'] == "This is a test task"
#     assert response.json()[0]['status'] == "pending"
#     assert response.json()[0]['priority'] == 2
#     assert response.json()[0]['id'] == 1
#     assert response.json()[0]['owner_id'] == 1
#
#
# def test_post_tasks(client):
#     token = login(client)
#     url = '/tasks'
#     data = {
#         "title": "Mikola",
#         "description": "Descr",
#         "status": "pending",
#         "priority": 2
#     }
#     response = client.post(
#         url,
#         json=data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()['title'] == "Mikola"
#     assert response.json()['description'] == "Descr"
#     assert response.json()['status'] == "pending"
#     assert response.json()['priority'] == 2
#     assert response.json()['id'] == 1
#     assert response.json()['owner_id'] == 1
#
#
# def test_post_tasks_descr_none(client):
#     token = login(client)
#     url = '/tasks'
#     data = {
#         "title": "Mikola",
#         "status": "pending",
#         "priority": 2
#     }
#     response = client.post(
#         url,
#         json=data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()['title'] == "Mikola"
#     assert response.json()['description'] == None
#     assert response.json()['status'] == "pending"
#     assert response.json()['priority'] == 2
#     assert response.json()['id'] == 1
#     assert response.json()['owner_id'] == 1
#
#
# def test_put_tasks(test_task, client):
#     token = login(client)
#     url = '/tasks/1'
#     data = {
#         "title": "Mikola",
#         "description": "Descr",
#         "status": "done",
#         "priority": 2
#     }
#     response = client.put(
#         url,
#         json=data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()['title'] == "Mikola"
#     assert response.json()['description'] == "Descr"
#     assert response.json()['status'] == "done"
#     assert response.json()['priority'] == 2
#     assert response.json()['id'] == 1
#     assert response.json()['owner_id'] == 1
#
#
# def test_get_search_tasks(test_task, client):
#     token = login(client)
#     q = 'task'
#     url = f'/tasks/search?q={q}'
#     response = client.get(
#         url,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()[0]['title'] == "Test Task"
#     assert response.json()[0]['description'] == "This is a test task"
#     assert response.json()[0]['status'] == "pending"
#     assert response.json()[0]['priority'] == 2
#     assert response.json()[0]['id'] == 1
#     assert response.json()[0]['owner_id'] == 1
