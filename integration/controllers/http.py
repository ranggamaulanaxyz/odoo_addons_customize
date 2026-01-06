from odoo.http import Controller, request
from werkzeug.exceptions import BadRequest, TooManyRequests
from collections import defaultdict
from time import time
import json

# In-memory store for rate limiting: {ip: [timestamp1, timestamp2, ...]}
_rate_limit_store = defaultdict(list)


class RestApiController(Controller):
    
    def throttle(self, max_requests=5, window_seconds=60, key=None):
        """
        Check rate limit for the current request.
        
        Args:
            max_requests: Maximum number of requests allowed in the time window
            window_seconds: Time window in seconds
            key: Optional custom key (defaults to IP address)
            
        Raises:
            TooManyRequests: If rate limit is exceeded
        """
        if key is None:
            key = request.httprequest.remote_addr
        
        now = time()
        
        # Clean old entries outside the time window
        _rate_limit_store[key] = [
            t for t in _rate_limit_store[key] 
            if now - t < window_seconds
        ]
        
        # Check if limit exceeded
        if len(_rate_limit_store[key]) >= max_requests:
            raise TooManyRequests("Rate limit exceeded. Please try again later.")
        
        # Record this request
        _rate_limit_store[key].append(now)

    def response_data(self, success=True, message="", data={}, meta={}):
        response_data = {
            'success': success,
            'message': message,
            'data': data,
            'meta': meta
        }
        return response_data
