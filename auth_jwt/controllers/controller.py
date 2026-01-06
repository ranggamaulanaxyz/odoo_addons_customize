from odoo import http
from odoo.http import request

class Controller(http.Controller):
    def _response_error(self, code, message):
        """Helper to format JSON responses consistently"""
        # Adjust this structure to match your frontend client's expectations
        return {
            "status": "error",
            "code": code,
            "message": message
        }

    def _response_success(self, code, message=None, data={}):
        """Helper to format JSON responses consistently"""
        # Adjust this structure to match your frontend client's expectations
        response = {
            "status": "success",
            "code": code,
        }
        if message:
            response['message'] = message
        if data:
            response['data'] = data
        return response