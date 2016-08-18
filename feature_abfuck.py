import glob
import ast
import re


keywords_po = []
keywords_eo = []
liste_pronomen_sg = []
liste_pronomen_pl = []

def get_data(filename, list_of_sents):
	with open(filename, "r") as f_in:
		f_string = f_in.read()
		list_of_sents.append(ast.literal_eval(f_string))
	return list_of_sents


def mapping(list_of_sents):
	return list_of_sents

def sents_length(sent):
	return float(len(sent['tokens']))

def counts_ner(sent): #eventuell auch normalisieren ueber satzlaenge 
	ner_l = len(sent['ner'])
	sents_l = sents_length(sent)
	normalized_counts_ner = float(ner_l / sents_l) * 100
	return normalized_counts_ner

def mainverb(sent):
	for token in sent['tokens']:
		if re.search(r'VB.?', token[3]):
			return token[1]

def modalverb(sent):
	modalverb_list = []
	for token in sent['tokens']:
		if token[3] == 'MD':
			return token[1]

def count_pronomen(sent):
	counter = 0
	for token in sent['tokens']:
		if token[3] == 'PRP':
			counter += 1
	return counter



def count_satzzeichen(sent):
	count_punct = 0
	for token in sent['tokens']:
		if re.search(r'\p', token[1]):
			count_punct += 1
	return count_punct

def keyword_binary_eo(sent):
	with open("keywords_eo.txt", "r") as f_in:
		eo_bin = 0
		f_string = f_in.read()
		keywords_eo = f_string.split("\r\n")
		for token in sent['tokens']:
			if token[1] in keywords_eo:
				eo_bin = 1
		return eo_bin

def keyword_binary_po(sent):
	with open("keywords_po.txt", "r") as f_in:
		po_bin = 0
		f_string = f_in.read()
		keywords_po = f_string.split()
		for token in sent['tokens']:
			if token[1] in keywords_po:
				po_bin = 1
		return po_bin

def keyword_count_eo(sent): #NOCH NORMALISIEREN
	with open("keywords_eo.txt", "r") as f_in:
		eo_count = 0
		f_string = f_in.read()
		keywords_eo = f_string.split("\r\n")
		for token in sent['tokens']:
			if token[1] in keywords_eo:
				eo_count += 1
		sents_l = sents_length(sent)
		norm_eo_count = eo_count / float(sents_l)
		return norm_eo_count

def keyword_count_po(sent): #NOCH NORMALISIEREN
	with open("keywords_po.txt", "r") as f_in:
		po_count = 0
		f_string = f_in.read()
		keywords_po = f_string.split("\r\n")
		for token in sent['tokens']:
			if token[1] in keywords_po:
				po_count += 1
		sents_l = sents_length(sent)
		norm_po_count = po_count / float(sents_l)
		return norm_po_count
 
def adverb(sent):
 	for token in sent['tokens']:
		if token[3] == 'RBR':
			return token[1]
		elif token[3] == 'WRB':
			return token[1]

 #def praemissen-claim-liste

 #fremdwoerter

 #def is_subject_pronomen???

def iob_eo(sent):
	iob_eo_bin = 0
	for token in sent['tokens']:
		if re.search(r'Expert', token[2]):
 			iob_eo_bin = 1
 	return iob_eo_bin

def iob_po(sent):
	iob_po_bin = 0
	for token in sent['tokens']:
		if re.search(r'Popular', token[2]):
 			iob_po_bin = 1
 	return iob_po_bin


 #def pronomen im singular oder plural?











def main():
	#Namen holen von Files in Ordner
	list_of_files = glob.glob("preprocessed/*")
	#Jede Datei durchgehen und getdata() auf alle Dateien anwenden. 
	#Es wird eine Liste erstellt in der jeder Text als Liste hineinkommt. 
	#In diesen Listen sind Dictionaries, die die Saetze darstellen
	list_of_sents = []
	for filename_in in list_of_files:
		get_data(filename_in, list_of_sents)
	#print list_of_sents

	feature_result = []
	list_of_items = mapping(list_of_sents)
	#for text in list_of_items:
	for i in range(0, len(list_of_items)):
		for sent in list_of_items[i]: #sent = ein satz, list_of_items[i] = ein text
			feature_values = []
			feature_values.append(sents_length(sent)) #Satzlaenge
			feature_values.append(counts_ner(sent)) #Anzahl NER geteilt durch Satzlaenge * 100 > Gibt Prozent anwenden
			feature_values.append(modalverb(sent)) #Welches Modalverb
			feature_values.append(mainverb(sent)) #Welches Hauptverb
			feature_values.append(adverb(sent))
			feature_values.append(count_pronomen(sent))
			feature_values.append(count_satzzeichen(sent))
			feature_values.append(keyword_binary_eo(sent))
			feature_values.append(keyword_binary_po(sent))
			feature_values.append(keyword_count_eo(sent))
			feature_values.append(keyword_count_po(sent))
			feature_values.append(iob_eo(sent))
			feature_values.append(iob_po(sent))


			feature_result.append(feature_values)

	print feature_result
			
			#filename_out = re.sub(r"preprocessed", "featuredata", filename_in)
        	#with open(filename_out, "w") as fout:


if __name__ == '__main__':
    main()
