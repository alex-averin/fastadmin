from fastadmin.models.helpers import get_admin_model


async def test_change(session_id, admin_models, event, client):
    assert session_id
    event_admin_model = admin_models[event.__class__]
    fields = event_admin_model.get_model_fields()
    participant_model_cls_name: str = fields["participants"]["parent_model"]
    participant_model = f"{event_admin_model.model_name_prefix}.{participant_model_cls_name}"
    participant_admin_model = get_admin_model(participant_model)
    participant = await participant_admin_model.save_model(None, {"username": "participant", "password": "test"})
    r = await client.patch(
        f"/api/change/{event.get_model_name()}/{event.id}",
        json={
            "name": "new name",
            "participants": [participant["id"]],
        },
    )
    assert r.status_code == 200, r.text

    updated_event = await event_admin_model.get_obj(event.id)
    item = r.json()
    assert item["id"] == updated_event["id"]
    assert item["name"] == updated_event["name"]
    assert item["tournament_id"] == updated_event["tournament_id"]
    assert item["created_at"] == updated_event["created_at"].isoformat()
    assert item["updated_at"] == updated_event["updated_at"].isoformat()
    assert item["participants"] == [participant["id"]]

    r = await client.delete(f"/api/delete/{participant_model}/{participant['id']}")
    assert r.status_code == 200, r.text


async def test_change_405(session_id, event, client):
    assert session_id
    r = await client.get(
        f"/api/change/{event.get_model_name()}/{event.id}",
    )
    assert r.status_code == 405, r.text


async def test_change_401(superuser, event, client):
    r = await client.patch(
        f"/api/change/{event.get_model_name()}/{event.id}",
        json={
            "name": "new name",
            "participants": [superuser.id],
        },
    )
    assert r.status_code == 401, r.text


async def test_change_404_admin_class_found(session_id, admin_models, superuser, event, client):
    assert session_id
    del admin_models[event.__class__]
    r = await client.patch(
        f"/api/change/{event.get_model_name()}/{event.id}",
        json={
            "name": "new name",
            "participants": [superuser.id],
        },
    )
    assert r.status_code == 404, r.text


async def test_change_404_obj_not_found(session_id, superuser, event, client):
    assert session_id
    r = await client.patch(
        f"/api/change/{event.get_model_name()}/invalid",
        json={
            "name": "new name",
            "participants": [superuser.id],
        },
    )
    assert r.status_code == 422, r.text

    r = await client.patch(
        f"/api/change/{event.get_model_name()}/-1",
        json={
            "name": "new name",
            "participants": [superuser.id],
        },
    )
    assert r.status_code == 404, r.text
