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

#def keywords(item) anzahl normalisieren ueber satzlaenge

def count_pronomen(sent):
	counter = 0
	for token in sent['tokens']:
		if token[3] == 'PRP':
			counter += 1
	return counter


#def is_subject_pronomen???

def count_satzzeichen(sent):
	count_punct = 0
	for token in sent['tokens']:
		if re.search(r'\p', token[1]):
			count_punct += 1
	return count_punct













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
			feature_values.append(count_pronomen(sent))
			feature_values.append(count_satzzeichen(sent))
			feature_result.append(feature_values)

	print feature_result
			
			#filename_out = re.sub(r"preprocessed", "featuredata", filename_in)
        	#with open(filename_out, "w") as fout:


if __name__ == '__main__':
    main()