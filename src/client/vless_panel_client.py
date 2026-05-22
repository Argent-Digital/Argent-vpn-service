import httpx
import uuid

from src.schemas.vless_schema import LoginData, VlessClientInit, KeyData, ClientData, AddClientPayload, InboundSettingsWrap

class VlessPanelClient:
    def __init__(self, panel_data: VlessClientInit):
        self.ux_url = panel_data.ux_url.rstrip("/")
        self.ux_pass = panel_data.ux_pass
        self.ux_username = panel_data.ux_username
        self.vless_inbound = panel_data.vless_inbound
        self.ip = panel_data.ip
        self.path = panel_data.path
        self.port = 10000

        self.client = httpx.AsyncClient(
            base_url=self.ux_url,
            verify=False,
            timeout=httpx.Timeout(10.0, connect=5.0)
        )

    async def close(self):
        await self.client.aclose()
        
    async def login(self) -> bool:
        try:
            url = "/login"
            data = LoginData(password=self.ux_pass, username=self.ux_username)
            headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": f"{self.ux_url}/"
                }
            
            response = await self.client.post(url, data=data.model_dump(), headers=headers)

            if response.status_code == 200:
                res_json = response.json()
                return res_json.get("success", False)
            
            return False
        except Exception as e:
            print(f"Error login on {self.ux_url}: {e}")
            return False
        
    async def add_client(self, user_data: KeyData):
        client_uuid = str(uuid.uuid4())
        email = f"user_{user_data.user_id}"

        client_data = ClientData(id=client_uuid, email=email, tgId=user_data.user_id)
        base = self.ux_url.strip('/')
        url = f"{base}/panel/api/inbounds/addClient"
        payload = AddClientPayload(id=self.vless_inbound, settings=InboundSettingsWrap(clients=[client_data]))

        try:
            res = await self.client.post(url=url, data=payload)

            if not res:
                return None, f"None res"
            
            data = res.json()
            if data.get("success"):
                vless_link = (
                        f"vless://{client_uuid}@{self.ip}:{self.port}?"
                        f"type=ws&encryption=none&path={self.path}&host=&security=none"
                        f"#Argent-speed_{user_data.user_id}"
                    )
                return vless_link, client_uuid
            else:
                return None, "Panel reject"
            
        except Exception as e:
            return None, f"Add client error: {e}"

