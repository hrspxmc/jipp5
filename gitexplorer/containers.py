from dependency_injector import containers, providers
from github import Github

from . import SearchServices
from . import SaveServices

def _get_avilable_services(config):
    services_names = [
        ii.service_name for ii in SaveServices.SaveServiceInterface.__subclasses__()
    ]
    services_factories = [
        providers.Factory(jj, db_path=config.db.path)
        for jj in SaveServices.SaveServiceInterface.__subclasses__()
    ]
    return dict(zip(services_names, services_factories))
    
class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".views"])
    config = providers.Configuration(yaml_files=["config.yml"])

    github_client = providers.Factory(
        Github,
        login_or_token=config.github.auth_token,
        timeout=config.github.request_timeout,
    )

    search_service = providers.Factory(
        SearchServices.SearchService, github_client=github_client
    )

    save_service = providers.Selector(
        config.db.engine, **_get_avilable_services(config)
    )
