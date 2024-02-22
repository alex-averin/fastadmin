from fastadmin.api.service import get_user_id_from_session_id


async def test_delete(authorized_client, event):
    r = await authorized_client.delete(
        f"/api/delete/{event.get_model_name()}/{event.id}",
    )
    obj_id = r.json()

    assert r.status_code == 200, r.text
    assert str(obj_id) == str(event.id)


async def test_configuration_405(authorized_client, event):
    r = await authorized_client.get(
        f"/api/delete/{event.get_model_name()}/{event.id}",
    )

    assert r.status_code == 405, r.text


async def test_delete_401(event, client):
    r = await client.delete(
        f"/api/delete/{event.get_model_name()}/{event.id}",
    )

    assert r.status_code == 401, r.text


async def test_delete_404(authorized_client, admin_models, event):
    del admin_models[event.__class__]

    r = await authorized_client.delete(
        f"/api/delete/{event.get_model_name()}/{event.id}",
    )

    assert r.status_code == 404, r.text


async def test_delete_403(authorized_client, session_id, superuser):
    assert session_id
    user_id = await get_user_id_from_session_id(session_id)
    assert user_id
    r = await authorized_client.delete(
        f"/api/delete/{superuser.get_model_name()}/{user_id}",
    )

    assert r.status_code == 403, r.text


async def test_delete_422(authorized_client, event):
    r = await authorized_client.delete(
        f"/api/delete/{event.get_model_name()}/invalid",
    )

    assert r.status_code == 422, r.text
