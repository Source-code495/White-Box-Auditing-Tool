import markdown
from markupsafe import Markup

def init_extensions(app):
    @app.context_processor
    def utility_processor():
        return dict(markdown=markdown_filter)

    def markdown_filter(text):
        html = markdown.markdown(
            text,
            extensions=['fenced_code', 'tables', 'codehilite'],
            extension_configs={
                'codehilite': {
                    'use_pygments': False,
                    'css_class': 'code-highlight'
                }
            }
        )
        return Markup(html)