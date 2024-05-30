import zbricks
import project # type: ignore

def create_app(layout : zbricks.zLayout|None = None, config : zbricks.zConfig|None = None) -> zbricks.zApp: # type: ignore
    layout : zbricks.zLayout = project.get_layout() # type: ignore # contains the connections between zBricks
    config : zbricks.zConfig = project.get_config() # type: ignore # loads configuration from class and environment

    app : zbricks.zApp = zbricks.assemble_app(layout = layout, config = config) # type: ignore # ready to run
    return app

if __name__ == '__main__':
    app = create_app()
    app.run() # runs the localhost development server with settings from `config` above