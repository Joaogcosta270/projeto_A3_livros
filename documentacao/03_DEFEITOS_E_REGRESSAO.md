# Registro de defeitos e regressão

Foram utilizados dois problemas **reproduzidos no HTML anterior** (`versoes/versao_antes_dos_retestes.html`). Eles foram corrigidos no HTML final (`index.html`) e retestados. Os screenshots foram gerados pelo mesmo teste automatizado em ambas as versões.

## BUG01 — Retirada futura aceita
- **Severidade:** média (regra temporal e integridade do histórico).
- **Pré-condição:** livro disponível cadastrado.
- **Passos:** abrir Empréstimos, selecionar um livro, informar leitor, colocar data de retirada em hoje + 2 dias e devolução em hoje + 5 dias; clicar em Registrar empréstimo.
- **Esperado:** rejeitar retirada futura; nenhum livro deve passar a emprestado.
- **Obtido na versão anterior:** o sistema aceitava e incrementava o contador de empréstimos.
- **Correção:** validar `loanDate > today()` na função `validateLoan`.
- **Reteste:** CT24 aprovado: empréstimo futuro bloqueado e contador preservado.
- **Evidência antes:** `09-bug01-antes-data-futura-aceita.png`.
- **Evidência depois:** `02-bug01-depois-data-futura-bloqueada.png`.
- **Estado:** corrigido e retestado.

## BUG02 — Histórico ativo exibe título antigo após edição
- **Severidade:** média (inconsistência entre acervo e histórico ativo).
- **Pré-condição:** livro com empréstimo ativo.
- **Passos:** emprestar `Dom Casmurro`; na aba Acervo, editar o título para `Dom Casmurro - Revisado`; abrir Empréstimos.
- **Esperado:** histórico do empréstimo ainda ativo exibe o nome atual do livro.
- **Obtido na versão anterior:** histórico continuava mostrando `Dom Casmurro`.
- **Correção:** sincronizar `bookTitle` dos empréstimos ativos na edição, sem alterar snapshots já devolvidos.
- **Reteste:** CT30 aprovado, histórico ativo atualizado.
- **Evidência antes:** `10-bug02-antes-historico-antigo.png`.
- **Evidência depois:** `04-bug02-depois-historico-atualizado.png`.
- **Estado:** corrigido e retestado.

**Observação metodológica:** os dois defeitos foram demonstrados em versão anterior de fato, e não são exemplos hipotéticos inventados. Reproduzir um bug é diferente de afirmar que a versão final ainda está defeituosa.
