# Refinamento visual do Seus Livros

## Objetivo
Melhorar legibilidade e consistência da aplicação sem modificar regras de negócio nem exigir backend.

## Mudanças
- Paleta atualizada: verde-petróleo, fundo neutro, branco e detalhes de cobre.
- Fonte principal: Public Sans (com Segoe UI como reserva).
- Títulos: Source Serif 4 (com Georgia como reserva), sem tamanhos exagerados.
- Tamanhos de botões, campos e textos aumentados para facilitar a leitura.
- Cartões, formulários e indicadores com espaçamento mais uniforme.
- Layout adaptativo para desktop e celular, sem rolagem horizontal no teste de 390 px.

## O que foi preservado
- Cadastro livre de títulos e autores, ano de 1 a 2026 e código sequencial LIV001+.
- Pesquisa, filtros, edição, exclusão, empréstimos e devoluções.
- Limite máximo de três meses de calendário para devolução.
- Chave e formato de armazenamento no LocalStorage, para manter os livros cadastrados na versão anterior quando acessado pelo mesmo endereço/origem.
- Dois defeitos históricos com as evidências de correção.

## Verificação
A suíte `python tests/testes_interface.py` foi reexecutada na versão redesenhada com fontes remotas desativadas apenas no ambiente automatizado, para evitar dependências de rede. As telas de referência ficam em `evidencias/13-layout-refinado-desktop.png` e `14-layout-refinado-mobile.png`.

**Nota:** a persistência real via F5 no Chrome/Edge com Live Server ainda precisa ser conferida pelo grupo. A suíte automatizada utiliza armazenamento simulado.
