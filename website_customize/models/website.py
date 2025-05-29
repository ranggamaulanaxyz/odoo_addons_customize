from odoo import models
from werkzeug import urls

class Website(models.Model):
    _inherit = 'website'

    def get_client_action_url(self, url, mode_edit=False):
        action_params = {
            "path": url,
        }
        if mode_edit:
            action_params["enable_editor"] = 1
        return "/app/action-website.website_preview?" + urls.url_encode(action_params)