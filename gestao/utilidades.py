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
        Ferramenta('Atas de Reunião', 'gestao-reunioes', 'book', [
            SubFerramenta('gestao-reunioes-nova'),
        ]),
        Ferramenta('Associados', 'gestao-associados', 'people_outline', [
            SubFerramenta('gestao-associados-novo'),
        ]),
        Ferramenta('Egressos', 'gestao-egressos', 'check', [
            SubFerramenta('gestao-egressos-novo'),
        ]),
        # Ferramenta('Interessados no Curso', 'gestao-egressos', 'child_friendly', [
        #     SubFerramenta('gestao-egressos-novo'),
        # ]),
        Ferramenta('Diretores', 'gestao-diretores', 'people', [
            SubFerramenta('gestao-diretores-cargos'),
        ]),
        Ferramenta('Cargos', 'gestao-cargos', 'contacts', [
            SubFerramenta('gestao-cargos-novo'),
        ]),
        Ferramenta('Áreas', 'gestao-areas', 'view_carousel', [
            SubFerramenta('gestao-areas-nova')
        ]),
        Ferramenta('Config. Diretório', 'gestao-config-diretorio', 'settings'),
    ]),
    Area('Comunicação', 'gestao-logout', []),
    Area('Financeiro', 'gestao-logout', []),
    Area('Eventos', 'gestao-logout', []),
]