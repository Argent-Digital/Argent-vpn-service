import httpx
from typing import List

from src.schemas.vless_schema import LoginData, VlessClientInit

class VlessPanelClient:
    def __init__(self, panel_data: VlessClientInit):
        self.ux_url = panel_data.ux_url.rstrip("/")
        self.ux_pass = panel_data.ux_pass
        self.ux_username = panel_data.ux_username
        self.vless_inbound = panel_data.vless_inbound

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