# Laboratório de Protocol Buffers

Neste tutorial supõe-se que o sistema operacional utilizado é uma versão 64 bits do Windows. 

## Instalação do compilador do Protocol Buffers

O compilador que será instalado é responsável por gerar as classes a partir do arquivo _.proto_ e que serão utilizadas durante o desenvolvimento. Para isso, é necessário ir até o repositório do [Protocol Buffers](https://github.com/protocolbuffers/protobuf/releases) e baixar um dos releases da página (dê preferência ao arquivo _protoc-3.11.2-win64.zip_).  
  
Após terminar o download, descompacte o arquivo dentro da pasta _protoc-3.11.2-win64_ e abra o prompt de comando dentro dessa pasta para que possamos registrar o compilador no _path_ do sistema operacional.

Supondo que a pasta _protoc-3.11.2-win64_ foi criada dentro da pasta _Downloads_, utilize o seguinte comando para concatenar o compilador ao _path_:
```
set PATH = %PATH%;%USERPROFILE%\Downloads\protoc-3.11.2-win64\bin
```
Ainda no prompt de comando, digite `protoc --version` para verificar se o compilador está funcionando corretamente.

Lembre-se de não fechar esse terminal até que o tutorial esteja concluído.

## Criação do Projeto Python

Utilizando o sua IDE favorita, crie um projeto _python_ para ser utilizado nesse tutorial e logo após instale o _protobuf_ utilizando o gerenciador de pacotes do Python.

```sh #!/bin/bash
pip install protobuf
```

Com o pacote do _protobuf_ instalado, é hora de definir o esquema que será compilado para gerar as classes do projeto.

## Criação do Arquivo .proto

Crie um arquivo chamado _schema.proto_ na raiz da pasta do projeto criado anteriormente e dentro escreva o seguinte código:
```
syntax = "proto3";  
  
package laboratorio;  
  
message Telefone {  
    enum TipoTelefone {  
        CELULAR = 0;  
        RESIDENCIAL = 1;  
        TRABALHO = 2;  
    }  
  
    string telefone = 1;  
    TipoTelefone tipo = 2;  
}  
  
message Aluno {  
   string nome = 1;  
   string matricula = 2;  
   repeated Telefone telefones = 3;  
}  
  
message Turma {  
    repeated Aluno alunos = 1;  
}
```

Analisando o código acima, neste arquivo utilizamos diversas palavras-chave para definir a sintaxe e a estrutura das mensagens a serem criadas.  
  
Na primeira linha, a palavra-chave _syntax_ é utilizada para definir a sintaxe utilizada nesse arquivo. Até o momento, o Protocol Buffers trabalha com dois tipos de sintaxe: a _proto2_ e a _proto3_. A principal diferença entre elas é na forma em como são declarados os tipos das propriedades das mensagens.  
  
Outra palavra reservada existente no arquivo é _message_, utilizada para definir um novo tipo de mensagem. As mensagens semelhantes às classes na orientação a objetos e nelas podemos definir os seus atributos usando tipos escalares (int, double, float, string e etc) ou tipo pré-definidos.  

## Gerando as Classes Necessárias  
  
Novamente de volta ao terminal, mas dessa vez, aberto dentro da pasta onde está localizado o arquivo _schema.proto_, execute o seguinte comando:  
```sh #!/bin/bash
protoc --python_out=./classes ./schema.proto  
```  
O comando _protoc_ é usado para compilar o arquivo _schema.proto_ e a opção _--python_out_ indica que a saída deverá ser um código em Python a ser colocado dentro da pasta _classes_. Após isso, vá até essa pasta chamada _classes_ e repare lá que foi criado um arquivo chamado _schema_pb2.py_. É a partir desse arquivo que serão importadas as classes utilizadas nesse projeto.

## Serializando Objetos com Protocol Buffers  
  
Agora é hora de criar o arquivo onde será escrito o código responsável por serializar os objetos criados e escrevê-los em um arquivo binário. Para isso, crie um arquivo chamado _serializacao.py_ na raiz da pasta do projeto e dentro escreva o seguinte código:

```python
from classes.schema_pb2 import Aluno, Telefone, Turma


def main():
    aluno = Aluno(nome="José Carlos da Silva", matricula="2018370254", telefones=[])
    aluno.telefones.append(Telefone(telefone="(83) 3215-5123", tipo=Telefone.RESIDENCIAL))

    turma = Turma(alunos=[])
    turma.alunos.append(aluno)

    with open("turma", "wb") as file:
        file.write(turma.SerializeToString())

if __name__ == "__main__":
    main()
```

Na primeira linha, repare que importamos as classes _Aluno_, _Telefone_ e _Turma_ a partir do arquivo _schema_pb2_. Logo em seguida, na função _main_, foi instanciado um aluno chamado "José Carlos da Silva" e, logo após, adicionamos um objeto do tipo Telefone em sua lista de telefones.  
  
Repare que na instanciação do telefone, o atributo tipo recebe um valor chamado _Telefone.RESIDENCIAL_. Isso acontece porque o enum declarado no arquivo _.proto_ foi transformado em constantes da classe Telefone após a compilação.  
  
Após a instanciação do aluno, criamos um objeto turma e dentro da lista de alunos desse objeto e incluímos nele o aluno criado anteriormente.  
  
Para serializar o objeto, é necessário abrir um arquivo no modo de escrita binária e dentro desse arquivo escrever os bytes do objeto gerados a partir do método _SerializeToString_.


## Desserializando Objetos com Protocol Buffers  
  
Novamente, crie um arquivo chamado _desserializacao.py_ na raiz da pasta do projeto e dentro escreva o seguinte código:  

``` python
from classes.schema_pb2 import Turma


def main():
    turma = Turma()

    with open("turma", "rb") as file:
        turma.ParseFromString(file.read())

    for aluno in turma.alunos:
        print("O aluno {0} possui {1} telefone(s) cadastrado(s).".format(aluno.nome, len(aluno.telefones)))


if __name__ == "__main__":
    main()
```
  
Antes de ler o arquivo foi necessário criar um objeto do tipo _Turma_ que será populado com os dados lidos a partir arquivo criado anteriormente. Logo em seguida, abrimos o arquivo binário no modo de leitura binária e, utilizando o método _ParseFromString_ populamos o objeto com dados obtidos a partir do arquivo.  
  
Para comprovar que os dados foram desserializados da forma correta, utilizou-se um for para listar alguns dados dos alunos.