class Ferramenta():
    def __init__(self, titulo, url, icone):
        self.titulo = titulo
        self.url = url
        self.icone = icone

class Area():
    def __init__(self, titulo, url, ferramentas):
        self.titulo = titulo
        self.url = url
        self.ferramentas = ferramentas