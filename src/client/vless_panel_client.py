import uuid

import httpx

from src.schemas.vless_schema import (
    AddKeyReturn,
    KeyData,
    KeyDelData,
    LoginData,
    VlessClientInit,
)


class VlessPanelClient:
    def __init__(self, panel_data: VlessClientInit):
        self.ux_url = panel_data.ux_url.rstrip("/") + "/"
        self.ux_pass = panel_data.ux_pass
        self.ux_username = panel_data.ux_username
        self.vless_inbound = panel_data.vless_inbound
        self.ip = panel_data.ip
        self.path = panel_data.path
        self.port = panel_data.port
        self.reality_public_key = panel_data.reality_public_key
        self.reality_short_id = panel_data.reality_short_id

        self.client = httpx.AsyncClient(
            base_url=self.ux_url,
            verify=False,
            cookies=httpx.Cookies(),
            timeout=httpx.Timeout(10.0, connect=5.0),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": self.ux_url,
            }
        )

    async def close(self):
        await self.client.aclose()

    async def login(self) -> bool:
        try:
            csrf_res = await self.client.get("csrf-token")
            print(f"🛡️ [CSRF] url={csrf_res.request.url} | status={csrf_res.status_code}")

            if csrf_res.status_code == 200:
                csrf_token = csrf_res.json().get("obj")
                if csrf_token:
                    self.client.headers["X-CSRF-Token"] = str(csrf_token)


            data = LoginData(password=self.ux_pass, username=self.ux_username)
            response = await self.client.post("login", data=data.model_dump())

            print(f"🔑 [LOGIN] url={response.request.url} | status={response.status_code} | body={response.text}")

            if response.status_code == 200:
                res_json = response.json()
                return res_json.get("success", False)

            return False
        except Exception as e:
            print(f"❌ Error login on {self.ux_url}: {e}")
            return False

    async def add_client(self, user_data: KeyData) -> AddKeyReturn | None:
        client_uuid = str(uuid.uuid4())
        short_id = client_uuid[:4]
        email = f"user_{user_data.user_id}_{short_id}"
        sub_id = f"argent_{user_data.user_id}_{short_id}"

        url = "panel/api/clients/add"

        payload = {
            "client": {
                "id": client_uuid,
                "auth": client_uuid,
                "email": email,
                "subId": sub_id,
                "totalGB": 0,
                "expiryTime": 0,
                "tgId": int(user_data.user_id),
                "limitIp": 0,
                "limitHwid": 0,
                "enable": True,
            },
            "inboundIds": [1,],
        }

        try:
            res = await self.client.post(url=url, json=payload)
            print(f"🔍 [ADD_CLIENT] url={res.request.url} | status={res.status_code} | body={res.text}")

            if res.status_code != 200:
                return None

            data = res.json()
            if data.get("success"):
                sub_link = f"https://key.argentvpn.ru/sub/{sub_id}"
                return AddKeyReturn(
                    key_name=email,
                    access_url=sub_link,
                    vless_uuid=client_uuid,
                )
            else:
                print(f"❌ Panel returned False: {data.get('msg')}")
                return None

        except Exception as e:
            print(f"🔥 Critical error in add_client: {e}")
            return None

    async def del_client(self, key_data: KeyDelData) -> bool:
        short_id = str(key_data.vless_uuid)[:4]
        emails_to_try = [
            f"user_{key_data.user_id}_{short_id}",
            f"user_{key_data.user_id}",
        ]
        if getattr(key_data, "key_name", None) and key_data.key_name not in emails_to_try:
            emails_to_try.insert(0, key_data.key_name)

        try:
            for email in emails_to_try:
                url = f"panel/api/clients/del/{email}"
                res = await self.client.post(url, params={"keepTraffic": 0})
                print(f"🗑️ [DEL_CLIENT] try email={email} | status={res.status_code} | body={res.text}")

                if res.status_code == 200 and res.json().get("success"):
                    return True

            return False

        except Exception as e:
            print(f"❌ Ошибка в del_client: {e}")
            return False