# Regra de prazo de devolução (RF08)

## Objetivo
Permitir empréstimos com data prevista de devolução de **até 3 meses de calendário** após a retirada. Um prazo menor é permitido. O limite é inclusivo.

## Comportamento
1. O campo **Retirada** começa preenchido com a data de hoje, no fuso local do navegador.
2. Ao escolher a data de retirada, o campo **Devolução prevista** recebe um limite máximo (`max`) calculado automaticamente.
3. O campo exibe uma frase informando a data máxima de devolução.
4. O formulário valida novamente em JavaScript ao salvar, impedindo que o usuário ultrapasse o prazo mesmo se contornar o controle do navegador.
5. Datas anteriores à retirada, anteriores ao dia atual ou retiradas futuras são proibidas pelas regras já existentes.

## Exemplos
| Retirada | Último dia aceito |
|---|---|
| 16/11/2026 | 16/02/2027 |
| 30/11/2026 | 28/02/2027 |
| 31/08/2026 | 30/11/2026 |

## Testes automatizados
- CT41: data máxima aparece no calendário e no texto.
- CT42: ultrapassar 3 meses em 1 dia bloqueia o empréstimo.
- CT43: prazo de exatamente 3 meses é aceito.
- CT44: prazo de 7 dias é aceito.
- CT45: 30/11/2026 + 3 meses = 28/02/2027.
- CT46: 31/08/2026 + 3 meses = 30/11/2026.

Os casos anteriores também foram reexecutados como regressão. CT40 (F5 real com LocalStorage no Chrome ou Edge via Live Server) continua pendente de registro pelo grupo.
