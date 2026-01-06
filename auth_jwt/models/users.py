from odoo import models
from odoo.tools import config
from datetime import datetime, timezone, timedelta
import jwt
import uuid
import logging

_logger = logging.getLogger(__name__)

DEFAULT_JWT_SECRET_KEY = 'Hk5U4qM6xWgb_YzmlfJYq7hF8nGZ1E0qzDbN6oL0x5Q'

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _jwt_secret_key(self):
        secret_key = config.get('jwt_secret_key', DEFAULT_JWT_SECRET_KEY)
        if secret_key == DEFAULT_JWT_SECRET_KEY:
            _logger.warning("You are using default JWT secret key!")
        return secret_key
    
    def _jwt_expiration_time(self, duration=60):
        """Generate JWT expiration timestamp
        
        Args:
            duration: Token lifetime in seconds
            
        Returns:
            Unix timestamp (seconds since epoch)
        """
        now_utc = datetime.now(timezone.utc)
        exp_time = now_utc + timedelta(seconds=duration)
        exp_timestamp = int(exp_time.timestamp())
        
        _logger.info(f"JWT Token - Current UTC: {now_utc}, Expiration: {exp_time}, Duration: {duration}s, Timestamp: {exp_timestamp}")
        
        return exp_timestamp   
    
    def _jwt_generate_token(self, payload, algorithm="HS256"):
        secret_key = self._jwt_secret_key()
        token = jwt.encode(payload, secret_key, algorithm)
        return token
    
    def _jwt_decode_token(self, token):
        secret_key = self._jwt_secret_key()
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            _logger.info(f"Token decoded successfully. Payload: {payload}")
        except jwt.exceptions.ExpiredSignatureError as e:
            payload = {}
            try:
                # Decode without verification to see the expiration time
                unverified = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_signature": True, "verify_exp": False})
                exp_time = datetime.fromtimestamp(unverified.get('exp', 0), tz=timezone.utc)
                now_time = datetime.now(timezone.utc)
                time_diff = (now_time - exp_time).total_seconds()
                _logger.warning(f"Token EXPIRED - Expired at: {exp_time} UTC, Current time: {now_time} UTC, Expired {time_diff}s ago. Error: {e}")
            except Exception as decode_error:
                _logger.warning(f"Token is expired and could not decode for details: {e}, Decode error: {decode_error}")
        except Exception as e:
            payload = {}
            _logger.warning(f"Token is invalid: {e}")
        return payload

    def _jwt_generate_access_token(self):
        self.ensure_one()
        company = self.company_id
        exp = self._jwt_expiration_time(company.jwt_access_token_duration)
        payload = {
            'sub': str(self.id),
            'exp': exp,
            'type': 'access'
        }
        token = self._jwt_generate_token(payload)
        return token
    
    def _jwt_generate_refresh_token(self, token_id=None):
        company = self.company_id
        exp = self._jwt_expiration_time(company.jwt_refresh_token_duration)
        new_token_id = str(uuid.uuid4())
        payload = {
            'sub': str(self.id),
            'exp': exp,
            'jti': new_token_id,
            'type': 'refresh'
        }
        token = self._jwt_generate_token(payload)
        RefreshToken = self.env['res.users.jwt.refresh']
        hash_new_token_id = RefreshToken._hash_token_id(new_token_id)
        existing_refresh_token = RefreshToken._browse_token(self.id, token_id)
        if existing_refresh_token:
            existing_refresh_token.write({'hash_token_id': hash_new_token_id})
        else:
            RefreshToken.create({
                'hash_token_id': hash_new_token_id,
                'user_id': self.id,
            })
        return token