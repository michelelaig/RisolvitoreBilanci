dare = 'dare'
avere = 'avere'

imm_imm = 'immobilizazioni immateriali'
imm_mat = 'immobilizazioni materiali'
brev = 'brevetti'
marc = 'marchi'
macc = 'macchinario'
impi = 'impianto'
fabb = 'fabbricato'

att_circ = 'attivo circolante'
attr = 'attrzzatura'
prod_fin_vend = 'prodotti finiti conto vendita'
fitt_att = 'fitto attivo'
fitt_pass = 'fitto passivo'
cred_clie = 'credito clienti'
banc = 'banca'
patr_nett = 'patrimonio netto'
cap_soc = 'capitale sociale'
ris_leg = 'riserva legale'
uti_net = 'utile netto'
deb = 'debiti'
mat_prim = 'materie prime'
deb_forn = 'debiti vs fornitori'
deb_trib = 'debiti tributari'
deb_banc = 'debiti verso banche'
attivita = 'attività'
passivita = 'passività'
minus = 'minusvalenza'
spese = 'spese'
spese_varie = 'spese varie'
ricavi = 'ricavi'
amm = 'ammortamenti'
risc_pass = 'risconto passivo'
risc_att = 'risconto attivo'
rateo_pass = 'rateo passivo'
uten = 'utenze'
stip = 'stipendi'
int_pas = 'interessi passivi'
rim = 'rimanenze'
rim_fin = 'rimanenze finali'
accant = 'accantonamento'
fond_risc = 'fondi rischi e oneri'
ris_sovr_az = 'riserva sovrapprezzo azioni'
deb_az = 'debito azionisti'
voci_SP = [banc,deb_banc,brev,macc,impi,fabb,cred_clie,cap_soc,ris_leg,uti_net,deb_forn,deb_trib,deb_banc,fond_risc,ris_sovr_az]
voci_att_imm_imm = [brev,marc]
voci_amm_imm = [f'ammortamento {el}' for el in voci_att_imm_imm]
#print(voci_amm_imm)
voci_att_imm_mat = [macc,impi,fabb,attr]
voci_amm_mat = [f'ammortamento {el}' for el in voci_att_imm_mat]
voci_att_att_circ = [banc,cred_clie,rim,risc_att]
voci_pass_patr_nett = [cap_soc,ris_leg,uti_net,ris_sovr_az]
voci_pass_deb = [deb_forn,deb_trib,deb_banc,deb_az]
voci_pass_boh = [risc_pass,rateo_pass,fond_risc]

voci_spes = [spese_varie,mat_prim,uten,int_pas,stip,fitt_pass,accant,minus]
voci_rica = [prod_fin_vend,fitt_att,rim_fin]
voci_amm = []


tasso_imposte = .3

mastrino_latex_l = [
	'\\begin{table}[ht]',
	'\centering \n\\begin{tabular}{|c|c|}\n\hline\n',
	'\multicolumn{2}{|c|}{%s} \\\ \n',
	'\hline %s \hline \n',
	'%s & %s \\\ \n\hline\n',
	'%s \\\ \n\hline\n',
	'\\end{tabular} \end{table}']




