from dependency_injector import containers, providers
from github import Github

from . import SearchServices
from . import SaveServices

class Container(containers.DeclarativeContainer):

    avilable_save_services = dict(zip(
            [ii.service_name for ii in SaveServices.SaveServiceInterface.__subclasses__()],
            SaveServices.SaveServiceInterface.__subclasses__()))

    print(avilable_save_services)

    wiring_config = containers.WiringConfiguration(modules=[".views"])
    config = providers.Configuration(yaml_files=["config.yml"])

    github_client = providers.Factory(
        Github,
        login_or_token = config.github.auth_token,
        timeout = config.github.request_timeout
    )

    search_service = providers.Factory(
        SearchServices.SearchService,
        github_client = github_client
    )

    save_service = providers.Factory(
        avilable_save_services["pickle"],
        db_path = "pickles_folder" 
    )