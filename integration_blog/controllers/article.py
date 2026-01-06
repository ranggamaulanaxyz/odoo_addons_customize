from odoo import http

class IntegrationBlogArticleController(http.Controller):
    @http.route('/api/article/list', type="json2", auth="none", methods=['GET'], csrf=False)
    def list(self, **kwargs):
        """Get list of published articles"""
        domain = [('is_published', '=', True)]
        
        # Optional: Filter by application ID if provided
        if kwargs.get('application_id'):
            domain.append(('integration_application_id', '=', int(kwargs.get('application_id'))))
            
        articles = http.request.env['intgration.blog.article'].sudo().search(domain, order='publish_date desc')
        
        return {
            'status': 'success',
            'data': [{
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                'view_count': article.view_count,
                'comment_count': article.comment_count,
                'author': article.author_user_id.name,
                'categories': [{'id': c.id, 'name': c.name} for c in article.category_ids],
                'tags': [{'id': t.id, 'name': t.name, 'color': t.color} for t in article.tag_ids],
            } for article in articles]
        }

    @http.route('/api/article/detail/<string:slug>', type="json2", auth="none", methods=['GET'], csrf=False)
    def detail(self, slug, **kwargs):
        """Get details of a published article by slug"""
        article = http.request.env['intgration.blog.article'].sudo().search([
            ('slug', '=', slug),
            ('is_published', '=', True)
        ], limit=1)

        if not article:
             return {'status': 'error', 'message': 'Article not found'}

        # Increment view count
        article.sudo().write({'view_count': article.view_count + 1})

        return {
            'status': 'success',
            'data': {
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt,
                'content': article.content,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                'view_count': article.view_count,
                'comment_count': article.comment_count,
                'author': {
                    'id': article.author_user_id.id,
                    'name': article.author_user_id.name
                },
                'categories': [{'id': c.id, 'name': c.name} for c in article.category_ids],
                'tags': [{'id': t.id, 'name': t.name, 'color': t.color} for t in article.tag_ids],
            }
        }