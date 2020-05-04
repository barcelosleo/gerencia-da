class Ferramenta():
    def __init__(self, titulo, url, icone, subferramentas = []):
        self.titulo = titulo
        self.url = url
        self.icone = icone
        self.subferramentas = subferramentas

class SubFerramenta():
    def __init__(self, url):
        self.url = url

class Area():
    def __init__(self, titulo, url, ferramentas):
        self.titulo = titulo
        self.url = url
        self.ferramentas = ferramentas

areas = [
    Area('Direção Admnistrativa', 'gestao-administrativo', [
        Ferramenta('Início', 'gestao-administrativo', 'home'),
        Ferramenta('Config. Diretório', 'gestao-config-diretorio', 'settings'),
        Ferramenta('Áreas', 'gestao-areas', 'view_carousel', [
            SubFerramenta('gestao-areas-nova')
        ]),
        Ferramenta('Cargos', 'gestao-cargos', 'contacts', [
            SubFerramenta('gestao-cargos-novo'),
        ]),
        Ferramenta('Diretores', 'gestao-diretores', 'people', [
            SubFerramenta('gestao-diretores-cargos'),
        ]),
        Ferramenta('Associados', 'gestao-associados', 'people_outline', [
            SubFerramenta('gestao-associados-novo'),
        ]),
        Ferramenta('Egressos', 'gestao-egressos', 'check', [
            SubFerramenta('gestao-egressos-novo'),
        ])
    ]),
    Area('Comunicação', 'gestao-eventos', []),
    Area('Financeiro', 'gestao-financeira', []),
    Area('Eventos', 'gestao-eventos', []),
]