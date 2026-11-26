# Roteiro curto para a apresentação A3

**1. Introdução (30 segundos):** escolhemos Empréstimo de Livros, uma alternativa autorizada pelo enunciado. Aplicação pequena em HTML/CSS/JavaScript e LocalStorage.

**2. Demonstração (1–2 minutos):** cadastrar um livro e mostrar código automático; pesquisar; alterar o título; emprestar com leitor e data; tentar devolver após 3 meses + 1 dia (rejeitado), escolher data dentro do prazo (aceito); devolver e demonstrar indicadores.

**3. Testes (1 minuto):** explicar caixa preta (validar pelo formulário), caixa branca (ramos de `validateBook` e `validateLoan`) e integração (cadastro + armazenamento + empréstimo + histórico).

**4. Bugs (1 minuto):** BUG01 aceitava retirada futura, BUG02 mantinha título antigo no empréstimo ativo. Mostrar pares de capturas antes/depois e dizer o que mudou no código.

**5. Automação e métricas (1 minuto):** executar `python tests/testes_interface.py`; mostrar 45 casos aprovados na versão final, 2 defeitos corrigidos, 100% de aprovação dos testes automatizados. Explicar que as 2 verificações adicionais reproduzem a versão anterior e não são bugs da versão atual.

**6. Limitações (20 segundos):** CT40 precisa ser repetido no Chrome com F5 real. A automação de persistência que acompanha o pacote usa armazenamento simulado.
