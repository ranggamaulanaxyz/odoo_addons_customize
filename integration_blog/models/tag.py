from odoo import models, fields

class BlogTag(models.Model):
    _name = 'intgration.blog.tag'
    _description = 'Blog Tag'
    _rec_name = 'name'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 
         'The tag name must be unique!')
    ]
    
    name = fields.Char(string='Tag Name', required=True, index=True, help='The name of the tag (must be globally unique across all applications)')
    color = fields.Integer(string='Color', help='Color index for the tag display')
