from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.enums import talon_number_choices
from talon_template.views import (login_page, export_docx, logout_view, talon_add, get_talons_1_2_3_view,
                                  load_organizations, talon_update)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('enum/talon_numbers/', talon_number_choices, name='talon_number_choices'),

    path('', login_page, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('export_docx/', export_docx, name='export_docx'),
    path('add-talon/', talon_add, name='add_talon'),
    path('talon_update/<int:talon_id>/', talon_update, name='talon_update'),
    path('load_organizations/', load_organizations, name='load_organizations'),
    path('talons/', get_talons_1_2_3_view, name='get_talons_1_2_3_view'),

    path('user/', include('user.urls')),
    path('talon/', include('talon.urls'))
]
