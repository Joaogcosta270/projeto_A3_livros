# Seus Livros

Sistema de gerenciamento de biblioteca desenvolvido como projeto acadêmico para a atividade A3 da faculdade.

O **Seus Livros** permite organizar o acervo de uma biblioteca, gerenciar usuários e controlar empréstimos e devoluções de forma simples e intuitiva.

## Funcionalidades

- **Cadastro de livros:** inclusão de livros com geração automática de códigos sequenciais.
- **Edição e exclusão:** gerenciamento das informações dos livros cadastrados.
- **Pesquisa e filtros:** localização de livros no acervo.
- **Cadastro de usuários:** registro dos usuários da biblioteca.
- **Empréstimos:** controle da retirada de livros.
- **Devoluções:** atualização automática da disponibilidade dos livros.
- **Histórico:** acompanhamento dos empréstimos e devoluções.
- **Indicadores:** visualização de informações sobre o acervo e os empréstimos.
- **Controle de atrasos:** identificação de empréstimos com devolução pendente.

## Tecnologias utilizadas

- HTML5
- CSS3
- JavaScript
- LocalStorage

## Regras de negócio

- Cada livro recebe um código sequencial automático, seguindo o padrão `LIV001`, `LIV002` e assim por diante.
- A edição de um livro preserva seu código de identificação.
- Códigos de livros excluídos não são reutilizados.
- Ao realizar um empréstimo, a disponibilidade do livro é atualizada.
- Após a devolução, a disponibilidade é restaurada.
- O prazo máximo de empréstimo é de **3 meses de calendário**.

## Testes

O projeto passou por verificações funcionais e de interface, contemplando diferentes cenários de utilização.

- 45 testes de lógica.
- 38 verificações de interface.

Os testes contemplaram cadastros, edições, exclusões, empréstimos, devoluções e regras de negócio.

## Como executar

1. Faça o download ou clone este repositório.
2. Localize o arquivo HTML principal.
3. Abra o arquivo no navegador.
4. Utilize as funcionalidades disponíveis no sistema.

Não é necessário instalar dependências ou configurar um servidor para executar a versão atual.

## Sobre o projeto

Este projeto foi desenvolvido como parte da atividade acadêmica A3, com o objetivo de aplicar conhecimentos de desenvolvimento web, lógica de programação, manipulação de dados e implementação de regras de negócio.

Desenvolvido por **Lucas Nascimento** **João Gabriel Costa** **Gabrielle Cardim** **João Victor Amorim**