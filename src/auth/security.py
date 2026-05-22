from jose import jwt, JWTError
from typing import Optional

from src.config import settings
from src.schemas.jwt_schema import TokenData

def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY_FOR_JWT,
            algorithms=[settings.ALGORITHM]
        )

        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            return None
        
        return TokenData(user_id=int(user_id_str))
    
    except (JWTError, ValueError):
        return None