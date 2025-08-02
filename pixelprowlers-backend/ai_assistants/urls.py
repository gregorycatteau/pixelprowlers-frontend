from django.urls import path
from . import views

urlpatterns = [
    path("ask-agents/", views.ask_agent_view, name="ask_all_agents"),  # nouvelle route explicite
    path("ask-<str:agent_name>/", views.ask_agent_view, name="ask_specific_agent"),
]
