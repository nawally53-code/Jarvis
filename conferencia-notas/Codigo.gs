/**
 * CONFERÊNCIA DE NOTAS FISCAIS — Repasses Médicos (ING, ANGIOCARDIS, ENCORE, CCRI)
 *
 * Lê os e-mails da caixa onde o script é instalado (Gmail),
 * procura as notas da competência configurada e marca, em cada linha
 * das abas de controle (ING, ANGIOCARDIS, ENCORE, CCRI...), se a nota foi recebida.
 *
 * Instale este código na planilha usando a conta repassesmedicos.
 * Veja o arquivo COMO-USAR.md para o passo a passo.
 */

// ----------------------------------------------------------------------------
// Nomes das abas criadas pelo script (as demais abas são tratadas como controle)
// ----------------------------------------------------------------------------
var ABA_CONFIG = 'Config';
var ABA_EMAILS = 'E-mails';
var ABA_RESUMO = 'Resumo';
var ABAS_SISTEMA = [ABA_CONFIG, ABA_EMAILS, ABA_RESUMO];

var COL_STATUS = 'STATUS NOTA (E-MAIL)';
var COL_DETALHE = 'E-MAIL ENCONTRADO';

var STATUS_RECEBIDA = 'RECEBIDA';
var STATUS_VERIFICAR = 'VERIFICAR';
var STATUS_PENDENTE = 'PENDENTE';

var COR = {
  RECEBIDA: '#c8e6c9',
  VERIFICAR: '#fff3b0',
  PENDENTE: '#f8c4c4'
};

// Palavras ignoradas na comparação de nomes e empresas
var IGNORAR_NOME = ['DE', 'DA', 'DO', 'DOS', 'DAS', 'E', 'DR', 'DRA', 'JR', 'JUNIOR', 'FILHO', 'NETO', 'SOBRINHO'];
var IGNORAR_EMPRESA = IGNORAR_NOME.concat([
  'LTDA', 'LT', 'ME', 'EPP', 'EIRELI', 'SS', 'S', 'A', 'SA', 'UNI', 'UNIPESSOAL', 'CIA', 'SOCIEDADE', 'SIMPLES', 'CIVIL', 'L',
  'SERVICOS', 'SERVICO', 'SEVICOS', 'MEDICOS', 'MEDICO', 'MEDICA', 'MEDICINA', 'CLINICA', 'CONSULTORIO',
  'ASSISTENCIA', 'ATENDIMENTO', 'SAUDE', 'HOSPITALARES', 'DIAGNOSTICOS', 'ASSOCIADOS', 'INSTITUTO', 'CENTRO', 'EM', 'SS1'
]);

// ============================================================================
// MENU
// ============================================================================
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Conferência de Notas')
    .addItem('▶ Conferir agora', 'conferirNotas')
    .addSeparator()
    .addItem('Configurar (primeira vez)', 'configurar')
    .addItem('Ativar conferência automática diária', 'ativarAutomatico')
    .addItem('Desativar conferência automática', 'desativarAutomatico')
    .addSeparator()
    .addItem('Preparar novo mês (apagar abas antigas)', 'prepararNovoMes')
    .addToUi();
}

// ============================================================================
// CONFIGURAÇÃO
// ============================================================================
function configurar() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var aba = ss.getSheetByName(ABA_CONFIG) || ss.insertSheet(ABA_CONFIG, 0);
  if (aba.getLastRow() < 2) {
    var hoje = new Date();
    var comp = Utilities.formatDate(hoje, Session.getScriptTimeZone(), 'MM/yyyy');
    aba.getRange('A1:C1').setValues([['CONFIGURAÇÃO', 'VALOR', 'EXPLICAÇÃO']]).setFontWeight('bold');
    aba.getRange('A2:C5').setValues([
      ['Competência', comp, 'Mês/ano das notas a conferir. Ex.: 11/2026'],
      ['Buscar e-mails dos últimos (dias)', 60, 'Até quantos dias atrás procurar e-mails'],
      ['Busca personalizada no Gmail (opcional)', '', 'Deixe em branco para usar a busca automática pela competência. Ex.: subject:(11/2026) has:attachment'],
      ['Última conferência', '', 'Preenchido automaticamente']
    ]);
    aba.getRange('B2').setNumberFormat('@');
    aba.setColumnWidth(1, 260); aba.setColumnWidth(2, 220); aba.setColumnWidth(3, 520);
  }
  SpreadsheetApp.getUi().alert(
    'Pronto!\n\n1) Confira a competência na aba "Config".\n' +
    '2) Importe a planilha do mês (Arquivo > Importar > Inserir nova(s) página(s)).\n' +
    '3) Clique em Conferência de Notas > Conferir agora.'
  );
}

function lerConfig_() {
  var aba = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(ABA_CONFIG);
  if (!aba) throw new Error('Rode primeiro: Conferência de Notas > Configurar (primeira vez).');
  var v = aba.getRange('B2:B4').getDisplayValues();
  return {
    competencia: String(v[0][0]).trim(),
    dias: parseInt(v[1][0], 10) || 60,
    buscaPersonalizada: String(v[2][0]).trim(),
    aba: aba
  };
}

// ============================================================================
// AUTOMÁTICO
// ============================================================================
function ativarAutomatico() {
  desativarAutomatico(true);
  ScriptApp.newTrigger('conferirNotas').timeBased().everyDays(1).atHour(7).create();
  SpreadsheetApp.getUi().alert('Conferência automática ativada: todos os dias por volta das 7h.');
}

function desativarAutomatico(silencioso) {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'conferirNotas') ScriptApp.deleteTrigger(t);
  });
  if (silencioso !== true) SpreadsheetApp.getUi().alert('Conferência automática desativada.');
}

// ============================================================================
// NOVO MÊS
// ============================================================================
function prepararNovoMes() {
  var ui = SpreadsheetApp.getUi();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var abas = ss.getSheets().filter(function (s) { return ABAS_SISTEMA.indexOf(s.getName()) < 0; });
  var nomes = abas.map(function (s) { return s.getName(); }).join(', ') || '(nenhuma)';
  var r = ui.alert('Apagar as abas do mês anterior?', 'Serão apagadas: ' + nomes +
    '\n\nAs abas Config, E-mails e Resumo são mantidas.', ui.ButtonSet.YES_NO);
  if (r !== ui.Button.YES) return;
  if (!ss.getSheetByName(ABA_CONFIG)) configurar();
  abas.forEach(function (s) { ss.deleteSheet(s); });
  ui.alert('Feito. Agora:\n1) Atualize a competência na aba "Config".\n' +
    '2) Arquivo > Importar > envie a planilha do mês > "Inserir nova(s) página(s)".\n' +
    '3) Conferência de Notas > Conferir agora.');
}

// ============================================================================
// CONFERÊNCIA PRINCIPAL
// ============================================================================
function conferirNotas() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var cfg = lerConfig_();

  // 1) Linhas de controle
  var linhas = [];
  var abasControle = [];
  ss.getSheets().forEach(function (aba) {
    if (ABAS_SISTEMA.indexOf(aba.getName()) >= 0) return;
    var dados = aba.getDataRange().getDisplayValues();
    var lidas = lerLinhasControle(dados, aba.getName());
    if (lidas.cabecalho < 0) return;
    abasControle.push({ aba: aba, info: lidas });
    linhas = linhas.concat(lidas.linhas);
  });
  if (!linhas.length) {
    throw new Error('Não encontrei abas de controle (com colunas MÉDICO e EMPRESA). ' +
      'Importe a planilha do mês com Arquivo > Importar > "Inserir nova(s) página(s)".');
  }

  // 2) E-mails
  var consulta = cfg.buscaPersonalizada || montarBuscaGmail(cfg.competencia, cfg.dias);
  if (cfg.buscaPersonalizada && !/newer_than|after:/.test(consulta)) consulta += ' newer_than:' + cfg.dias + 'd';
  var emails = buscarEmails_(consulta);
  _ULTIMA_.linhas = linhas;
  _ULTIMA_.emails = emails;

  // 3) Cruzamento
  var res = cruzar(linhas, emails);

  // 4) Escrever resultado
  abasControle.forEach(function (ac) { escreverStatus_(ac.aba, ac.info, res.porLinha); });
  escreverEmails_(ss, emails, res.porEmail);
  escreverResumo_(ss, linhas, res.porLinha, emails, res.porEmail, cfg, consulta);
  cfg.aba.getRange('B5').setValue(new Date());

  try {
    ss.toast('Conferência concluída: ' + emails.length + ' e-mail(s) lidos, ' + linhas.length + ' linha(s) conferidas.', 'Conferência de Notas', 8);
  } catch (e) { /* execução automática, sem tela */ }
}

// ============================================================================
// LEITURA DA PLANILHA DE CONTROLE (lógica pura — testável)
// ============================================================================
function lerLinhasControle(dados, nomeAba) {
  var cab = -1, col = {};
  for (var i = 0; i < Math.min(dados.length, 15); i++) {
    var norm = dados[i].map(normalizar);
    var iMed = norm.indexOf('MEDICO'), iEmp = norm.indexOf('EMPRESA');
    if (iMed >= 0 && iEmp >= 0) {
      cab = i;
      col.medico = iMed;
      col.empresa = iEmp;
      col.cnpj = norm.indexOf('CNPJ');
      col.item = norm.indexOf('ITEM');
      col.servico = indiceQueComeca_(norm, 'SERVICO PRESTADO');
      col.local = norm.indexOf('LOCAL');
      col.status = norm.indexOf(normalizar(COL_STATUS));
      col.detalhe = norm.indexOf(normalizar(COL_DETALHE));
      break;
    }
  }
  var linhas = [];
  if (cab < 0) return { cabecalho: -1, colunas: col, linhas: linhas };

  var hospitalAba = hospitalDaAba(nomeAba);
  for (var r = cab + 1; r < dados.length; r++) {
    var row = dados[r];
    var medico = limpo_(row[col.medico]);
    var empresa = limpo_(row[col.empresa]);
    if (!medico && !empresa) continue;
    if (/^(TOTAL|ING|ANGIO)\b/.test(normalizar(medico)) && !empresa) continue;
    // Se houver um novo cabeçalho no meio da aba (ex.: bloco ANGIOCARDIS abaixo do ING)
    if (normalizar(medico) === 'MEDICO') {
      var novo = detectarHospitais(normalizar((dados[r - 1] || []).join(' ') + ' ' + row.join(' ')));
      if (novo.length === 1) hospitalAba = novo[0];
      continue;
    }
    var local = col.local >= 0 ? normalizar(row[col.local]) : '';
    var doLocal = detectarHospitais(local);
    var hospital = doLocal.length === 1 ? doLocal[0] : hospitalAba;
    var item = col.item >= 0 ? row[col.item] : '';
    var servico = col.servico >= 0 ? row[col.servico] : '';
    linhas.push({
      aba: nomeAba,
      linhaPlanilha: r + 1,          // número da linha na planilha (1-based)
      hospital: hospital,
      medico: medico,
      empresa: empresa,
      cnpj: so_digitos_(col.cnpj >= 0 ? row[col.cnpj] : ''),
      tipo: tipoServico(item + ' ' + servico),
      descricao: limpo_(item + ' / ' + servico)
    });
  }
  return { cabecalho: cab, colunas: col, linhas: linhas };
}

// ============================================================================
// GMAIL
// ============================================================================
function montarBuscaGmail(competencia, dias) {
  var m = String(competencia).match(/(\d{1,2})\D+(\d{2,4})/);
  var termos = [];
  if (m) {
    var mes = ('0' + m[1]).slice(-2), ano = m[2].length === 2 ? '20' + m[2] : m[2], ano2 = ano.slice(-2);
    var nomes = ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'];
    termos = ['"' + mes + '/' + ano + '"', '"' + mes + '/' + ano2 + '"', '"' + mes + '-' + ano + '"', '"' + mes + '.' + ano + '"',
      '"competencia ' + mes + '"', '"competência ' + mes + '"', '"comp ' + mes + '"', nomes[parseInt(mes, 10) - 1].toLowerCase()];
    if (mes === '03') termos.push('março');
  }
  var q = termos.length ? '{' + termos.join(' ') + '}' : '';
  return (q + ' newer_than:' + (dias || 60) + 'd -in:sent -in:drafts').trim();
}

function buscarEmails_(consulta) {
  var eu = (Session.getEffectiveUser().getEmail() || '').toLowerCase();
  var emails = [], inicio = 0, lote = 100;
  while (inicio < 1000) {
    var threads = GmailApp.search(consulta, inicio, lote);
    threads.forEach(function (t) {
      t.getMessages().forEach(function (msg) {
        var de = msg.getFrom();
        var endereco = ((de.match(/<([^>]+)>/) || [null, de])[1] || '').toLowerCase().trim();
        if (eu && endereco === eu) return; // ignora respostas enviadas pela própria caixa
        var anexos = [];
        try {
          anexos = msg.getAttachments({ includeInlineImages: false }).map(function (a) { return a.getName(); });
        } catch (e) { /* ignora */ }
        emails.push({
          id: msg.getId(),
          data: msg.getDate(),
          de: de,
          assunto: msg.getSubject() || '',
          anexos: anexos,
          corpo: (msg.getPlainBody() || '').slice(0, 3000),
          link: 'https://mail.google.com/mail/u/0/#all/' + msg.getId()
        });
      });
    });
    if (threads.length < lote) break;
    inicio += lote;
  }
  return emails;
}

// ============================================================================
// CRUZAMENTO (lógica pura — testável)
// ============================================================================
function cruzar(linhas, emails) {
  var prepLinhas = linhas.map(prepararLinha_);
  var prepEmails = emails.map(prepararEmail_);

  var porEmail = prepEmails.map(function () { return []; });
  var porLinha = prepLinhas.map(function () { return { exato: [], semTipo: [], outroTipo: [] }; });

  prepEmails.forEach(function (pe, ie) {
    var cands = [];
    prepLinhas.forEach(function (pl, il) {
      if (pe.hospitais.length && pe.hospitais.indexOf(pl.hospital) < 0) return;
      var s = pontuar_(pl, pe);
      if (s > 0) cands.push({ il: il, s: s });
    });
    if (!cands.length) return;
    var max = Math.max.apply(null, cands.map(function (c) { return c.s; }));
    cands.filter(function (c) { return c.s === max; }).forEach(function (c) {
      porEmail[ie].push(c.il);
      var pl = prepLinhas[c.il];
      if (!pe.tipo) porLinha[c.il].semTipo.push(ie);
      else if (pe.tipo === pl.tipo) porLinha[c.il].exato.push(ie);
      else porLinha[c.il].outroTipo.push(ie);
    });
  });

  // Quantas linhas do mesmo médico/hospital ficaram sem e-mail de tipo exato
  var semExatoPorChave = {};
  prepLinhas.forEach(function (pl, il) {
    if (!porLinha[il].exato.length) semExatoPorChave[pl.chave] = (semExatoPorChave[pl.chave] || 0) + 1;
  });

  var resultado = prepLinhas.map(function (pl, il) {
    var m = porLinha[il];
    var status, obs, usados;
    if (m.exato.length) {
      status = STATUS_RECEBIDA; usados = m.exato; obs = '';
    } else if (m.semTipo.length) {
      usados = m.semTipo;
      if (m.semTipo.length >= semExatoPorChave[pl.chave]) {
        status = STATUS_RECEBIDA; obs = '';
      } else {
        status = STATUS_VERIFICAR;
        obs = m.semTipo.length + ' e-mail(s) para ' + semExatoPorChave[pl.chave] + ' linha(s) deste médico — conferir se falta nota';
      }
    } else if (m.outroTipo.length) {
      status = STATUS_VERIFICAR; usados = m.outroTipo;
      obs = 'Só achei e-mail de outro serviço (' + m.outroTipo.map(function (i) { return prepEmails[i].tipo; }).join(', ') + ')';
    } else {
      status = STATUS_PENDENTE; usados = []; obs = '';
    }
    return { status: status, obs: obs, emails: usados };
  });

  return { porLinha: resultado, porEmail: porEmail };
}

function prepararLinha_(l) {
  // primeiro nome com 3+ letras; sobrenomes curtos (ex.: SÁ) também contam
  var tokNome = tokens_(l.medico, IGNORAR_NOME).filter(function (t, i) { return t.length >= (i === 0 ? 3 : 2); });
  var tokEmp = tokens_(l.empresa, IGNORAR_EMPRESA).filter(function (t) { return t.length >= 2; });
  return {
    hospital: l.hospital,
    tipo: l.tipo,
    nome: tokNome,
    empresa: tokEmp,
    cnpj: l.cnpj && l.cnpj.length === 14 ? l.cnpj : '',
    chave: l.hospital + '|' + (l.cnpj && l.cnpj.length === 14 ? l.cnpj : normalizar(l.medico)) + '|' + normalizar(l.medico)
  };
}

function prepararEmail_(e) {
  var nomeRemetente = String(e.de || '').replace(/<[^>]*>/, ' ');
  var endereco = (String(e.de || '').match(/<([^>]+)>/) || [null, e.de || ''])[1];
  var localEndereco = String(endereco).split('@')[0].replace(/[._\-0-9]+/g, ' ');
  var cabecalho = [e.assunto, nomeRemetente, localEndereco].concat(e.anexos || []).join(' ');
  var cabNorm = normalizar(cabecalho);
  var hospText = normalizar([e.assunto].concat(e.anexos || []).join(' '));
  return {
    palavrasCab: conjunto_(cabNorm),
    palavrasCorpo: conjunto_(normalizar(e.corpo || '')),
    digitos: so_digitos_(cabecalho + ' ' + (e.corpo || '')),
    hospitais: hospitaisDoEmail(hospText),
    tipo: tipoEmail(normalizar([e.assunto].concat(e.anexos || []).join(' ')))
  };
}

/** 3 = nome do médico, 2 = CNPJ, 1 = nome da empresa, 0 = não bate */
function pontuar_(pl, pe) {
  var n = pl.nome;
  if (n.length >= 2) {
    var noCab = n.filter(function (t) { return pe.palavrasCab[t]; }).length;
    if (pe.palavrasCab[n[0]] && noCab >= 2) return 3;
    var noCorpo = n.filter(function (t) { return pe.palavrasCorpo[t]; }).length;
    if (noCorpo === n.length) return 3;
  }
  if (pl.cnpj && pe.digitos.indexOf(pl.cnpj) >= 0) return 2;
  var emp = pl.empresa;
  if (emp.length) {
    var todos = emp.every(function (t) { return pe.palavrasCab[t]; });
    var forte = emp.some(function (t) { return t.length >= (emp.length === 1 ? 5 : 4); });
    if (todos && forte) return 1;
  }
  return 0;
}

// ============================================================================
// HOSPITAIS
// ============================================================================
// Para incluir outro hospital, acrescente uma linha: [NOME, expressão que o identifica]
var HOSPITAIS = [
  ['ANGIOCARDIS', /\bANGIOCARDIS\b|\bANGIO\b|\bANGIOCARDIO\b/],
  ['ENCORE', /\bH?ENCORE\b/],
  ['CCRI VILA BRASILIA', /\bCCRI\b.*\b(VLB|VILA|BRASILIA)\b|\bVILA BRASILIA\b/],
  ['CCRI CERES', /\bCERES\b/],
  ['ING', /\bING\b|\bNEUROLOGICO\b|INSTITUTO DE NEUROLOGIA/]
];

/** Hospitais citados num texto já normalizado. */
function detectarHospitais(textoNorm) {
  return HOSPITAIS.filter(function (h) { return h[1].test(textoNorm); }).map(function (h) { return h[0]; });
}

/** Hospital de uma aba de controle, pelo nome da aba (ex.: ING, ANGIOCARDIS, ENCORE, CCRI VLB). */
function hospitalDaAba(nomeAba) {
  var n = normalizar(nomeAba);
  var h = detectarHospitais(n);
  return h.length === 1 ? h[0] : (n || 'SEM NOME');
}

/** Hospitais citados no assunto/anexos do e-mail. Vazio = não restringe. */
function hospitaisDoEmail(textoNorm) {
  var h = detectarHospitais(textoNorm);
  // "CCRI" sozinho vale para as duas unidades CCRI
  if (!h.length && /\bCCRI\b/.test(textoNorm)) h = ['CCRI VILA BRASILIA', 'CCRI CERES'];
  return h;
}

// ============================================================================
// CLASSIFICAÇÃO DO TIPO DE SERVIÇO
// ============================================================================
function tipoServico(texto) {
  var t = normalizar(texto);
  if (/PLANT/.test(t)) return 'PLANTAO';
  if (/REPASSE|\bHM\b|HONORARIO|BONUS|HEMODINAMICA|PRODUCAO/.test(t)) return 'REPASSE';
  return 'DEMAIS';
}

function tipoEmail(t) {
  var tipos = [];
  if (/PLANT/.test(t)) tipos.push('PLANTAO');
  if (/REPASSE|\bHM\b|HONORARIO|BONUS/.test(t)) tipos.push('REPASSE');
  if (/DEMAIS|SOBREAVISO|COORDENA|ACIONAMENTO|EVOLUC|DIRETOR|GERENTE|AUDITOR|ALUGUEL|FISIOTERAPIA|FONO|CONSULTORIA|SERVICO MEDICO CONTRATADO/.test(t)) tipos.push('DEMAIS');
  return tipos.length === 1 ? tipos[0] : ''; // ambíguo ou sem indicação = sem tipo
}

// ============================================================================
// ESCRITA DOS RESULTADOS
// ============================================================================
function escreverStatus_(aba, info, porLinha) {
  var cab = info.cabecalho + 1;
  var col = info.colunas;
  var ultima = aba.getLastColumn();
  var cStatus = col.status >= 0 ? col.status + 1 : ultima + 1;
  var cDet = col.detalhe >= 0 ? col.detalhe + 1 : (col.status >= 0 ? ultima + 1 : ultima + 2);
  aba.getRange(cab, cStatus).setValue(COL_STATUS).setFontWeight('bold');
  aba.getRange(cab, cDet).setValue(COL_DETALHE).setFontWeight('bold');

  // índice global das linhas desta aba, na ordem em que foram lidas
  var resultados = cruzarResultadosDaAba_(aba.getName(), porLinha);
  resultados.forEach(function (r) {
    aba.getRange(r.linha, cStatus).setValue(r.status).setBackground(COR[r.status]);
    aba.getRange(r.linha, cDet).setValue(r.detalhe);
  });
  aba.setColumnWidth(cStatus, 160);
  aba.setColumnWidth(cDet, 420);
}

// guarda temporária com as linhas lidas e os e-mails, preenchida em conferirNotas
var _ULTIMA_ = { linhas: [], emails: [] };

function cruzarResultadosDaAba_(nomeAba, porLinha) {
  var out = [];
  _ULTIMA_.linhas.forEach(function (l, i) {
    if (l.aba !== nomeAba) return;
    var r = porLinha[i];
    var det = r.emails.map(function (ie) {
      var e = _ULTIMA_.emails[ie];
      return Utilities.formatDate(e.data, Session.getScriptTimeZone(), 'dd/MM') + ' — ' + e.assunto;
    }).join(' | ');
    if (r.obs) det = (det ? det + ' | ' : '') + r.obs;
    out.push({ linha: l.linhaPlanilha, status: r.status, detalhe: det });
  });
  return out;
}

function escreverEmails_(ss, emails, porEmail) {
  var aba = ss.getSheetByName(ABA_EMAILS) || ss.insertSheet(ABA_EMAILS);
  aba.clear();
  var cab = [['DATA', 'REMETENTE', 'ASSUNTO', 'ANEXOS', 'VINCULADO À LINHA', 'ABRIR']];
  var dados = emails.map(function (e, i) {
    var vinc = porEmail[i].map(function (il) {
      var l = _ULTIMA_.linhas[il];
      return l.hospital + ' — ' + l.medico + ' (' + l.tipo + ', linha ' + l.linhaPlanilha + ')';
    });
    return [e.data, e.de, e.assunto, e.anexos.join(', '),
      vinc.length ? vinc.join(' | ') : 'NÃO ENCONTRADO NA PLANILHA', e.link];
  });
  aba.getRange(1, 1, 1, cab[0].length).setValues(cab).setFontWeight('bold');
  if (dados.length) {
    aba.getRange(2, 1, dados.length, cab[0].length).setValues(dados);
    aba.getRange(2, 1, dados.length, 1).setNumberFormat('dd/MM/yyyy HH:mm');
    dados.forEach(function (d, i) {
      if (d[4] === 'NÃO ENCONTRADO NA PLANILHA') aba.getRange(i + 2, 5).setBackground(COR.VERIFICAR);
    });
  }
  aba.setFrozenRows(1);
  aba.setColumnWidth(2, 260); aba.setColumnWidth(3, 380); aba.setColumnWidth(4, 260); aba.setColumnWidth(5, 380);
}

function escreverResumo_(ss, linhas, porLinha, emails, porEmail, cfg, consulta) {
  var aba = ss.getSheetByName(ABA_RESUMO) || ss.insertSheet(ABA_RESUMO, 1);
  aba.clear();
  var cont = {};
  linhas.forEach(function (l, i) {
    var h = l.hospital;
    cont[h] = cont[h] || { total: 0, RECEBIDA: 0, VERIFICAR: 0, PENDENTE: 0 };
    cont[h].total++;
    cont[h][porLinha[i].status]++;
  });
  var semVinculo = porEmail.filter(function (v) { return !v.length; }).length;

  var out = [
    ['CONFERÊNCIA DE NOTAS — COMPETÊNCIA ' + cfg.competencia, '', '', '', ''],
    ['Atualizado em', Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'dd/MM/yyyy HH:mm'), '', '', ''],
    ['E-mails lidos', emails.length, 'Sem vínculo com a planilha', semVinculo, ''],
    ['Busca usada no Gmail', consulta, '', '', ''],
    ['', '', '', '', ''],
    ['HOSPITAL', 'LINHAS', 'RECEBIDA', 'VERIFICAR', 'PENDENTE']
  ];
  Object.keys(cont).sort().forEach(function (h) {
    out.push([h, cont[h].total, cont[h].RECEBIDA, cont[h].VERIFICAR, cont[h].PENDENTE]);
  });
  out.push(['', '', '', '', '']);
  out.push(['PENDENTES / VERIFICAR', 'HOSPITAL', 'SERVIÇO', 'STATUS', 'OBS.']);
  linhas.forEach(function (l, i) {
    var r = porLinha[i];
    if (r.status === STATUS_RECEBIDA) return;
    out.push([l.medico + ' — ' + l.empresa, l.hospital, l.descricao, r.status, r.obs]);
  });
  aba.getRange(1, 1, out.length, 5).setValues(out);
  aba.getRange('A1').setFontWeight('bold').setFontSize(13);
  aba.getRange('A6:E6').setFontWeight('bold');
  var iPend = out.findIndex(function (r) { return r[0] === 'PENDENTES / VERIFICAR'; });
  aba.getRange(iPend + 1, 1, 1, 5).setFontWeight('bold');
  for (var i = iPend + 1; i < out.length; i++) aba.getRange(i + 1, 4).setBackground(COR[out[i][3]]);
  aba.setColumnWidth(1, 420); aba.setColumnWidth(2, 140); aba.setColumnWidth(3, 320); aba.setColumnWidth(5, 380);
}

// ============================================================================
// UTILITÁRIOS
// ============================================================================
function normalizar(s) {
  return String(s == null ? '' : s)
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, ' ')
    .trim();
}
function tokens_(s, ignorar) {
  return normalizar(s).split(' ').filter(function (t) { return t && ignorar.indexOf(t) < 0; });
}
function conjunto_(textoNorm) {
  var o = {};
  textoNorm.split(' ').forEach(function (t) { if (t) o[t] = true; });
  return o;
}
function so_digitos_(s) { return String(s == null ? '' : s).replace(/\D/g, ''); }
function limpo_(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim(); }
function indiceQueComeca_(arr, prefixo) {
  for (var i = 0; i < arr.length; i++) if (arr[i].indexOf(prefixo) === 0) return i;
  return -1;
}
