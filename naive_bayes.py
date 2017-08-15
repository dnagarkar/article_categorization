from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import load_files
from decimal import *
import numpy as np
from load_files import load_files_edited

categories = ['hiring', 'fundraising', 'ui_ux', 'performance_management', 'diversity', 'other']
article_list = load_files_edited('train', categories=categories, shuffle=True, encoding='ISO-8859-2', ignore_files=".DS_Store") 

#stopwords
stopwords=['a', 'about', 'above', 'after', 'again', 'all', 'am', 'an', 'and', 
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

test_articles= load_files_edited('test_full', shuffle=True, encoding='ISO-8859-2', ignore_files=".DS_Store")

X_new_counts = count_vect.transform(test_articles.data)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

#predicting
predicted = clf.predict(X_new_tfidf)

#confidence
confidence= clf.predict_proba(X_new_tfidf)
#print confidence

total=0
correct=0

#printing results 
for x in range(0, len(test_articles.filenames)):
	total+=1
	#print('%r => %s' % (test_articles.filenames[x], article_list.target_names[predicted[x]]))
	if(article_list.target_names[predicted[x]] == test_articles.target_names[test_articles.target[x]]):
		correct+=1

print correct
print total






