from classi import mastrino, StatoPatrimoniale, ContoEconomico
from stringhe import *
from classi import fai_mutuo,fai_sval
from classi import fai_amm,fai_aquisto_mat_prim,fai_vendita_prod_fin
from classi import fai_fitto_attivo,fai_risconto_pass,fai_spesa
from classi import riscuoti_credito,paga_deb_forn
from classi import paga_utile_azionisti,paga_deb_trib
from classi import acquista_marc,paga_utenze,paga_mutuo,rileva_rimanenze
from classi import paga_stipendi,fai_fitto_passivo,fai_rateo_pass
from classi import acquista_brev,fai_accantonamento
from classi import vendita_azioni,acquista_attr,acquista_fabb
from classi import vendi_impianto,acquista_macc,fai_risconto_att
from classi import acquista_mat_prim,vendi_prod_fin

import subprocess


diz_SP =	{
			attivita: {
				imm_imm : {brev: 1100},
				imm_mat : {macc:800,impi : 2100,fabb : 450},
				att_circ : {cred_clie : 380,banc : 90}},
			passivita: {
				patr_nett : {
					cap_soc : 2500,ris_leg : 500,uti_net : 882},
				deb : {
					deb_forn : 660, deb_trib : 378}
			}
			}

SP = StatoPatrimoniale(diz_SP)
m = SP.fai_mastrini()

fai_mutuo(m,1000)
fai_sval(m,macc,200)
acquista_mat_prim(m,180,0,180)
vendi_prod_fin(m,980,0,980)
fai_fitto_attivo(m,48)
fai_spesa(m,45)
riscuoti_credito(m,250)
paga_deb_forn(m,120)
paga_utile_azionisti(m,352.8)
paga_deb_trib(m,378)
acquista_marc(m,360)
vendi_prod_fin(m,780,780,0)
acquista_mat_prim(m,440,290,150)
riscuoti_credito(m,220)
paga_utenze(m,240)
vendi_prod_fin(m,630)
paga_stipendi(m,960)
paga_mutuo(m,67.216,30,37.216)

rileva_rimanenze(m,1630)



#chiusura
fai_risconto_pass(m,12)
fai_amm(m,brev,100,True)
fai_amm(m,marc,18,True)
fai_amm(m,impi,300,False)
fai_amm(m,fabb,150,False)
fai_amm(m,macc,150,False)

CE = ContoEconomico(m)
mastrini = CE.aggiorna_mastrini(m)

new_SP = StatoPatrimoniale(False)
new_SP.compila(m)


	
yo = ''.join(f'{m[mas].to_latex()} \n' for mas in m)
yo+=new_SP.to_latex()
print(f'Conto Economico: {CE}')
print()
#print(f'Stato Patrimoniale: {new_SP}')


NOME_OUT = 'es'
with open('template.tex','r') as f:
	s = f.read()
	s=s.replace('TEMPLATE',yo)
	with open(f'{NOME_OUT}.tex','w') as out:
		out.write(s)
subprocess.run(["pdflatex",f'{NOME_OUT}.tex'],stdout=subprocess.DEVNULL)
subprocess.run(["rm", f'{NOME_OUT}.aux'],stdout=subprocess.DEVNULL)
subprocess.run(["rm", f'{NOME_OUT}.log'],stdout=subprocess.DEVNULL)
subprocess.run(["rm", f'{NOME_OUT}.toc'],stdout=subprocess.DEVNULL)
subprocess.run(["rm", f'{NOME_OUT}.out'],stdout=subprocess.DEVNULL)



tot_attiv = new_SP.fai_tot_att()
tot_passi = new_SP.fai_tot_pas()

print(f'tot attività  = {tot_attiv}')
print(f'tot passività = {tot_passi}')
