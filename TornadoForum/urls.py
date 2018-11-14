from apps.users import urls as user_urls
from apps.community import urls as community_urls

urlpattern = []

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern
