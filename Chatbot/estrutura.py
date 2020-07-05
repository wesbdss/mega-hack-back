import aiml
import unidecode
import os
import json

class aimlbot:
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.learn('std-startup.xml')
        self.kernel.respond('load aiml b')
        self.last = ''
    
    def response(self,input:str):
        input = unidecode.unidecode(input)
        input = input.lower()
        if self.last == input:
            return 'Por favor , não floode'
        self.last = input
        #remove itens
        resposta= self.kernel.respond(input)
        if resposta.lower() == 'notarget':
            #armazena labels não treinadas
            with open('naotreinadas','a+',encoding="utf8") as f:
                lines = f.readlines()
                lines.append(input+'\n')
                f.writelines(lines)
                f.close()
            return 'Não Possuo "{}" na minha base de dados.'.format(input)
        else:
            if resposta.find('command') >= 0:
                #lista de comandos
                opcao = resposta.split(':')[1]
                if opcao == 'help':
                    return 'Comando *help*:\n*livros* - para obter os 10 primeiros livros\n*ler livro <nome do livro>* para que eu leia o livro para você'
                if opcao == 'listadelivros':
                    livros = os.listdir('./livros')
                    lista = ''
                    for livro in livros:
                        with open('./livros/{}'.format(livro),'r',encoding="utf8") as f:
                            data = json.load(f)
                            lista = lista+data['title']+'\n'
                            f.close()
                    return lista
                
                try:
                    if opcao.split(' ')[0] == 'selecionarlivro':
                        opcao = opcao.replace('selecionarlivro ','')
                        opcao = unidecode.unidecode(opcao)
                        livros = os.listdir('./livros')
                        texto = []
                        for livro in livros:
                            with open('./livros/{}'.format(livro),'r',encoding="utf8") as f:
                                data = json.load(f)
                                f.close()
                                if data['title'].lower() == opcao.lower():
                                    for linha in data['historia']:
                                        texto.append(linha['text'])
                                    return texto
                except Exception as ex:
                    print("erro no selecionar livros ", ex)
                    return 'historia "{}" não está registrada'.format(opcao)
            else:
                return resposta

