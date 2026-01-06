from odoo import models, fields

class BlogCategory(models.Model):
    _name = 'intgration.blog.category'
    _description = 'Blog Category'
    _rec_name = 'name'
    _sql_constraints = [
        ('unique_category_per_application', 'UNIQUE(integration_application_id, name)', 
         'The category name must be unique per application!')
    ]
    
    name = fields.Char(string='Category Name', required=True, index=True, help='The name of the category (must be unique per application)')
    integration_application_id = fields.Many2one('integration.application', string='Application', required=True, index=True, ondelete='cascade', help='The application this category belongs to')
    description = fields.Text(string='Description', help='A detailed description of this category')
    
    
