from django.urls import path
from .views import jared_dashboard_view, jared_admin_summary_view

urlpatterns = [
    path("cockpit/", jared_dashboard_view, name="jared_dashboard"),
    path("admin/jared-dashboard/", jared_admin_summary_view, name="jared_admin_summary"),
]
