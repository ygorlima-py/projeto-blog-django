from site_setup.models import SiteSetup

def context_processor_example(request):
    return {
        'example': 'Isto aqui Veio do Context Processors'
    }

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()

    
    return {
        'site_setup': setup,
    }