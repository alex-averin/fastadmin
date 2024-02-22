async def test_retrieve(authorized_client, admin_models, event):
    event_admin_model = admin_models[event.__class__]

    r = await authorized_client.get(
        f"/api/retrieve/{event.get_model_name()}/{event.id}",
    )

    assert r.status_code == 200, r.text
    item = r.json()
    updated_event = await event_admin_model.get_obj(event.id)
    assert item["id"] == updated_event["id"]
    assert item["name"] == updated_event["name"]
    assert item["tournament"] == updated_event["tournament"]
    assert item["created_at"] == updated_event["created_at"].isoformat()
    assert item["updated_at"] == updated_event["updated_at"].isoformat()
    assert "participants" in item
    assert item["participants"]
    assert item["participants"][0] == updated_event["participants"][0]


async def test_list_405(authorized_client, event):
    r = await authorized_client.post(
        f"/api/retrieve/{event.get_model_name()}/{event.id}",
    )
    assert r.status_code == 405, r.text


async def test_retrieve_401(event, client):
    r = await client.get(
        f"/api/retrieve/{event.get_model_name()}/{event.id}",
    )

    assert r.status_code == 401, r.text


async def test_retrieve_404_admin_class_found(authorized_client, admin_models, event):
    del admin_models[event.__class__]

    r = await authorized_client.get(
        f"/api/retrieve/{event.get_model_name()}/{event.id}",
    )

    assert r.status_code == 404, r.text


async def test_retrieve_422_unprocessable_entity(authorized_client, event):
    r = await authorized_client.get(
        f"/api/retrieve/{event.get_model_name()}/invalid",
    )

    assert r.status_code == 422, r.text


async def test_retrieve_404_obj_not_found(authorized_client, event):
    r = await authorized_client.get(
        f"/api/retrieve/{event.get_model_name()}/-1",
    )

    assert r.status_code == 404, r.text
