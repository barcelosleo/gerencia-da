from django import template

register = template.Library()

@register.simple_tag(name='verifica_area')
def verifica_area(url_atual, area):
    for ferramenta in area.ferramentas:
        if url_atual == ferramenta.url:
            return True
        for subferramenta in ferramenta.subferramentas:
            if url_atual == subferramenta.url:
                return True
    return False

@register.simple_tag(name='verifica_area_subferramenta')
def verifica_area_subferramenta(url_atual, ferramenta):
    if url_atual == ferramenta.url:
        return True
    for subferramenta in ferramenta.subferramentas:
        if url_atual == subferramenta.url:
            return True
    return False