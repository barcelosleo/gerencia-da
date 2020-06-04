from django import template

register = template.Library()

@register.filter(name='dinheiro')
def dinheiro(valor):
    a = '{:,.2f}'.format(float(valor))
    b = a.replace(',', 'v')
    c = b.replace('.', ',')
    return c.replace('v', '.')