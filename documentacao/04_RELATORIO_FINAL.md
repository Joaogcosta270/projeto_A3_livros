# Relatório final — Seus Livros

**Data da execução:** 16 de novembro de 2026 (versão atualizada)  
**Disciplina:** Garantia da Qualidade de Software  
**Equipe:** Grupo 10 — confirmar integrantes e RAs na planilha do Drive.

## Resultado dos testes

| Indicador | Resultado |
|---|---:|
| Casos funcionais da versão anterior (CT01–CT39, CT41–CT46) | 45 |
| Novos casos de funcionalidade e interface | 15 |
| **Total de casos funcionais da versão atual** | **60** |
| Testes aprovados | 60 |
| Testes reprovados | 0 |
| Taxa de aprovação | 100% |
| Defeitos reproduzidos na versão anterior | 2 |
| Defeitos corrigidos e retestados | 2 |
| Taxa de correção | 100% |
| Teste manual de F5 real | Pendente |

Os 15 casos complementares incluíram indicadores de atraso, vencimento em até sete dias, filtros por status, exportação CSV do acervo e acessibilidade básica no celular. Os cenários anteriores cobriram cadastro, códigos sequenciais, campos obrigatórios, limite de ano, pesquisa, filtros, edição, exclusão com confirmação, empréstimo, datas inválidas, devolução, indicadores, XSS básico, responsividade e armazenamento simulado. A regra adicional RF08 limita a devolução a três meses de calendário após a retirada, com seis testes automatizados novos (CT41–CT46).

### Teste automatizado
Executado em Chromium usando Python + Playwright pelos arquivos `tests/testes_interface.py` e `tests/testes_novidades.py`. Resultados e capturas estão em `documentacao/resultados_automatizados.json`, `documentacao/saida_testes.txt` e `evidencias/`. Das 62 verificações de execução, 60 são casos da versão corrigida, enquanto 2 demonstram falhas reais na versão antiga. As 2 verificações históricas **não contam** como aprovação de testes funcionais da versão final.

### Limitações
A ferramenta de navegador neste ambiente bloqueou acesso HTTP e `file://`, então os testes do fluxo rodaram no Chromium via `set_content` e injeção de LocalStorage simulado. Essa simulação confirma o uso das operações de salvar/ler dados pela aplicação, **mas não demonstra F5 real nem persistência na origem do Chrome do aluno**. A evidência complementar CT40 deverá ser feita localmente com Live Server.

### Conclusão
A aplicação atende ao escopo funcional de Empréstimo de Livros previsto como alternativa no enunciado. As validações e fluxos avaliados passaram após a correção de dois defeitos. O resultado é satisfatório nos cenários automatizados, com uma pendência explícita de verificação de persistência real no navegador do grupo antes da entrega e da apresentação.


**Atualização de 17/11/2026:** o botão de exportação CSV e o atalho superior “Novo empréstimo” foram removidos da interface a pedido do grupo. O fluxo de registro de empréstimo permanece disponível. Os resultados anteriores associados ao CSV são históricos e não representam mais uma funcionalidade da interface atual.
