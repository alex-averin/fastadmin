async def test_export(authorized_client, event):
    async with authorized_client.stream("POST", f"/api/export/{event.get_model_name()}", json={}) as r:
        assert r.status_code == 200
        rows = [line async for line in r.aiter_lines()]
    assert rows


async def test_export_405(authorized_client, event):
    r = await authorized_client.get(f"/api/export/{event.get_model_name()}")

    assert r.status_code == 405


async def test_export_401(client, event):
    async with client.stream("POST", f"/api/export/{event.get_model_name()}", json={}) as r:
        assert r.status_code == 401


async def test_export_404(authorized_client, admin_models, event):
    del admin_models[event.__class__]

    async with authorized_client.stream("POST", f"/api/export/{event.get_model_name()}", json={}) as r:
        assert r.status_code == 404
