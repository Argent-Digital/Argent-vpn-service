from src.client.vless_panel_client import VlessPanelClient
from src.schemas.billing_schema import DelKeysData
from collections import defaultdict

class VlessCleaner:
    async def billing_del(self, billing_data: DelKeysData):
        vless_keys = defaultdict(list)
        outline_keys = defaultdict(list)

        for key in billing_data.keys_list:
            if key.protocol.lower() == "vless":
                vless_keys[key.node_id].append(key)

            elif key.protocol.lower() == "outline":
                outline_keys[key.node_id].append(key)