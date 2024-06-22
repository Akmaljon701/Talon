from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.enums import talon_number_choices
from talon.views import login_page, talon_list, export_docx, logout_view, add_talon

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('enum/talon_numbers/', talon_number_choices, name='talon_number_choices'),

    # path('', login_page, name='login_page'),
    # path('logout/', logout_view, name='logout'),
    # path('talon-list/', talon_list, name='talon_list'),
    # path('export_docx/', export_docx, name='export_docx'),
    # path('add-talon/', add_talon, name='add_talon'),

    path('user/', include('user.urls')),
    path('talon/', include('talon.urls'))
]
