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