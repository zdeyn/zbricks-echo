from typing import Dict, List, Type, Union
import zbricks
import project

User, Permission = zbricks.get_bricks('auth.User', 'auth.Permission')

class BlogDomain(zbricks.base.zDomain):
    name: str = 'blog'
    depends: Dict[str, List[Union[str, zbricks.zBrick]]] = {
        'instances': ['storage.zStorage'],  # Instance fulfilling the zStorage interface
        'entities': ['auth.zUser', 'auth.zRole', 'auth.zPermission'],  # Subclasses of zEntity dataclass
        'queries': ['auth.zUser.has_permission', 'auth.zUser.get_permissions'],  # Query functions zBricks
    }
    exposes: Dict[str, List[Union[str, zbricks.zBrick]]] = {
        'entities': ['Post', 'Comment', 'Reaction'],
        'permissions': [
            'post.create', 
            'post.read', 
            'post.modify_own', 'post.modify_outrank', 'post.modify_any',
            'post.delete_own', 'post.delete_outrank', 'post.delete_any',
            'post.react', 'post.unreact', 'post.hide', 
            'comment.create',
            'comment.read',
            'comment.modify_own', 'comment.modify_outrank', 'comment.modify_any', 
            'comment.delete_own', 'comment.delete_outrank', 'comment.delete_any',
            'comment.react', 'comment.unreact', 'comment.hide', 
        ],
        'roles': ['anonymous', 'user(anonymous)', 'author(user)', 'moderator(author)', 'admin(moderator)'],
        'role:permissions': [
            'anonymous=post.read|comment.read',
            'user=post.react|post.unreact|comment.create|comment.react|comment.unreact',
            'author=post.create|post.modify_own|post.delete_own|comment.hide',
            'moderator=post.hide|comment.modify_any|comment.delete_any',
            'admin=post.modify_any|post.delete_any|comment.modify_any|comment.delete_any',
        ],
        'commands': ['post.create', 'post.modify', 'post.delete', 'comment.create', 'comment.modify', 'comment.delete'],
        'queries': ['post.get', 'comment.get', 'reaction.get'],
    }

def create_app(layout: zbricks.zLayout = None, config: zbricks.zConfig = None) -> zbricks.zApp:
    layout = layout or project.get_layout()  # Get connections between zBricks
    config = config or project.get_config()  # Load configuration from class and environment

    # Added validation to ensure layout and config are correctly loaded
    if layout is None or config is None:
        raise ValueError("Failed to load layout or config.")

    app: zbricks.zApp = zbricks.assemble_app(layout=layout, config=config)  # Ready to run!
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()  # Runs the localhost development server with settings from `config` above
