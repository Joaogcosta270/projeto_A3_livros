# Análise de caixa branca - funções e caminhos

A análise considera os caminhos realmente exercitados pela automação, com foco em decisões simples em vez de uma métrica sofisticada de cobertura de código.

| Trecho do `index.html` | Condição / decisão | Caminho verdadeiro | Caminho falso | Casos associados |
|---|---|---|---|---|
| `validateBook` | `!title` | Título vazio gera erro | Título preenchido não gera erro | CT02, CT07 |
| `validateBook` | `!author` | Autor vazio gera erro | Autor preenchido prossegue | CT03, CT07 |
| `validateBook` | `!/\d{1,4}/` (regex de ano, com âncoras) | Ano `2e3` é rejeitado | Ano `1899` é aceito | CT06, CT07 |
| `validateBook` | Ano menor que 1 ou maior que 2026 | Anos 0 e 2027 são rejeitados | Anos 1 e 2026 são aceitos | CT04, CT05, CT09, CT10 |
| `validateLoan` | `!borrower` | Empréstimo sem leitor é barrado | Nome preenchido prossegue | CT21, CT25 |
| `validateLoan` | `dueDate < loanDate` | Previsão anterior é barrada | Data posterior prossegue | CT23, CT25 |
| `validateLoan` | `loanDate > today()` | Retirada futura é barrada | Retirada hoje é aceita | CT24, CT25 |
| `validateLoan` | `dueDate < today()` | Previsão passada é barrada | Previsão futura prossegue | CT22, CT25 |
| `activeLoan` | Existe empréstimo não devolvido | Livro indisponível / bloqueia exclusão | Livro fica disponível | CT25, CT26, CT29, CT34 |
| Salvamento de livro | `editingId` preenchido | Atualiza registro sem trocar código | Cria livro novo com novo código | CT16, CT07 |
| Edição de título | Empréstimo ativo corresponde ao livro | Atualiza título do empréstimo ativo | Não altera outros empréstimos | CT30 |
| `persist` | `localStorage.setItem` falha | Mantém dados só durante a sessão e avisa | Salva no armazenamento simulado | CT39, CT35 |

**Explicação para a apresentação:** em caixa preta observamos entradas e saídas do sistema sem olhar a implementação; em caixa branca examinamos essas condições `if`, as decisões e os diferentes caminhos que precisamos provocar com dados válidos e inválidos.

## RF08 - Prazo máximo de 3 meses
O código calcula a data máxima usando meses de calendário e limita o dia ao último dia do mês-alvo. A interface atualiza `max` do campo de devolução ao mudar a retirada; a função `validateLoan` rejeita qualquer data além do limite, mesmo que o atributo HTML seja contornado. CT41–CT46 exercitam aceitação no limite, rejeição após o limite, prazo curto e limites em fins de mês.
