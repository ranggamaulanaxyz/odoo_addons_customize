from odoo import models, fields, api
import re
import random
import string
from datetime import datetime

class BlogArticle(models.Model):
    _name = 'intgration.blog.article'
    _description = 'Article'
    _rec_name = 'title'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('unique_slug_per_application', 'UNIQUE(integration_application_id, slug)', 
         'The slug must be unique per application!')
    ]
    
    integration_application_id = fields.Many2one('integration.application', string='Application', required=True, index=True, ondelete='cascade', help='The application this article belongs to')
    slug = fields.Char(string='Slug', required=True, index=True, help='URL-friendly identifier (lowercase letters, numbers, and hyphens only). Auto-generated from title if left empty.')
    title = fields.Char(string='Title', required=True, index=True, help='The title of the article')
    content = fields.Html(string='Content', help='The main content of the article (supports HTML formatting)')
    author_user_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user, help='The user who created this article')
    category_ids = fields.Many2many('intgration.blog.category', string='Categories', help='Categories this article belongs to')
    tag_ids = fields.Many2many('intgration.blog.tag', string='Tags', help='Tags associated with this article')
    excerpt = fields.Text(string='Excerpt', help='A short summary or preview of the article')
    is_published = fields.Boolean(string='Published', default=False, help='Whether this article is published and visible to readers')
    publish_date = fields.Datetime(string='Publish Date', help='The date and time when this article was published')
    view_count = fields.Integer(string='Views', default=0, help='Number of times this article has been viewed')
    comment_count = fields.Integer(string='Comments', default=0, help='Number of comments on this article')
    
    @api.onchange('title')
    def _onchange_title_generate_slug(self):
        """Auto-generate slug from title"""
        if self.title and not self.slug:
            # Convert title to URL-friendly slug
            slug = re.sub(r'[^\w\s-]', '', self.title.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            # Check uniqueness within the same application
            if self.integration_application_id:
                existing = self.search([
                    ('integration_application_id', '=', self.integration_application_id.id),
                    ('slug', '=', slug),
                    ('id', '!=', self.id or 0)
                ])
                
                # Add random suffix if slug already exists
                if existing:
                    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                    slug = f"{slug}-{random_suffix}"
            
            self.slug = slug
    
    @api.constrains('slug')
    def _check_slug_format(self):
        """Validate slug format - must be URL-friendly"""
        for record in self:
            if record.slug:
                # Check if slug contains only lowercase letters, numbers, and hyphens
                if not re.match(r'^[a-z0-9-]+$', record.slug):
                    raise models.ValidationError(
                        'Slug must only contain lowercase letters, numbers, and hyphens. '
                        'Invalid slug: {}'.format(record.slug)
                    )
                
                # Check if slug starts or ends with hyphen
                if record.slug.startswith('-') or record.slug.endswith('-'):
                    raise models.ValidationError(
                        'Slug cannot start or end with a hyphen. '
                        'Invalid slug: {}'.format(record.slug)
                    )
                
                # Check for consecutive hyphens
                if '--' in record.slug:
                    raise models.ValidationError(
                        'Slug cannot contain consecutive hyphens. '
                        'Invalid slug: {}'.format(record.slug)
                    )
    
    def publish(self):
        """Publish the article"""
        self.write({
            'is_published': True,
            'publish_date': fields.Datetime.now()
        })
        return True