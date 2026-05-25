import asyncio
from outline_vpn.outline_vpn import OutlineVPN
from src.schemas.outline_schema import OutlineLoginData, OutlineCreateKey, OutlineCreateKeyReturn

class OutlinePanelClient:
    def login(self, session_data: OutlineLoginData):
        try:
            self.client = OutlineVPN(api_url=session_data.out_url, cert_sha256=session_data.out_cert)
        except Exception as e:
            print(f"Error onit Outline client: {e}")
            self.client = None

    async def outline_create_key(self, data: OutlineCreateKey) -> OutlineCreateKeyReturn:
        if not self.client:
            print("❌ Error: Outline client is not initialized")
            return None
        try:
            new_key = await asyncio.to_thread(self.client.create_key)

            key_id = int(new_key.key_id)
            key_url = f"{new_key.access_url}&prefix=POST%20"
            key_name = f"User_{data.user_id}"

            await asyncio.to_thread(self.client.rename_key, key_id=key_id, name=key_name)

            res = OutlineCreateKeyReturn(key_name=key_name, access_url=key_url)
            return res
        except Exception as e:
            print(f"Error create key: {e}")
            return None

    async def outline_del_key(self, server_key_id: str) -> bool:
        if not self.client:
            print("❌ Error: Outline client is not initialized")
            return False
        try:
            success = await asyncio.to_thread(self.client.delete_key, server_key_id)
            return success
        except Exception as e:
            print(f"Error can't del key: {e}")
            return False