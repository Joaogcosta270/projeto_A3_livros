# Plano de Testes — Seus Livros

**Disciplina:** Garantia da Qualidade de Software | **Projeto:** Sistema de Empréstimo de Livros | **Grupo:** 10 (conferir nomes na planilha GrupoA3).

## Objetivo
Avaliar se o sistema permite cadastrar, consultar, editar e excluir livros; registrar empréstimos e devoluções; mostrar a disponibilidade; validar entradas; e preservar dados quando o armazenamento do navegador está disponível.

## Escopo e requisitos testáveis
- RF01: Cadastrar qualquer título e autor, com ano entre 1 e 2026.
- RF02: Gerar códigos únicos sequenciais `LIV001`, `LIV002`... sem reaproveitamento após exclusão.
- RF03: Listar e pesquisar livros por título, autor ou código; filtrar por disponibilidade.
- RF04: Editar livro e excluir mediante confirmação, exceto se houver empréstimo ativo.
- RF05: Registrar empréstimo apenas se o exemplar estiver disponível; exigir leitor e datas válidas.
- RF06: Registrar devolução e atualizar disponibilidade, filtros e indicadores.
- RF07: Manter histórico; ao editar título de exemplar emprestado, atualizar a identificação no empréstimo ativo.
- RF08: Permitir prazo de devolução de até 3 meses de calendário após a retirada (inclusive), bloqueando qualquer prazo acima. Mostrar limite no formulário e tratar meses com 28, 30 ou 31 dias.
- RNF01: Usar HTML/CSS/JavaScript, interface responsiva e mensagens claras.
- RNF02: Guardar dados em LocalStorage quando habilitado e informar quando há armazenamento temporário.

## Ambiente e massa de teste
- **Código:** `index.html` em navegador Chromium.
- **Ferramenta de automação:** Python + Playwright (execução em navegador real com injeção de LocalStorage simulado, porque navegação local foi bloqueada neste ambiente).
- **Dados fictícios:** Dom Casmurro/Machado de Assis/1899, A Arte da Guerra/Sun Tzu/1, Livro contemporâneo/Autora Teste/2026, leitor fictício.
- **Datas:** geradas com fuso America/Sao_Paulo em relação ao dia da execução. CT45 e CT46 usam datas fixas para testar fim de mês e a regra dos 3 meses.

## Estratégia
- **Caixa preta:** observar a interface e os resultados após entradas válidas e inválidas (CT02 a CT13, CT20 a CT29).
- **Caixa branca:** exercitar ramos de `validateBook` (campos vazios, regex do ano, intervalo, aceite) e `validateLoan` (leitor vazio, data no passado, devolução anterior à retirada, retirada futura, disponibilidade, prazo máximo de devolução).
- **Funcional/integrado:** cadastro -> listagem -> seleção -> empréstimo -> histórico -> devolução (CT07, CT20, CT25, CT27, CT32, CT34).
- **Regressão:** CT24 e CT30 após corrigir BUG01 e BUG02; CT41–CT46 confirmam a nova regra de três meses sem afetar os empréstimos de prazo curto.
- **Automação:** executar `python tests/testes_interface.py` e registrar saída e capturas.
- **Persistência:** CT35 testa serialização, armazenamento simulado e reconstrução da página. O recarregamento real com F5, usando Chrome/Edge via Live Server, ainda requer execução manual.
- **Prazo máximo:** CT41–CT46 verificam limite automático na interface, rejeição de 3 meses + 1 dia, aceitação de 3 meses exatos, aceitação de prazo menor e datas de fim de mês.

## Critérios
- **Entrada:** projeto abre, JavaScript é inicializado e casos de teste estão definidos.
- **Saída:** cenários críticos executados, defeitos reproduzidos e corrigidos documentados, evidências anexas, métricas calculadas e limitações apontadas.
- **Limitação importante:** teste de compatibilidade do LocalStorage com o navegador real, após F5, está pendente de evidência local. Isso não é declarado como aprovado.

## Teste manual pendente (CT40)
1. Abra `index.html` no Chrome/Edge via Live Server no VS Code.
2. Cadastre `Dom Casmurro`, `Machado de Assis`, `1899`; confirme o código do livro.
3. Aperte F5. Confirme que o livro e a sequência dos códigos continuam presentes.
4. Capture as duas telas e preencha o resultado de CT40 antes da entrega.
