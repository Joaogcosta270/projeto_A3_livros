# Revisão de layout e novas funcionalidades — Seus Livros

## Alteração estrutural de interface

A versão foi reorganizada, e não apenas recolorida:
- Barra superior escura com navegação por Acervo e Empréstimos.
- Painel compacto de indicadores, agora incluindo **Em atraso**.
- Formulário de cadastro em faixa horizontal acima da lista, em lugar da barra lateral.
- Acervo em linhas com título, autor, ano, situação e ações, em vez de cartões grandes.
- Tela de empréstimos com faixa de cadastro, quadro de prazos e histórico organizado por movimentação.
- Comportamento responsivo em telas pequenas.
- Tipografia: Georgia para títulos, DM Sans para textos e IBM Plex Mono para códigos; com alternativas locais.
- Paleta: verde-petróleo escuro, off-white, verde discreto e coral nos botões de ação.

## Novas funcionalidades

**RF09 — Indicadores automáticos de atraso.** Se a data prevista for anterior à data atual e não houver devolução, o empréstimo fica como `Atrasado`. Um exemplar devolvido deixa de ser contado como atrasado.

**RF10 — Devoluções próximas.** Quando faltam de 0 a 7 dias (inclusive) para o vencimento, um empréstimo ainda aberto aparece como `Vence em breve`. Os demais empréstimos ativos ficam como `Em dia`.

**RF11 — Filtros por prazo.** O histórico pode mostrar `Todos`, `Em aberto`, `Vencem em 7 dias`, `Atrasados` e `Devolvidos`.

**RF12 — Recurso descontinuado na versão atual.** O botão de exportação CSV foi retirado da interface por decisão de simplificação. O título pode conter `;` ou aspas sem corromper as colunas. Campos com início de fórmula (`=`, `+`, `-`, `@`) são prefixados com apóstrofo para reduzir o risco de execução como fórmula na planilha.

## Regras preservadas

- Cadastro livre de títulos e autores, com códigos `LIV001`, `LIV002` etc. sem reutilização após exclusão.
- Ano de publicação de 1 a 2026.
- Cadastro, edição, pesquisa, exclusão mediante confirmação, empréstimo e devolução.
- Um livro não pode ser emprestado duas vezes simultaneamente ou excluído com empréstimo em aberto.
- Data de retirada não pode ser futura; devolução prevista deve respeitar até três meses de calendário.
- Dados continuam sob a chave `bookflow_layout_v1` para manter os registros do mesmo navegador/origem da versão anterior.

## Verificações extras realizadas

Em `tests/testes_novidades.py`, os **15 cenários novos** passaram em Chromium com Playwright e armazenamento simulado. Foram testados os contadores, a classificação de quatro tipos de empréstimo, os filtros, o caso exato de 7 dias, a exportação CSV com caracteres especiais, a devolução que remove o status de atraso, a versão mobile e a ausência de erros JavaScript.

Os **45 casos preexistentes da versão final** também passaram novamente. Além disso, a suíte mantém **2 verificações históricas** que reproduzem os defeitos anteriores, mas elas não são contabilizadas como casos funcionais da versão atual.

**Totais da versão atual:** 60 casos aprovados, 0 reprovados, mais 2 reproduções históricas. O teste manual de LocalStorage com F5 no Chrome/Edge real permanece pendente.

Evidências novas: `evidencias/15-novo-layout-acervo.png`, `16-novo-layout-emprestimos.png` e `17-novo-layout-mobile.png`. Resultados: `documentacao/resultados_novidades.json`.


> **Atualização de interface:** na versão atual, o botão de exportar CSV e o atalho superior de novo empréstimo foram removidos. O cadastro de empréstimos continua no formulário específico da aba Empréstimos. As evidências anteriores retratam versões anteriores do projeto.
