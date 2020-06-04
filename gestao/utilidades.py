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
            SubFerramenta('gestao-reunioes-editar'),
            SubFerramenta('gestao-reunioes-ver'),
            SubFerramenta('gestao-reunioes-remover'),
        ]),
        Ferramenta('Alunos', 'gestao-associados', 'people_outline', [
            SubFerramenta('gestao-associados-novo'),
            SubFerramenta('gestao-associados-editar'),
            SubFerramenta('gestao-associados-ver'),
            SubFerramenta('gestao-associados-remover'),
        ]),
        Ferramenta('Egressos', 'gestao-egressos', 'check', [
            SubFerramenta('gestao-egressos-novo'),
            SubFerramenta('gestao-egressos-editar'),
            SubFerramenta('gestao-egressos-ver'),
            SubFerramenta('gestao-egressos-remover'),
        ]),
        # Ferramenta('Interessados no Curso', 'gestao-egressos', 'child_friendly', [
        #     SubFerramenta('gestao-egressos-novo'),
        # ]),
        Ferramenta('Grupos', 'gestao-grupos', 'people_outline', [
            SubFerramenta('gestao-grupos-novo'),
            SubFerramenta('gestao-grupos-editar'),
            SubFerramenta('gestao-grupos-remover'),
        ]),
        Ferramenta('Diretores', 'gestao-diretores', 'people', [
            SubFerramenta('gestao-diretores-novo'),
            SubFerramenta('gestao-diretores-editar'),
            SubFerramenta('gestao-diretores-ver'),
            SubFerramenta('gestao-diretores-remover'),
        ]),
        Ferramenta('Link de Cadastro', 'gestao-links-cadastro', 'contacts', [
            SubFerramenta('gestao-links-cadastro-novo'),
            SubFerramenta('gestao-links-cadastro-editar'),
            SubFerramenta('gestao-links-cadastro-ver'),
            SubFerramenta('gestao-links-cadastro-remover'),
        ]),
        Ferramenta('Áreas', 'gestao-areas', 'view_carousel', [
            SubFerramenta('gestao-areas-nova'),
            SubFerramenta('gestao-areas-editar'),
            SubFerramenta('gestao-areas-remover'),
        ]),
        Ferramenta('Config. Diretório', 'gestao-config-diretorio', 'settings'),
    ]),
    Area('Financeiro', 'financeiro-inicio', [
        Ferramenta('Início', 'financeiro-inicio', 'home'),
        Ferramenta('Vendas', 'financeiro-vendas', 'shopping_cart', [
            SubFerramenta('financeiro-vendas-nova'),
            SubFerramenta('financeiro-vendas-editar'),
            SubFerramenta('financeiro-vendas-remover'),
            SubFerramenta('financeiro-vendas-ver'),
            SubFerramenta('financeiro-vendas-parcelas'),
        ]),
        Ferramenta('Entradas Financeiras', 'financeiro-entradas', 'archive', [
            SubFerramenta('financeiro-entradas-nova'),
            SubFerramenta('financeiro-entradas-editar'),
            SubFerramenta('financeiro-entradas-remover'),
            SubFerramenta('financeiro-entradas-ver'),
        ]),
        Ferramenta('Saídas Financeiras', 'financeiro-saidas', 'unarchive', [
            SubFerramenta('financeiro-saidas-nova'),
            SubFerramenta('financeiro-saidas-editar'),
            SubFerramenta('financeiro-saidas-remover'),
            SubFerramenta('financeiro-saidas-ver'),
        ]),
        Ferramenta('Transferências Financeiras', 'financeiro-transferencias', 'repeat', [
            SubFerramenta('financeiro-transferencias-nova'),
            SubFerramenta('financeiro-transferencias-editar'),
            SubFerramenta('financeiro-transferencias-remover'),
            SubFerramenta('financeiro-transferencias-ver'),
        ]),
        Ferramenta('Produtos', 'financeiro-produtos', 'shopping_cart', [
            SubFerramenta('financeiro-produtos-novo'),
            SubFerramenta('financeiro-produtos-editar'),
            SubFerramenta('financeiro-produtos-remover'),
            SubFerramenta('financeiro-produtos-ver'),
        ]),
        Ferramenta('Carteiras', 'financeiro-carteiras', 'markunread_mailbox', [
            SubFerramenta('financeiro-carteiras-nova'),
            SubFerramenta('financeiro-carteiras-editar'),
            SubFerramenta('financeiro-carteiras-remover'),
            SubFerramenta('financeiro-carteiras-ver'),
        ]),
    ]),
    Area('Comunicação', 'gestao-logout', []),
    Area('Eventos', 'gestao-logout', []),
]