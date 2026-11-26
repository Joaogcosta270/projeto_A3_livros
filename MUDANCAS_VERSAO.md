# Nova versão - Seus Livros

Nesta atualização, o layout foi reorganizado por completo:

- O cadastro deixou de ficar na coluna lateral e passou para uma faixa horizontal no topo.
- O acervo passou de cartões grandes para uma lista em linhas, com título, autor, ano, status e ações.
- Os indicadores agora incluem quantidade de empréstimos atrasados.
- A página de empréstimos tem um painel com prazos e os estados **Em dia**, **Vence em breve**, **Atrasado** e **Devolvido**.
- Foram adicionados filtros por prazo e exportação da lista de livros para CSV.
- O CSV trata aspas e ponto e vírgula em nomes de livros e protege campos que começam com caracteres interpretáveis como fórmula em planilhas.
- O visual foi atualizado com verde-petróleo, coral discreto e tipografia mais equilibrada.

## Como atualizar no VS Code sem perder os livros

Faça uma cópia da pasta anterior. Depois, copie o novo `index.html` para a mesma pasta e use o mesmo endereço do Live Server. A chave do LocalStorage continua `bookflow_layout_v1`.

Se você abrir o novo projeto em outra porta/endereço, os dados poderão não aparecer, porque LocalStorage é separado por origem.

## Testes

- `python tests/testes_interface.py`: 45 testes funcionais atuais anteriores + 2 reproduções históricas de defeitos.
- `python tests/testes_novidades.py`: 15 testes novos.
- Total: **60 testes funcionais da versão atual aprovados** + **2 demonstrações de bugs da versão anterior**. Teste de F5 real no navegador do aluno ainda pendente.
