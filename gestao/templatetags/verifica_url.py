from django import template

register = template.Library()

@register.simple_tag(name='verifica_area')
def verifica_area(url_atual, area):
    for ferramenta in area.ferramentas:
        if url_atual == ferramenta.url:
            return True
    return False