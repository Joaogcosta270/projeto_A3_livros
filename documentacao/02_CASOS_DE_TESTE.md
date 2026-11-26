# Casos de teste e resultados

**Fonte:** execução automatizada atualizada em 16/11/2026 (fuso America/Sao_Paulo). O resultado refere-se ao ambiente Chromium com LocalStorage simulado. CT40 permanece manual/pendente.

| ID | Cenário | Resultado esperado | Resultado obtido | Situação |
|---|---|---|---|---|
| CT01 | Inicialização do sistema | Contadores iniciam em zero e JavaScript ativo | Cadastro ativo. Preencha os campos e clique em Salvar livro. | Aprovado |
| CT02 | Cadastro sem título/autor/ano | Bloqueio com mensagem | Informe o título do livro. Informe o autor do livro. Informe o ano de publicação | Aprovado |
| CT03 | Cadastro sem autor | Mensagem obrigatória | Informe o autor do livro. | Aprovado |
| CT04 | Ano zero | Rejeitado | O ano deve estar entre 1 e 2026. | Aprovado |
| CT05 | Ano acima de 2026 | Rejeitado | O ano deve estar entre 1 e 2026. | Aprovado |
| CT06 | Ano em notação exponencial 2e3 | Bloqueado como formato inválido | Digite o ano com até 4 algarismos, sem letras ou símbolos. | Aprovado |
| CT07 | Cadastro de livro válido | Aparece como LIV001 e contador 1 | LIV001 Dom Casmurro  Machado de Assis  Publicado em 1899 ● Disponível Editar Emp | Aprovado |
| CT08 | Prévia do código | Próximo código LIV002 | LIV002 | Aprovado |
| CT09 | Livro com ano mínimo 1 | Aceito com LIV002 | LIV001 Dom Casmurro  Machado de Assis  Publicado em 1899 ● Disponível Editar Emp | Aprovado |
| CT10 | Livro de 2026 | Aceito com LIV003 | LIV001 Dom Casmurro  Machado de Assis  Publicado em 1899 ● Disponível Editar Emp | Aprovado |
| CT11 | Pesquisar por título | Só o título correspondente aparece | LIV001 Dom Casmurro  Machado de Assis  Publicado em 1899 ● Disponível Editar Emp | Aprovado |
| CT12 | Pesquisar por autor | Encontra A Arte da Guerra | LIV002 A Arte da Guerra  Sun Tzu  Publicado em 1 ● Disponível Editar Emprestar E | Aprovado |
| CT13 | Filtro emprestados antes do empréstimo | Nenhum cartão visível | ▦ Nenhum livro encontrado  Experimente mudar a busca ou o filtro. | Aprovado |
| CT14 | Editar livro | Formulário preenchido | Dom Casmurro | Aprovado |
| CT15 | Cancelar edição | Retorna a modo cadastro, sem alterar livro | Cadastrar livro | Aprovado |
| CT16 | Salvar edição | Título novo com mesmo LIV002 e 3 livros | LIV001 Dom Casmurro  Machado de Assis  Publicado em 1899 ● Disponível Editar Emp | Aprovado |
| CT17 | Cancelar exclusão | Livro permanece após cancelar confirmação | 3 | Aprovado |
| CT18 | Confirmar exclusão | Livro removido do acervo | 2 | Aprovado |
| CT19 | Sequência após exclusão | Próximo é LIV004 e nunca reutiliza LIV002 | LIV001 Dom Casmurro  Machado de Assis  Publicado em 1899 ● Disponível Editar Emp | Aprovado |
| CT20 | Atalho Emprestar | Abre empréstimos com livro selecionado | mwei0j8lck6eul | Aprovado |
| CT21 | Empréstimo sem leitor | Bloqueado e mensagem exibida | Informe quem pegou o livro. | Aprovado |
| CT22 | Devolução prevista no passado | Bloqueada | A devolução prevista não pode ser anterior à retirada. A devolução prevista não  | Aprovado |
| CT23 | Devolução antes da retirada | Bloqueada | A devolução prevista não pode ser anterior à retirada. A devolução prevista não  | Aprovado |
| CT24 | REGRESSÃO BUG01: retirada futura | Bloqueada, sem empréstimo ativo | A data da retirada não pode ser futura. | Aprovado |
| CT25 | Empréstimo válido | Aparece 1 emprestado e 2 disponíveis | 1 emprestado | Aprovado |
| CT26 | Livro emprestado removido da seleção | Sem opção do livro ativo | Selecione um livro LIV003 · Livro contemporâneo LIV004 · Depois da exclusão | Aprovado |
| CT27 | Histórico exibe empréstimo | Leitor e livro aparecem | Dom Casmurro  Leitor: Leitora Teste  ● Em aberto Retirada 13/11/2026 Devolução p | Aprovado |
| CT28 | Filtro devolvidos antes de devolver | Histórico devolvido vazio | Nenhum empréstimo registrado nesta categoria. | Aprovado |
| CT29 | Excluir livro emprestado | Bloqueia exclusão e preserva cadastro | Não é possível excluir um livro com empréstimo em aberto. | Aprovado |
| CT30 | REGRESSÃO BUG02: editar livro emprestado | Histórico ativo exibe título atualizado | Dom Casmurro - Revisado | Aprovado |
| CT31 | Filtro empréstimos ativos | Exibe empréstimo aberto | Dom Casmurro - Revisado  Leitor: Leitora Teste  ● Em aberto Retirada 13/11/2026  | Aprovado |
| CT32 | Devolver livro pelo histórico | Empréstimos ativos 0 e devoluções 1 | 1 devolução | Aprovado |
| CT33 | Filtro devolvidos após devolução | Exibe registro com data real | Dom Casmurro - Revisado  Leitor: Leitora Teste  ● Devolvido Retirada 13/11/2026  | Aprovado |
| CT34 | Disponibilidade após devolução | Livro volta a ficar disponível | 3 | Aprovado |
| CT35 | Integração de armazenamento / remontagem | 3 livros, 1 devolução e próximo LIV005 recuperados | 3 livros; LIV005 | Aprovado |
| CT36 | Escape de título HTML malicioso | Título exibido como texto, sem executar tag | LIV005 <img src=x onerror=alert(1)>  Autor Seguro  Publicado em 2020 ● Disponíve | Aprovado |
| CT37 | Ausência de erro JavaScript no fluxo | Nenhum erro JS |  | Aprovado |
| CT38 | Interface no celular | Sem rolagem horizontal | [390, 390] | Aprovado |
| CT39 | Fallback com LocalStorage bloqueado | Cadastro visível com aviso de sessão temporária | Livro LIV001 cadastrado nesta sessão. O armazenamento permanente está bloqueado; | Aprovado |

| CT41 | Limite automático de 3 meses no calendário | Data máxima e orientação exibidas | 2027-02-16 / Prazo máximo: 3 meses após a retirada (até 16/02/2027). | **Aprovado** |
| CT42 | Prazo 3 meses + 1 dia | Empréstimo rejeitado, contador permanece zero | A devolução prevista deve ocorrer em até 3 meses após a retirada. | **Aprovado** |
| CT43 | Prazo exatamente de 3 meses | Empréstimo aceito e registrado | 1 livro emprestado | **Aprovado** |
| CT44 | Prazo menor que 3 meses (7 dias) | Empréstimo aceito | 2 livros emprestados | **Aprovado** |
| CT45 | Fim de mês: 30/11/2026 + 3 meses | Data máxima 28/02/2027, sem transbordar para março | 2027-02-28 | **Aprovado** |
| CT46 | Mês com 31 dias seguido de mês com 30 dias | 31/08/2026 + 3 meses = 30/11/2026 | 2026-11-30 | **Aprovado** |

| CT40 | Recarregar o navegador com F5 usando LocalStorage real | Livros permanecem | Não executado neste ambiente | **Pendente** |

## Amostras de evidência
- `evidencias/01-cadastro-liv001.png`: cadastro e código LIV001.
- `evidencias/03-emprestimo-ativo.png`: empréstimo, leitor e indicadores.
- `evidencias/05-devolucao-registrada.png`: estado após devolução.
- `evidencias/06-persistencia-simulada.png`: estado recuperado em nova montagem com armazenamento simulado.
- `evidencias/07-mobile.png`: visualização no celular.
- `evidencias/09-bug01-antes-data-futura-aceita.png` e `02-bug01-depois-data-futura-bloqueada.png`: BUG01.
- `evidencias/10-bug02-antes-historico-antigo.png` e `04-bug02-depois-historico-atualizado.png`: BUG02.
- `documentacao/resultados_automatizados.json`: registro completo por ID.

## Evidências da nova regra de prazo
- `evidencias/11-prazo-superior-tres-meses-bloqueado.png`: CT42, tentativa de devolver após 3 meses + 1 dia, rejeitada.
- `evidencias/12-prazo-tres-meses-aceito.png`: CT43, empréstimo com prazo exatamente de 3 meses aceito.
- `CT41`, `CT45` e `CT46`: saída da automação registra o `max` do campo de data inclusive nos fins de mês.
