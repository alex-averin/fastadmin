from fastadmin.models.base import ModelAdmin
from fastadmin.models.helpers import get_admin_model
from fastadmin.models.schemas import ModelFieldWidgetSchema


async def test_add(authorized_client, admin_models, event):
    event_admin_model: ModelAdmin = admin_models[event.__class__]
    fields = event_admin_model.get_model_fields_with_widget_types()

    participants_field: ModelFieldWidgetSchema = next((f for f in fields if f.name == "participants"), None)
    assert participants_field
    tournament_field: ModelFieldWidgetSchema = next((f for f in fields if f.name == "tournament"), None)
    assert tournament_field

    participants_model_cls_name = participants_field.form_widget_props["parentModel"]
    participants_model = f"{event_admin_model.model_name_prefix}.{participants_model_cls_name}"
    participants_admin_model = get_admin_model(participants_model)
    participant = await participants_admin_model.save_model(None, {"username": "participant", "password": "test"})

    tournament_model_cls_name = tournament_field.form_widget_props["parentModel"]
    tournament_model = f"{event_admin_model.model_name_prefix}.{tournament_model_cls_name}"
    tournament_admin_model = get_admin_model(tournament_model)
    tournament = await tournament_admin_model.save_model(None, {"name": "test_tournament"})

    r = await authorized_client.post(
        f"/api/add/{event.get_model_name()}",
        json={
            "name": "new name",
            "tournament": tournament["id"],
            "participants": [participant["id"]],
        },
    )
    assert r.status_code == 200, r.text
    item = r.json()
    updated_event = await event_admin_model.get_obj(item["id"])
    assert item["name"] == "new name"
    assert item["tournament"] == tournament["id"]
    assert item["created_at"] == updated_event["created_at"].isoformat()
    assert item["updated_at"] == updated_event["updated_at"].isoformat()
    assert item["participants"] == [participant["id"]]
    r = await authorized_client.delete(f"/api/delete/{event.get_model_name()}/{item['id']}")
    assert r.status_code == 200, r.text
    r = await authorized_client.delete(f"/api/delete/{participants_model}/{participant['id']}")
    assert r.status_code == 200, r.text
    r = await authorized_client.delete(f"/api/delete/{tournament_model}/{tournament['id']}")
    assert r.status_code == 200, r.text


async def test_add_405(authorized_client, event):
    r = await authorized_client.get(
        f"/api/add/{event.get_model_name()}",
    )

    assert r.status_code == 405, r.text


async def test_add_401(superuser, tournament, event, client):
    r = await client.post(
        f"/api/add/{event.get_model_name()}",
        json={
            "name": "new name",
            "tournament": tournament.id,
            "participants": [superuser.id],
        },
    )

    assert r.status_code == 401, r.text


async def test_add_404(authorized_client, admin_models, superuser, tournament, event):
    del admin_models[event.__class__]

    r = await authorized_client.post(
        f"/api/add/{event.get_model_name()}",
        json={
            "name": "new name",
            "tournament": tournament.id,
            "participants": [superuser.id],
        },
    )

    assert r.status_code == 404, r.text
