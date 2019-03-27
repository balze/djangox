from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
	
class IndexPageView(TemplateView):
    # def as_view():

    template_name = 'pages/index_base.html'

