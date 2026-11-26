from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RAW = (ROOT/'index.html').read_text(encoding='utf-8')
HTML = re.sub(r'<link\b[^>]*https://fonts\.(?:googleapis|gstatic)\.com[^>]*>', '', RAW)

def iso(days):
    return (datetime.now(ZoneInfo('America/Sao_Paulo')).date()+timedelta(days=days)).isoformat()

books = [
  {'id':'a','code':'LIV001','title':'Dom Casmurro','author':'Machado de Assis','year':1899},
  {'id':'b','code':'LIV002','title':'Vidas Secas','author':'Graciliano Ramos','year':1938},
  {'id':'c','code':'LIV003','title':'O Cortiço; edição "nova"','author':'Aluísio Azevedo','year':1890},
  {'id':'d','code':'LIV004','title':'Memórias Póstumas','author':'Machado de Assis','year':1881},
  {'id':'e','code':'LIV005','title':'A Hora da Estrela','author':'Clarice Lispector','year':1977},
]
loans = [
  {'id':'l1','bookId':'a','bookTitle':books[0]['title'],'borrower':'Leitor A','loanDate':iso(-60),'dueDate':iso(-2),'returnDate':None},
  {'id':'l2','bookId':'b','bookTitle':books[1]['title'],'borrower':'Leitor B','loanDate':iso(-5),'dueDate':iso(7),'returnDate':None},
  {'id':'l3','bookId':'c','bookTitle':books[2]['title'],'borrower':'Leitor C','loanDate':iso(-5),'dueDate':iso(20),'returnDate':None},
  {'id':'l4','bookId':'d','bookTitle':books[3]['title'],'borrower':'Leitor D','loanDate':iso(-20),'dueDate':iso(-10),'returnDate':iso(-11)},
]

store={'bookflow_layout_v1': json.dumps({'books':books, 'loans':loans, 'nextNumber':6},ensure_ascii=False)}
saved_js=json.dumps(store,ensure_ascii=False).replace('<','\\u003c')
html=HTML.replace('<script>\n  (() => {',f'''<script>
window.__testStorage={saved_js};
Object.defineProperty(window,'localStorage',{{configurable:true,value:{{getItem(k){{return window.__testStorage[k]??null;}},setItem(k,v){{window.__testStorage[k]=String(v);}},removeItem(k){{delete window.__testStorage[k];}}}}}});
</script><script>
  (() => {{''',1)

checks=[]
def check(name,ok):
    print(('OK ' if ok else 'FALHA ')+name)
    checks.append({'cenario':name,'resultado':'Aprovado' if ok else 'Reprovado'})
    if not ok: raise AssertionError(name)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':900},accept_downloads=True,locale='pt-BR',timezone_id='America/Sao_Paulo')
    errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content(html,wait_until='load')
    check('Nova estrutura com cadastro na faixa superior e acervo em linhas',page.locator('#book-form-panel').is_visible() and page.locator('.book-card').count()==5 and page.locator('.book-card').first.bounding_box()['width']>900)
    check('Contador de empréstimos atrasados',page.locator('#stat-overdue').inner_text()=='1')
    check('Contadores de empréstimos, devoluções e exemplares livres',page.locator('#stat-borrowed').inner_text()=='3' and page.locator('#stat-returned').inner_text()=='1' and page.locator('#stat-available').inner_text()=='2')
    page.screenshot(path=str(ROOT/'evidencias'/'15-novo-layout-acervo.png'),full_page=True)
    check('Botões redundantes de CSV e novo empréstimo removidos',page.locator('#export-books').count()==0 and page.locator('#quick-loan').count()==0)
    page.locator('[data-view-btn="loans"]').click()
    check('Menu Empréstimos abre o formulário sem atalho extra',page.locator('#loan-form-panel').is_visible() and page.locator('#loans-view').is_visible())
    check('Contador de empréstimos que vencem até 7 dias',page.locator('#stat-soon').inner_text()=='1')
    check('Classificação automática de empréstimos: atrasado, próximo, em dia e devolvido',all(page.locator(f'.history-item[data-due-state="{v}"]').count()==1 for v in ['overdue','soon','active','returned']))
    page.screenshot(path=str(ROOT/'evidencias'/'16-novo-layout-emprestimos.png'),full_page=True)
    page.locator('#loan-filter').select_option('overdue')
    check('Filtro Atrasados',page.locator('.history-item').count()==1 and page.locator('.history-item').first.get_attribute('data-due-state')=='overdue')
    page.locator('#loan-filter').select_option('soon')
    check('Filtro Vencem em 7 dias inclui o sétimo dia',page.locator('.history-item').count()==1 and page.locator('.history-item').first.get_attribute('data-due-state')=='soon')
    page.locator('#loan-filter').select_option('active')
    check('Filtro Em aberto inclui todos os empréstimos ainda não devolvidos',page.locator('.history-item').count()==3)
    page.locator('#loan-filter').select_option('returned')
    check('Filtro Devolvidos sem falsos atrasos',page.locator('.history-item').count()==1 and page.locator('.history-item').first.get_attribute('data-due-state')=='returned')
    page.locator('#loan-filter').select_option('all')
    page.locator('[data-loan-return="l1"]').click()
    check('Devolução retira livro do contador de atrasos',page.locator('#stat-overdue').inner_text()=='0' and page.locator('#stat-returned').inner_text()=='2')
    page.set_viewport_size({'width':390,'height':820})
    page.screenshot(path=str(ROOT/'evidencias'/'17-novo-layout-mobile.png'),full_page=True)
    check('Interface nova sem rolagem horizontal no celular',page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
    page.locator('[data-view-btn="books"]').click()
    page.locator('#title').fill('=2+2')
    page.locator('#author').fill('Autora Teste')
    page.locator('#year').fill('2026')
    page.locator('#save-book-btn').click()
    check('Cadastro aceita título digitado livremente',page.locator('.book-card').count()==6 and page.get_by_text('=2+2').count()>=1)
    check('Sem erros JavaScript nos novos fluxos',not errors)
    browser.close()

out={'total':len(checks),'aprovados':sum(x['resultado']=='Aprovado' for x in checks),'reprovados':sum(x['resultado']=='Reprovado' for x in checks),'ambiente':'Chromium + Playwright, armazenamento simulado','resultados':checks}
(ROOT/'documentacao'/'resultados_novidades.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',out['aprovados'],'/',out['total'])
