import aiml
import unidecode
import os
import json
import ast
import time


class aimlbot:
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.learn('std-startup.xml')
        self.kernel.respond('load aiml b')
        self.last = []
        self.users=[]

    def login(self, input:str,contact:str):
        if contact in self.users:
            return self.response(input,contact)
        else:
            try:
                v = ast.literal_eval(input)
                if type(v) == int:
                    self.users.append(contact)
                    self.last.append((contact,input))
                    return 'Acesso Liberado :)\nTente usar o comando HELP para ver as funcionalidades!!'
            except Exception as ex:
                print(ex)
                return 'Olá sou Genini, Por Favor Insira seu código de acesso: \nSe não houver digite "123"'

    def response(self, input: str,contact:str):
        input = unidecode.unidecode(input)
        input = input.lower()
        #anti flooding
        for tam in range(len(self.last)):
            contato,fala = self.last[tam]
            if contato == contact:
                if fala == input:
                    return 'Por favor Não floode!'
                else:
                    self.last[tam] = ((contato,input))
            else:
                pass
        
        # remove itens
        resposta = self.kernel.respond(input)
        if resposta.lower() == 'notarget':
            # armazena labels não treinadas
            with open('naotreinadas.txt', 'a+', encoding="utf8") as f:
                lines = f.readlines()
                lines.append(input+'\n')
                f.writelines(lines)
                f.close()
            return 'Não Possuo "{}" na minha base de dados.'.format(input)
        else:
            if resposta.find('command') >= 0:
                # lista de comandos
                opcao = resposta.split(':')[1]
                if opcao == 'help':
                    return 'Comando *help*:\n\n> *livros* - para obter os 10 primeiros livros\n> *ler livro <nome do livro>* para que eu leia o livro para você'
                if opcao == 'listadelivros':
                    livros = os.listdir('./livros')
                    lista = ''
                    for livro in livros:
                        with open('./livros/{}'.format(livro), 'r', encoding="utf8") as f:
                            data = json.load(f)
                            lista = lista+data['title']+'\n'
                            f.close()
                    return lista

                try:
                    if opcao.split(' ')[0] == 'selecionarlivro':
                        opcao = opcao.replace('selecionarlivro ', '')
                        opcao = unidecode.unidecode(opcao)
                        opcao = opcao.rstrip()
                        opcao = opcao.lstrip()
                        livros = os.listdir('./livros')
                        print('Opção de selecionar livros por ',contact, " ->",opcao,"<-")
                        texto = []
                        texto.append("Então eu vou lhe contar...\n")
                        time.sleep(2.4)

                        for livro in livros:
                            with open('./livros/{}'.format(livro), 'r', encoding="utf8") as f:
                                data = json.load(f)
                                f.close()
                                print("Livro escolhido ",data['title'].lower()," com a opção ",opcao.lower())
                                nome = unidecode.unidecode(data['title'])
                                if nome.lower() == opcao.lower():
                                    for linha in data['historia']:
                                        texto.append(linha['text'])
                                    return texto.append("*FIM*")
                        return 'O livro {} não foi encontrado na base de livros'.format(opcao)
                except Exception as ex:
                    print("erro no selecionar livros ", ex)
                    return 'historia "{}" não está registrada'.format(opcao)
            else:
                return resposta
