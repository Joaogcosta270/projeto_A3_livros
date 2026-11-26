from pathlib import Path
from datetime import datetime, timedelta, date
from calendar import monthrange
from zoneinfo import ZoneInfo
import argparse
import json
import os
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = re.sub(r'<link\b[^>]*https://fonts\.(?:googleapis|gstatic)\.com[^>]*>', '', (ROOT / 'index.html').read_text(encoding='utf-8'))
OLD_HTML = (ROOT / 'versoes' / 'versao_antes_dos_retestes.html').read_text(encoding='utf-8')
EVIDENCE = ROOT / 'evidencias'
EVIDENCE.mkdir(exist_ok=True)
REPORT_PATH = ROOT / 'documentacao' / 'resultados_automatizados.json'
BROWSER_EXEC = os.environ.get('BROWSER_EXECUTABLE')


def with_storage(html, saved=None):
    saved_json = json.dumps(saved or {}, ensure_ascii=False).replace('<', '\\u003c')
    injection = f'''<script>
    window.__testStorage = {saved_json};
    Object.defineProperty(window, 'localStorage', {{configurable:true,value:{{
      getItem(key){{return Object.prototype.hasOwnProperty.call(window.__testStorage,key)?window.__testStorage[key]:null}},
      setItem(key,value){{window.__testStorage[key]=String(value)}},
      removeItem(key){{delete window.__testStorage[key]}}
    }}}});
    </script>'''
    return html.replace('<script>\n  (() => {', injection+'\n<script>\n  (() => {', 1)


def book(page, title, author, year):
    page.locator('#title').fill(title)
    page.locator('#author').fill(author)
    page.locator('#year').fill(str(year))
    page.locator('#save-book-btn').click()


def iso(days=0):
    return (datetime.now(ZoneInfo('America/Sao_Paulo')).date()+timedelta(days=days)).isoformat()

def max_due(value):
    start=date.fromisoformat(value)
    year=start.year+(start.month+2)//12
    month=(start.month+2)%12+1
    return date(year,month,min(start.day,monthrange(year,month)[1])).isoformat()



class Suite:
    def __init__(self):
        self.results=[]
        self.current=''
    def check(self, case, scenario, expected, ok, observed, screenshot=None):
        result = {'id':case,'cenario':scenario,'esperado':expected,'obtido':str(observed), 'resultado':'Aprovado' if ok else 'Reprovado','evidencia':screenshot or ''}
        self.results.append(result)
        print(f"{case} [{'OK' if ok else 'FALHOU'}] {scenario} | {str(observed)[:110]}")
        if not ok:
            raise AssertionError(f'{case} reprovado: {scenario} -> {observed}')
    def save(self):
        REPORT_PATH.parent.mkdir(exist_ok=True)
        summary={'total':len(self.results),'aprovados':sum(x['resultado']=='Aprovado' for x in self.results),'reprovados':sum(x['resultado']=='Reprovado' for x in self.results),'ambiente':'Chromium, Playwright, HTML real renderizado com armazenamento simulado; rede/localhost bloqueados no ambiente de execução','resultados':self.results}
        REPORT_PATH.write_text(json.dumps(summary,ensure_ascii=False,indent=2), encoding='utf-8')
        (ROOT/'documentacao'/'saida_testes.txt').write_text('\n'.join(f"{x['id']}: {x['resultado']} — {x['cenario']}" for x in self.results)+f"\nTotal: {summary['total']} / Aprovados: {summary['aprovados']} / Reprovados: {summary['reprovados']}\n",encoding='utf-8')
        return summary


def run():
    s=Suite()
    args={ 'headless':True,'args':['--no-sandbox'] }
    if BROWSER_EXEC: args['executable_path']=BROWSER_EXEC
    elif Path('/usr/bin/chromium').exists(): args['executable_path']='/usr/bin/chromium'
    with sync_playwright() as p:
      browser=p.chromium.launch(**args)
      page=browser.new_page(viewport={'width':1360,'height':940},device_scale_factor=1,locale='pt-BR',timezone_id='America/Sao_Paulo')
      js_errors=[]
      page.on('pageerror', lambda e: js_errors.append(str(e)))
      page.set_content(with_storage(HTML),wait_until='load')
      s.check('CT01','Inicialização do sistema','Contadores iniciam em zero e JavaScript ativo',page.locator('#stat-books').inner_text()=='0' and 'Cadastro ativo' in page.locator('#runtime-status').inner_text(),page.locator('#runtime-status').inner_text())
      page.locator('#save-book-btn').click()
      s.check('CT02','Cadastro sem título/autor/ano','Bloqueio com mensagem',page.locator('#stat-books').inner_text()=='0' and 'Informe o título' in page.locator('#book-feedback').inner_text(),page.locator('#book-feedback').inner_text())
      page.locator('#title').fill('Um livro sem autor')
      page.locator('#year').fill('1990')
      page.locator('#save-book-btn').click()
      s.check('CT03','Cadastro sem autor','Mensagem obrigatória', 'Informe o autor' in page.locator('#book-feedback').inner_text(),page.locator('#book-feedback').inner_text())
      page.locator('#author').fill('Autor Teste')
      page.locator('#year').fill('0')
      page.locator('#save-book-btn').click()
      s.check('CT04','Ano zero','Rejeitado','entre 1 e 2026' in page.locator('#book-feedback').inner_text(),page.locator('#book-feedback').inner_text())
      page.locator('#year').fill('2027')
      page.locator('#save-book-btn').click()
      s.check('CT05','Ano acima de 2026','Rejeitado','entre 1 e 2026' in page.locator('#book-feedback').inner_text(),page.locator('#book-feedback').inner_text())
      page.locator('#year').fill('2e3')
      page.locator('#save-book-btn').click()
      s.check('CT06','Ano em notação exponencial 2e3','Bloqueado como formato inválido', 'sem letras ou símbolos' in page.locator('#book-feedback').inner_text(),page.locator('#book-feedback').inner_text())
      book(page,'Dom Casmurro','Machado de Assis','1899')
      page.screenshot(path=str(EVIDENCE/'01-cadastro-liv001.png'),full_page=True)
      s.check('CT07','Cadastro de livro válido','Aparece como LIV001 e contador 1',page.locator('#stat-books').inner_text()=='1' and 'LIV001' in page.locator('#books-grid').inner_text(),page.locator('#books-grid').inner_text()[:110],'01-cadastro-liv001.png')
      s.check('CT08','Prévia do código','Próximo código LIV002',page.locator('#code-preview').inner_text()=='LIV002',page.locator('#code-preview').inner_text())
      book(page,'A Arte da Guerra','Sun Tzu','1')
      s.check('CT09','Livro com ano mínimo 1','Aceito com LIV002',page.locator('#stat-books').inner_text()=='2' and 'LIV002' in page.locator('#books-grid').inner_text(),page.locator('#books-grid').inner_text()[:160])
      book(page,'Livro contemporâneo','Autora Teste','2026')
      s.check('CT10','Livro de 2026','Aceito com LIV003',page.locator('#stat-books').inner_text()=='3' and 'LIV003' in page.locator('#books-grid').inner_text(),page.locator('#books-grid').inner_text()[:160])
      page.locator('#search').fill('Dom Casmurro')
      s.check('CT11','Pesquisar por título','Só o título correspondente aparece',page.locator('.book-card').count()==1 and 'Dom Casmurro' in page.locator('#books-grid').inner_text(),page.locator('#books-grid').inner_text()[:100])
      page.locator('#search').fill('Sun Tzu')
      s.check('CT12','Pesquisar por autor','Encontra A Arte da Guerra',page.locator('.book-card').count()==1 and 'A Arte da Guerra' in page.locator('#books-grid').inner_text(),page.locator('#books-grid').inner_text()[:100])
      page.locator('#search').fill('')
      page.locator('#book-filter').select_option('borrowed')
      s.check('CT13','Filtro emprestados antes do empréstimo','Nenhum cartão visível',page.locator('.book-card').count()==0,page.locator('#books-grid').inner_text()[:70])
      page.locator('#book-filter').select_option('all')
      page.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-action="edit"]').click()
      s.check('CT14','Editar livro','Formulário preenchido',page.locator('#title').input_value()=='Dom Casmurro' and page.locator('#editing-id').input_value()!='',page.locator('#title').input_value())
      page.locator('#cancel-edit-btn').click()
      s.check('CT15','Cancelar edição','Retorna a modo cadastro, sem alterar livro',page.locator('#editing-id').input_value()=='' and 'Dom Casmurro' in page.locator('#books-grid').inner_text(),page.locator('#book-form-title').inner_text())
      page.locator('.book-card').filter(has_text='A Arte da Guerra').locator('[data-action="edit"]').click()
      page.locator('#title').fill('A Arte da Guerra - Revisto')
      page.locator('#save-book-btn').click()
      s.check('CT16','Salvar edição','Título novo com mesmo LIV002 e 3 livros', 'A Arte da Guerra - Revisto' in page.locator('#books-grid').inner_text() and page.locator('#stat-books').inner_text()=='3' and page.locator('#code-preview').inner_text()=='LIV004',page.locator('#books-grid').inner_text()[:200])
      page.once('dialog', lambda d:d.dismiss())
      page.locator('.book-card').filter(has_text='A Arte da Guerra - Revisto').locator('[data-action="delete"]').click()
      s.check('CT17','Cancelar exclusão','Livro permanece após cancelar confirmação',page.locator('#stat-books').inner_text()=='3' and 'A Arte da Guerra - Revisto' in page.locator('#books-grid').inner_text(),page.locator('#stat-books').inner_text())
      page.once('dialog', lambda d:d.accept())
      page.locator('.book-card').filter(has_text='A Arte da Guerra - Revisto').locator('[data-action="delete"]').click()
      s.check('CT18','Confirmar exclusão','Livro removido do acervo',page.locator('#stat-books').inner_text()=='2' and 'A Arte da Guerra - Revisto' not in page.locator('#books-grid').inner_text(),page.locator('#stat-books').inner_text())
      book(page,'Depois da exclusão','Autor Livre','1900')
      s.check('CT19','Sequência após exclusão','Próximo é LIV004 e nunca reutiliza LIV002','LIV004' in page.locator('#books-grid').inner_text() and page.locator('#code-preview').inner_text()=='LIV005',page.locator('#books-grid').inner_text()[:250])
      page.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-go-loan]').click()
      s.check('CT20','Atalho Emprestar','Abre empréstimos com livro selecionado',page.locator('#loan-form-panel').is_visible() and page.locator('#loan-book').input_value()!='',page.locator('#loan-book').input_value())
      page.locator('#loan-date').fill(iso(0))
      page.locator('#due-date').fill(iso(7))
      page.get_by_role('button',name='Registrar empréstimo').click()
      s.check('CT21','Empréstimo sem leitor','Bloqueado e mensagem exibida','Informe quem pegou' in page.locator('#notice').inner_text(),page.locator('#notice').inner_text())
      page.locator('#borrower').fill('Leitora Teste')
      page.locator('#due-date').fill(iso(-1))
      page.get_by_role('button',name='Registrar empréstimo').click()
      s.check('CT22','Devolução prevista no passado','Bloqueada','passada' in page.locator('#notice').inner_text(),page.locator('#notice').inner_text())
      page.locator('#loan-date').fill(iso(0))
      page.locator('#due-date').fill(iso(-1))
      page.get_by_role('button',name='Registrar empréstimo').click()
      s.check('CT23','Devolução antes da retirada','Bloqueada','anterior' in page.locator('#notice').inner_text(),page.locator('#notice').inner_text())
      page.locator('#loan-date').fill(iso(2))
      page.locator('#due-date').fill(iso(5))
      page.get_by_role('button',name='Registrar empréstimo').click()
      page.screenshot(path=str(EVIDENCE/'02-bug01-depois-data-futura-bloqueada.png'),full_page=True)
      s.check('CT24','REGRESSÃO BUG01: retirada futura','Bloqueada, sem empréstimo ativo',page.locator('#stat-borrowed').inner_text()=='0' and 'retirada não pode ser futura' in page.locator('#notice').inner_text(),page.locator('#notice').inner_text(),'02-bug01-depois-data-futura-bloqueada.png')
      page.locator('#loan-date').fill(iso(0))
      page.locator('#due-date').fill(iso(7))
      page.get_by_role('button',name='Registrar empréstimo').click()
      page.screenshot(path=str(EVIDENCE/'03-emprestimo-ativo.png'),full_page=True)
      s.check('CT25','Empréstimo válido','Aparece 1 emprestado e 2 disponíveis',page.locator('#stat-borrowed').inner_text()=='1' and page.locator('#stat-available').inner_text()=='2',page.locator('#stat-borrowed').inner_text()+' emprestado','03-emprestimo-ativo.png')
      s.check('CT26','Livro emprestado removido da seleção','Sem opção do livro ativo','Dom Casmurro' not in page.locator('#loan-book').inner_text(),page.locator('#loan-book').inner_text())
      s.check('CT27','Histórico exibe empréstimo','Leitor e livro aparecem',page.locator('.history-item').count()==1 and 'Leitora Teste' in page.locator('#loans-list').inner_text(),page.locator('#loans-list').inner_text()[:140])
      page.locator('#loan-filter').select_option('returned')
      s.check('CT28','Filtro devolvidos antes de devolver','Histórico devolvido vazio',page.locator('.history-item').count()==0,page.locator('#loans-list').inner_text()[:100])
      page.locator('#loan-filter').select_option('all')
      page.get_by_role('button',name='Acervo').click()
      page.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-action="delete"]').click()
      s.check('CT29','Excluir livro emprestado','Bloqueia exclusão e preserva cadastro',page.locator('#stat-books').inner_text()=='3' and 'Não é possível excluir' in page.locator('#notice').inner_text(),page.locator('#notice').inner_text())
      page.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-action="edit"]').click()
      page.locator('#title').fill('Dom Casmurro - Revisado')
      page.locator('#save-book-btn').click()
      page.get_by_role('button',name='Empréstimos').click()
      page.screenshot(path=str(EVIDENCE/'04-bug02-depois-historico-atualizado.png'),full_page=True)
      s.check('CT30','REGRESSÃO BUG02: editar livro emprestado','Histórico ativo exibe título atualizado','Dom Casmurro - Revisado' in page.locator('.history-item h4').first.inner_text(),page.locator('.history-item h4').first.inner_text(),'04-bug02-depois-historico-atualizado.png')
      page.locator('#loan-filter').select_option('active')
      s.check('CT31','Filtro empréstimos ativos','Exibe empréstimo aberto',page.locator('.history-item').count()==1,page.locator('#loans-list').inner_text()[:90])
      page.locator('[data-loan-return]').click()
      page.screenshot(path=str(EVIDENCE/'05-devolucao-registrada.png'),full_page=True)
      s.check('CT32','Devolver livro pelo histórico','Empréstimos ativos 0 e devoluções 1',page.locator('#stat-borrowed').inner_text()=='0' and page.locator('#stat-returned').inner_text()=='1',page.locator('#stat-returned').inner_text()+' devolução','05-devolucao-registrada.png')
      page.locator('#loan-filter').select_option('returned')
      s.check('CT33','Filtro devolvidos após devolução','Exibe registro com data real',page.locator('.history-item').count()==1 and iso(0).split('-')[0] in page.locator('#loans-list').inner_text(),page.locator('#loans-list').inner_text()[:180])
      page.get_by_role('button',name='Acervo').click()
      s.check('CT34','Disponibilidade após devolução','Livro volta a ficar disponível',page.locator('#stat-available').inner_text()=='3' and page.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-go-loan]').count()==1,page.locator('#stat-available').inner_text())
      store=page.evaluate('window.__testStorage')
      page.set_content(with_storage(HTML,store),wait_until='load')
      page.screenshot(path=str(EVIDENCE/'06-persistencia-simulada.png'),full_page=True)
      s.check('CT35','Integração de armazenamento / remontagem','3 livros, 1 devolução e próximo LIV005 recuperados',page.locator('#stat-books').inner_text()=='3' and page.locator('#stat-returned').inner_text()=='1' and page.locator('#code-preview').inner_text()=='LIV005',page.locator('#stat-books').inner_text()+' livros; '+page.locator('#code-preview').inner_text(),'06-persistencia-simulada.png')
      book(page,'<img src=x onerror=alert(1)>','Autor Seguro','2020')
      s.check('CT36','Escape de título HTML malicioso','Título exibido como texto, sem executar tag',page.locator('#books-grid img').count()==0 and page.locator('#stat-books').inner_text()=='4',page.locator('.book-card').filter(has_text='Autor Seguro').inner_text()[:100])
      s.check('CT37','Ausência de erro JavaScript no fluxo','Nenhum erro JS',not js_errors, '; '.join(js_errors))
      page.set_viewport_size({'width':390,'height':820})
      page.screenshot(path=str(EVIDENCE/'07-mobile.png'),full_page=True)
      s.check('CT38','Interface no celular','Sem rolagem horizontal',page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'),str(page.evaluate('[document.documentElement.scrollWidth,window.innerWidth]')),'07-mobile.png')
      # Modo temporário: localStorage indisponível, também deve permitir registro na sessão.
      other=browser.new_page(viewport={'width':1200,'height':900})
      other.set_content(HTML,wait_until='load')
      book(other,'Vidas Secas','Graciliano Ramos','1938')
      other.screenshot(path=str(EVIDENCE/'08-storage-bloqueado.png'),full_page=True)
      s.check('CT39','Fallback com LocalStorage bloqueado','Cadastro visível com aviso de sessão temporária',other.locator('#stat-books').inner_text()=='1' and 'sessão' in other.locator('#book-feedback').inner_text().lower(),other.locator('#book-feedback').inner_text()[:170],'08-storage-bloqueado.png')
      other.close()
      # Casos adicionais: prazo máximo de três meses corridos por calendário.
      prazo=browser.new_page(viewport={'width':1360,'height':940},device_scale_factor=1,locale='pt-BR',timezone_id='America/Sao_Paulo')
      prazo.set_content(with_storage(HTML),wait_until='load')
      book(prazo,'Memórias Póstumas','Machado de Assis','1881')
      prazo.locator('.book-card').filter(has_text='Memórias Póstumas').locator('[data-go-loan]').click()
      s.check('CT41','Limite automático de 3 meses no calendário','Data máxima e orientação exibidas',prazo.locator('#due-date').get_attribute('max')==max_due(iso()) and '3 meses' in prazo.locator('#loan-limit-hint').inner_text(),prazo.locator('#due-date').get_attribute('max')+' / '+prazo.locator('#loan-limit-hint').inner_text())
      prazo.locator('#borrower').fill('Leitor Prazo')
      prazo.locator('#loan-date').fill(iso())
      prazo.locator('#due-date').fill((date.fromisoformat(max_due(iso()))+timedelta(days=1)).isoformat())
      prazo.get_by_role('button',name='Registrar empréstimo').click()
      prazo.screenshot(path=str(EVIDENCE/'11-prazo-superior-tres-meses-bloqueado.png'),full_page=True)
      s.check('CT42','Prazo 3 meses + 1 dia','Empréstimo rejeitado, contador permanece zero','até 3 meses' in prazo.locator('#notice').inner_text() and prazo.locator('#stat-borrowed').inner_text()=='0',prazo.locator('#notice').inner_text(),'11-prazo-superior-tres-meses-bloqueado.png')
      prazo.locator('#due-date').fill(max_due(iso()))
      prazo.get_by_role('button',name='Registrar empréstimo').click()
      prazo.screenshot(path=str(EVIDENCE/'12-prazo-tres-meses-aceito.png'),full_page=True)
      s.check('CT43','Prazo exatamente de 3 meses','Empréstimo aceito e registrado',prazo.locator('#stat-borrowed').inner_text()=='1' and prazo.locator('.history-item').count()==1,prazo.locator('#stat-borrowed').inner_text()+' livro emprestado','12-prazo-tres-meses-aceito.png')
      prazo.get_by_role('button',name='Acervo').click()
      book(prazo,'Vidas Secas','Graciliano Ramos','1938')
      prazo.locator('.book-card').filter(has_text='Vidas Secas').locator('[data-go-loan]').click()
      prazo.locator('#borrower').fill('Leitor Prazo Curto')
      prazo.locator('#loan-date').fill(iso())
      prazo.locator('#due-date').fill(iso(7))
      prazo.get_by_role('button',name='Registrar empréstimo').click()
      s.check('CT44','Prazo menor que 3 meses (7 dias)','Empréstimo aceito',prazo.locator('#stat-borrowed').inner_text()=='2' and prazo.locator('.history-item').count()==2,prazo.locator('#stat-borrowed').inner_text()+' livros emprestados')
      prazo.locator('#loan-date').fill('2026-11-30')
      s.check('CT45','Fim de mês: 30/11/2026 + 3 meses','Data máxima 28/02/2027, sem transbordar para março',prazo.locator('#due-date').get_attribute('max')=='2027-02-28',prazo.locator('#due-date').get_attribute('max'))
      prazo.locator('#loan-date').fill('2026-08-31')
      s.check('CT46','Mês com 31 dias seguido de mês com 30 dias','31/08/2026 + 3 meses = 30/11/2026',prazo.locator('#due-date').get_attribute('max')=='2026-11-30',prazo.locator('#due-date').get_attribute('max'))
      prazo.close()
      # Evidências ANTES: falhas reproduzidas na versão imediatamente anterior.
      old=browser.new_page(viewport={'width':1360,'height':940})
      old.set_content(with_storage(OLD_HTML),wait_until='load')
      book(old,'Dom Casmurro','Machado de Assis','1899')
      old.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-go-loan]').click()
      old.locator('#borrower').fill('Leitora Teste')
      old.locator('#loan-date').fill(iso(2))
      old.locator('#due-date').fill(iso(5))
      old.get_by_role('button',name='Registrar empréstimo').click()
      old.screenshot(path=str(EVIDENCE/'09-bug01-antes-data-futura-aceita.png'),full_page=True)
      old_future_accepted=old.locator('#stat-borrowed').inner_text()=='1'
      s.check('BUG01-ANTES','Reproduzir defeito de retirada futura na versão anterior','Defeito demonstrado: empréstimo futuro foi aceito',old_future_accepted,old.locator('#notice').inner_text(),'09-bug01-antes-data-futura-aceita.png')
      old.get_by_role('button',name='Acervo').click()
      old.locator('.book-card').filter(has_text='Dom Casmurro').locator('[data-action="edit"]').click()
      old.locator('#title').fill('Dom Casmurro - Revisado')
      old.locator('#save-book-btn').click()
      old.get_by_role('button',name='Empréstimos').click()
      old.screenshot(path=str(EVIDENCE/'10-bug02-antes-historico-antigo.png'),full_page=True)
      old_stale=old.locator('.history-item h4').inner_text()=='Dom Casmurro'
      s.check('BUG02-ANTES','Reproduzir defeito de título desatualizado no histórico ativo','Defeito demonstrado: título antigo permanece no histórico',old_stale,old.locator('.history-item h4').inner_text(),'10-bug02-antes-historico-antigo.png')
      old.close()
      browser.close()
    return s.save()


if __name__=='__main__':
    try:
        results=run()
        print(f"\nRESULTADO FINAL: {results['aprovados']}/{results['total']} verificações aprovadas; {results['reprovados']} reprovadas.")
    except Exception as e:
        print(f"ERRO NA EXECUÇÃO: {type(e).__name__}: {e}")
        raise
