# Conferência automática de Notas Fiscais — ING, Angiocardis, Encore e CCRI

A planilha lê os e-mails da caixa **repassesmedicos** e marca, em cada linha do controle,
se a nota fiscal da competência chegou:

| Status | Significado |
|---|---|
| **RECEBIDA** (verde) | Achei e-mail com nota desse médico/empresa, no hospital e serviço certos |
| **VERIFICAR** (amarelo) | Achei e-mail do médico, mas falta nota de algum serviço (ex.: mandou plantão e não mandou repasse) ou o e-mail não deixou claro o tipo |
| **PENDENTE** (vermelho) | Não achei nenhum e-mail desse médico/empresa na competência |

Também cria:
- aba **Resumo**: totais por hospital e a lista de quem está PENDENTE ou VERIFICAR;
- aba **E-mails**: todos os e-mails lidos e a linha a que cada um foi vinculado. Os marcados **NÃO ENCONTRADO NA PLANILHA** são notas de quem não está no controle (ou com nome muito diferente).

> Não precisa de TI nem de encaminhamento: o script roda dentro da própria conta repassesmedicos,
> e os dados não saem dela.

---

## 1. Instalar (só uma vez, ~10 minutos)

Faça tudo **logada na conta repassesmedicos@neurologico.com.br** no navegador.

1. Abra **sheets.new**. Isso cria uma planilha em branco. Dê o nome **Conferência de Notas**.
2. Menu **Extensões → Apps Script**.
3. Apague o que estiver escrito e **cole todo o conteúdo do arquivo `Codigo.gs`**.
4. Clique no ícone de **disquete (Salvar)**. Se pedir nome do projeto, coloque *Conferência de Notas*.
5. Volte à aba da planilha e **recarregue a página (F5)**. Vai aparecer o menu **Conferência de Notas** no topo.
6. Clique em **Conferência de Notas → Configurar (primeira vez)**.
   - O Google vai pedir autorização: **Continuar** → escolha a conta repassesmedicos.
   - Se aparecer *"O Google não verificou este app"*, clique em **Avançado → Acessar Conferência de Notas (não seguro)** → **Permitir**.
     Esse aviso é normal: o "app" é o código que você mesma colou. Ele pede para **ler o Gmail** (para achar as notas) e **editar a planilha** (para marcar o resultado).

> Se aparecer uma mensagem dizendo que o administrador bloqueou o Apps Script, a empresa
> desativou esse recurso. Nesse caso me avise, porque há outro caminho.

## 2. Conferir uma competência

1. Na aba **Config**, confira a **Competência** (ex.: `11/2026`).
2. Importe as planilhas do mês, **uma de cada vez**: **Arquivo → Importar → Upload →** escolha o **ING 11-2026.xlsx** →
   em *Local de importação* escolha **"Inserir nova(s) página(s)"** → **Importar dados**.
   Repita com o **ENCORE 11-2026.xlsx**.
   Aparecem as abas **ING**, **ANGIOCARDIS**, **ENCORE**, **CCRI VLB** e **CCRI CERES**. A aba *legenda* é ignorada.
   Se quiser conferir só um hospital, importe só a planilha dele.
3. **Conferência de Notas → ▶ Conferir agora**.

Em cada aba de controle surgem duas colunas no fim: **STATUS NOTA (E-MAIL)** e **E-MAIL ENCONTRADO**
(data e assunto do e-mail que comprovou a nota).

## 3. Deixar automático

**Conferência de Notas → Ativar conferência automática diária**.
Todo dia, por volta das 7h, ele relê os e-mails e atualiza os status, mesmo com a planilha fechada.
Basta abrir e olhar a aba **Resumo**.

## 4. Virada do mês

1. **Conferência de Notas → Preparar novo mês**. Apaga as abas do mês anterior e mantém Config, Resumo e E-mails.
2. Atualize a **Competência** na aba Config (ex.: `12/2026`).
3. Importe as planilhas do novo mês (passo 2.2) e clique em **Conferir agora**.

---

## Como ele decide se a nota é de uma linha

Para cada e-mail recebido na competência, ele compara com cada linha do controle:

1. **Nome do médico** no assunto, no remetente ou no nome do anexo: precisa do primeiro nome e de mais um sobrenome. Também vale se o nome completo aparecer no corpo do e-mail.
2. **CNPJ** da empresa em qualquer parte do e-mail.
3. **Nome da empresa** no assunto, no remetente ou no anexo.

Quando dois médicos dividem a mesma empresa (ex.: Cleber e Ezio na LIFE), o nome do médico tem prioridade.

- **Hospital:** cada aba é um hospital (ING, ANGIOCARDIS, ENCORE, CCRI VILA BRASÍLIA, CCRI CERES). Se o assunto ou o anexo cita o hospital ("ING", "ANGIOCARDIS", "ENCORE", "CCRI", "CERES"...), ele só vincula às linhas daquele hospital. Se não cita, procura em todos.
- **Tipo de serviço:** se o assunto ou o anexo diz *plantão*, *repasse/HM* ou *sobreaviso/coordenação/demais*, ele vincula à linha do mesmo tipo. Se o e-mail não diz o tipo e o médico tem várias linhas, ele confere se a quantidade de e-mails cobre as linhas. Se não cobrir, marca **VERIFICAR**.

## Dicas para acertar mais

- O ideal é que os médicos mandem o assunto no padrão
  **`NF - COMPETÊNCIA 11/2026 - HOSPITAL - NOME DO MÉDICO - PLANTÃO`** (ou REPASSE / DEMAIS SERVIÇOS). Ex.: `NF - COMPETÊNCIA 11/2026 - ENCORE - BRENDA RODOVALHO - DEMAIS SERVIÇOS`.
- Se a busca estiver trazendo e-mails demais ou de menos, preencha **Busca personalizada no Gmail** na aba Config.
  Ela usa a mesma sintaxe da busca do Gmail. Exemplo: `subject:(11/2026) has:attachment`.
- Sempre que um e-mail aparecer como **NÃO ENCONTRADO NA PLANILHA**, olhe se o médico está com outro nome no controle.
- O script não altera nenhuma das colunas originais. Ele só escreve nas duas colunas novas e nas abas Resumo e E-mails.
