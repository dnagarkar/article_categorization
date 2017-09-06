from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import load_files
from decimal import *
import numpy as np
from load_files import load_files_edited
from sklearn.externals import joblib

allcategories = ['diversity', 'fundraising', 'hiring', 'other', 'performance_management', 'ui_ux']

def train_naive_bayes():
	article_list = load_files_edited('train', categories=allcategories, encoding='ISO-8859-2', ignore_files=".DS_Store") 

	#stopwords
	stopwords = ['a', 'about', 'above', 'after', 'again', 'all', 'am', 'an', 'and', 
	'any', 'are', 'as','at','be','because','been','before','being','below','between','both', 
	'but','by','cannot','could','did','do','does','doing','down','during','each','few','for', 
	'from','further','had','has','have','having','he','her','here','hers','herself','him', 
	'himself','his','how','i','if','in','into','is','it','its','itself','me','more','most','my', 
	'myself','no','nor','not','of','off','on','once','only','or','other','ought','our''ours', 
	'ourselves','out','over','own','same','she','should','so','some','such','than','that','the', 
	'their','theirs','them','themselves','then','there','these','they','this','those','through', 
	'to','too','under','until','up','very','was','we','were','what','when','where','which','while', 
	'who','whom','why','with','would','you','your','yours','yourself','yourselves']


	#Tokenizing text
	#count_vect = CountVectorizer()
	count_vect = CountVectorizer(stop_words=stopwords)
	X_train_counts = count_vect.fit_transform(article_list.data)

	#From occurrences to frequencies
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


	#training
	clf = MultinomialNB().fit(X_train_tfidf, article_list.target)

	filename = 'naive_bayes_model_verison1.plk'
	dictionary_file_path = 'dictionary_of_words.txt'
	# category_file_path = 'all_categories.txt'
	joblib.dump(clf, filename)
	joblib.dump(count_vect.vocabulary_, dictionary_file_path)


def test_predictions():
	#getting model to predict on
	clf = joblib.load('naive_bayes_model_verison1.plk')
	vocabulary_to_load = joblib.load('dictionary_of_words.txt')

	#loading files that need to be predicted
	test_articles = load_files_edited('test_new', shuffle=True, encoding='ISO-8859-2', ignore_files=".DS_Store")

	count_vect = CountVectorizer(vocabulary=vocabulary_to_load)

	#X_train_counts = count_vect.fit_transform(test_articles.data)

	#From occurrences to frequencies
	tfidf_transformer = TfidfTransformer()
	#X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

	X_new_counts = count_vect.transform(test_articles.data)
	X_new_tfidf = tfidf_transformer.fit_transform(X_new_counts)

	#predicting
	predicted = clf.predict(X_new_tfidf)

	#confidence
	confidence = clf.predict_proba(X_new_tfidf)
	print confidence



	#printing results 
	for x in range(0, len(test_articles.filenames)):
		#print('%r => %s' % (test_articles.filenames[x], article_list.target_names[predicted[x]]))
		print('%r => %s' % (test_articles.filenames[x], allcategories[predicted[x]]))


#train_naive_bayes()
test_predictions()





