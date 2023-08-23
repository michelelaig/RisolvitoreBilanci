from stringhe import *



class StatoPatrimoniale():
	def __init__(self,diz = None):
		if diz:
			self.prezzo_azioni = 10
			self.SP = diz
		else:
			self.SP = {}
	
	def __repr__(self):
		return str(self.SP)
	def fai_tot_att(self):
		tot = 0
		for sezione in self.SP[attivita]:
			for voce in self.SP[attivita][sezione]:
				tot+= self.SP[attivita][sezione][voce]
		return tot
	def fai_tot_pas(self):
		tot = 0
		for sezione in self.SP[passivita]:
			for voce in self.SP[passivita][sezione]:
				tot+=self.SP[passivita][sezione][voce]
		return tot
	def fai_mastrini(self):
		out = {}
		for sezione in self.SP[attivita]:
			for voce in self.SP[attivita][sezione]:
				check_mastrino_exist(out,voce)
				out[voce].dare.append(self.SP[attivita][sezione][voce])
		for sezione in self.SP[passivita]:
			for voce in self.SP[passivita][sezione]:
				check_mastrino_exist(out,voce)
				out[voce].avere.append(self.SP[passivita][sezione][voce])
		return out
	def compila(self,mastrini):
		out = {attivita: {imm_imm: {}, imm_mat : {}, att_circ : {} }, passivita : {patr_nett : {}, deb : {}}}
		for v in voci_att_imm_imm:
			if v in mastrini:
				out[attivita][imm_imm][v] = -mastrini[v].somma()
		for v in voci_att_imm_mat:
			if v in mastrini:
				tmp = -mastrini[v].somma()
				if f'fondo ammortamento {v}' in mastrini:
					tmp-=mastrini[f'fondo ammortamento {v}'].somma()
				out[attivita][imm_mat][v] = tmp
		
		for v in voci_att_att_circ:
			if v in mastrini:
				out[attivita][att_circ][v] = -mastrini[v].somma()
		
		for v in voci_pass_patr_nett:
			if v in mastrini:
				out[passivita][patr_nett][v] = mastrini[v].somma()
		for v in voci_pass_deb:
			if v in mastrini:
				out[passivita][deb][v] = mastrini[v].somma()
		for v in voci_pass_boh:
			if v in mastrini:
				out[passivita][deb][v] = mastrini[v].somma()

		self.SP = out					
	def to_latex(self):
		return str(self.SP)



class ContoEconomico():
	def __init__(self,mastrini):
		self.CE = {dare: {spese : {},amm : {}},avere:{}}
		for v in voci_spes:
			if v in mastrini:
				if mastrini[v].somma()<0:
					self.CE[dare][spese][v] = -mastrini[v].somma()
		for v in voci_amm_imm:
			if v in mastrini:
				if mastrini[v].somma()<0:
					self.CE[dare][amm][v] = -mastrini[v].somma()
		for v in voci_amm_mat:
			if v in mastrini and mastrini[v].somma()<0:
				self.CE[dare][amm][v] = -mastrini[v].somma()
		for v in voci_rica:
			if v in mastrini:
					self.CE[avere][v] = mastrini[v].somma()
	def __repr__(self):
		return str(self.CE)
	def tot_ricavi(self):
		out = 0
		for voce in self.CE[avere]:
			out += self.CE[avere][voce]
		return out
	def tot_amm(self):
		out = 0
		for voce in self.CE[dare][amm]:
			out += self.CE[dare][amm][voce]
		return out
	def tot_spese(self):
		out = 0
		for sezione in self.CE[dare]:
			for voce in self.CE[dare][sezione]:
				out += self.CE[dare][sezione][voce]
		return out
	def aggiorna_mastrini(self,mastrini):
		utile_lordo = self.tot_ricavi()-self.tot_spese()
		imposte = utile_lordo*tasso_imposte
		utile_netto = utile_lordo-imposte
		check_mastrino_exist(mastrini,uti_net)
		check_mastrino_exist(mastrini,deb_trib)
		mastrini[uti_net].avere.append(utile_netto)
		mastrini[deb_trib].avere.append(imposte)
		print(f'tot amm = {self.tot_amm()}')
		print(f'tot spese = {self.tot_spese()}')
		print(f'tot ricavi = {self.tot_ricavi()}')
		print(f'reddito lordo ={utile_lordo}')
		print(f'imposte = {imposte}')
		print(f'reddito netto ={utile_netto}')
		return mastrini

class mastrino():
	def __init__(self,nome):
		self.nome = nome
		self.dare = []
		self.avere = []
	def __repr__(self):
		tot = sum(self.avere)-sum(self.dare)
		return f'{self.nome} {self.dare}-{self.avere}'
	def somma(self):
		return sum(self.avere)-sum(self.dare)
	def tot_dare(self):
		return sum(self.dare)
	def tot_avere(self):
		return sum(self.avere)
	def add_dare(self,ammontare):
		if ammontare!=0:
			self.dare.append(ammontare)
	def add_avere(self,ammontare):
		if ammontare!=0:
			self.avere.append(ammontare)	
	def chiudi(self):
		self.avere=[]
		self.dare=[]
	def to_latex(self):
		mast = ''.join(s for s in mastrino_latex_l)
		s = '%s & %s \\\ \n'
		tmp_s = ''
		fin = ''
		n_righe = max(len(self.dare),len(self.avere))
		if n_righe!=1:
			for i in range(n_righe):
				a = 0
				b = 0
				if i < len(self.dare):
					a = self.dare[i]
				if i < len(self.avere):
					b = self.avere[i]
				tmp_s+= s%(str(a),str(b))
		som = self.somma()
		if som<0:
			fin =  s%(str(-som),str(0))
		else:
			fin = s%(str(0),str(som))

		mast = mast%(f'{self.nome}',f'{tmp_s}',f'{self.tot_dare()}',f'{self.tot_avere()}',fin)	
		return  mast

def check_mastrino_exist(mastrini,m):
	if m not in mastrini:
		mastrini[m] = mastrino(m)


def dare_avere(mastrini,sinistro,destro,ammontare):
	check_mastrino_exist(mastrini,sinistro)
	check_mastrino_exist(mastrini,destro)
	mastrini[sinistro].add_dare(ammontare)
	mastrini[destro].add_avere(ammontare)

def fai_mutuo(mastrini,ammontare):
	check_mastrino_exist(mastrini,deb_banc)
	check_mastrino_exist(mastrini,banc)
	mastrini[banc].dare.append(ammontare)
	mastrini[deb_banc].avere.append(ammontare)

#dare è sinistra

def fai_sval(mastrini,cosa,ammontare):
	check_mastrino_exist(mastrini,cosa)
	check_mastrino_exist(mastrini,minus)
	mastrini[cosa].avere.append(ammontare)
	mastrini[minus].dare.append(ammontare)

def fai_amm(mastrini,cosa,ammontare,in_conto):
	check_mastrino_exist(mastrini,f'ammortamento {cosa}')
	if in_conto:
		mastrini[cosa].avere.append(ammontare)
		mastrini[f'ammortamento {cosa}'].dare.append(ammontare)
	else:
		check_mastrino_exist(mastrini,f'fondo ammortamento {cosa}')
		mastrini[f'ammortamento {cosa}'].dare.append(ammontare)
		mastrini[f'fondo ammortamento {cosa}'].avere.append(ammontare)

def acquista_mat_prim(mastrini,ammontare,contanti,credito):
	check_mastrino_exist(mastrini,mat_prim)
	check_mastrino_exist(mastrini,deb_forn)
	check_mastrino_exist(mastrini,banc)
	mastrini[mat_prim].add_dare(ammontare)
	mastrini[banc].add_avere(contanti)
	mastrini[deb_forn].add_avere(credito)

def vendi_prod_fin(mastrini,ammontare,contanti=None,credito=None):
	if not (contanti or credito):
		dare_avere(mastrini,banc,prod_fin_vend,ammontare)
	else:
		check_mastrino_exist(mastrini,banc)
		check_mastrino_exist(mastrini,cred_clie)
		check_mastrino_exist(mastrini,prod_fin_vend)

		mastrini[prod_fin_vend].add_avere(ammontare)
		mastrini[banc].add_dare(contanti)
		mastrini[cred_clie].add_dare(credito)

def fai_aquisto_mat_prim(mastrini,ammontare,contanti,credito):
	#Funzione deprecata per il nome
	acquista_mat_prim(mastrini,ammontare,contanti,credito)

def fai_vendita_prod_fin(mastrini,ammontare,contanti,credito):
	#Funzione deprecata per il nome
	vendi_prod_fin(mastrini,ammontare,contanti,credito)

	


def fai_fitto_attivo(mastrini,ammontare):
	dare_avere(mastrini, banc, fitt_att, ammontare)

def fai_fitto_passivo(mastrini,ammontare):
	dare_avere(mastrini, fitt_pass, banc, ammontare)

def fai_rateo_pass(mastrini,ammontare):
	dare_avere(mastrini,fitt_pass, rateo_pass, ammontare)

#dare è sinistra
def fai_risconto_pass(mastrini,ammontare):
	dare_avere(mastrini,fitt_att,risc_pass,ammontare)

def fai_risconto_att(mastrini,ammontare):
	dare_avere(mastrini,risc_att,fitt_pass,ammontare)

def riscuoti_credito(mastrini,ammontare):
	check_mastrino_exist(mastrini,cred_clie)
	check_mastrino_exist(mastrini,banc)
	mastrini[cred_clie].avere.append(ammontare)
	mastrini[banc].dare.append(ammontare)




def paga_deb_forn(mastrini,ammontare):
	dare_avere(mastrini,deb_forn,banc,ammontare)


def paga_deb_trib(mastrini,ammontare):
	dare_avere(mastrini,deb_trib,banc,ammontare)

def fai_spesa(mastrini,ammontare):
	dare_avere(mastrini,spese_varie,banc,ammontare)

def paga_utile_azionisti(mastrini,ammontare):

	dare_avere(mastrini,uti_net,deb_az,mastrini[uti_net].somma())	
	dare_avere(mastrini,deb_az,banc,ammontare)	
	

def acquista_marc(mastrini,ammontare):
	dare_avere(mastrini,marc,banc,ammontare)
def acquista_brev(mastrini,ammontare):
	dare_avere(mastrini,brev,banc,ammontare)
def acquista_attr(mastrini,ammontare):
	dare_avere(mastrini,attr,banc,ammontare)
def acquista_macc(mastrini,ammontare):
	dare_avere(mastrini,macc,banc,ammontare)
def acquista_fabb(mastrini,ammontare):
	dare_avere(mastrini,fabb,banc,ammontare)
def paga_utenze(mastrini,ammontare):
	dare_avere(mastrini,uten,banc,ammontare)
def paga_stipendi(mastrini,ammontare):
	dare_avere(mastrini,stip,banc,ammontare)

def paga_mutuo(mastrini,totale,intpas,quo_cap):
	check_mastrino_exist(mastrini,deb_banc)
	check_mastrino_exist(mastrini,banc)
	check_mastrino_exist(mastrini,int_pas)
	mastrini[banc].add_avere(totale)
	mastrini[deb_banc].add_dare(quo_cap)
	mastrini[int_pas].add_dare(intpas)

def rileva_rimanenze(mastrini,ammontare):
	dare_avere(mastrini,rim,rim_fin,ammontare)

def fai_accantonamento(mastrini,ammontare):
	dare_avere(mastrini,accant,fond_risc,ammontare)

def vendita_azioni(mastrini,numero_azioni,prezzo_precedente, prezzo_azioni):
	check_mastrino_exist(mastrini, cap_soc)
	check_mastrino_exist(mastrini, ris_sovr_az)
	check_mastrino_exist(mastrini, banc)
	mastrini[banc].add_dare(numero_azioni*prezzo_azioni)
	mastrini[ris_sovr_az].add_avere(numero_azioni*(prezzo_azioni-prezzo_precedente))
	mastrini[cap_soc].add_avere(numero_azioni*prezzo_precedente)

def vendi_impianto(mastrini,ammontare):
	valore = -mastrini[impi].somma()-mastrini['fondo ammortamento impianto'].somma()
	dare_avere(mastrini, banc, impi, ammontare)
	mastrini[impi].chiudi()
	mastrini[('fondo ammortamento impianto')].chiudi()
	#mastrini['fondo ammortamento impianto'].chiudi()
	minusvalenza = -ammontare+valore
	check_mastrino_exist(mastrini,minus)
	mastrini[minus].add_dare(minusvalenza)
	#mastrini[impi].chiudi()
	#print(valore)

