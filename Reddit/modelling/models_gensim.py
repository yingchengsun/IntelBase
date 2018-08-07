# -*- coding:utf-8 -*-
'''
Created on Apr 16, 2018

@author: yingc
'''

from gensim import corpora, models, similarities
from pprint import pprint
import matplotlib.pyplot as plt
import math
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
    
import logging

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
            "The EPS user interface management system",
            "System and human system engineering testing of EPS",
            "Relation of user perceived response time to error measurement",
            "The generation of random binary unordered trees",
            "The intersection graph of paths in trees",
            "Graph minors IV Widths of trees and well quasi ordering",
            "Graph minors A survey"]

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

print 'got', len(documents), 'documents'    # got 9 documents
#pprint(documents)

class MyTexts(object):
    """Construct generator to avoid loading all docs
    
    """
    def __init__(self):
        #stop word list
        self.stoplist = set('for a of the and to in'.split())

    def __iter__(self):
        for doc in documents:
            #remove stop words from docs
            stop_free = [i for i in doc.lower().split() if i not in stop]

            punc_free = [ch for ch in stop_free if ch not in exclude]

            normalized = [lemma.lemmatize(word) for word in punc_free]
 
        
            #yield [word for word in doc.lower().split() if word not in stop]
            yield  normalized


def get_dictionary(texts, min_count=1):
    """Construct dictionary 
    
    """
    dictionary = corpora.Dictionary(texts)
    lowfreq_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() 
                    if docfreq < min_count]
    # remove stop words and low frequence words
    dictionary.filter_tokens(lowfreq_ids)
    # remove gaps in id sequence after words that were removed
    dictionary.compactify()
    
    #dictionary.save('docs.dict')
    return dictionary


def corpus2bow(texts,dictionary):
    """represent docs into a list with bag of words model
       bow: bag of words
    
    """
    corpus=[dictionary.doc2bow(text) for text in texts]
    #pprint(corpus)
    
    # save corpus
    #corpora.MmCorpus.serialize('corpus.mm', corpus)
    # load corpus
    #corpus = corpora.MmCorpus('corpus.mm')
    
    return corpus

def bow2tfidf(corpus):
    """represent docs  with TF*IDF model
    
    """
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus] # wrap the old corpus to tfidf
    
    #print tfidf, '\n' # TfidfModel(num_docs=9, num_nnz=51) 
    #print corpus_tfidf, '\n'
    #print tfidf[corpus[0]], '\n' # convert first doc from bow to tfidf
    
    #for doc in corpus_tfidf: # convert the whole corpus on the fly
    #    print doc
    
    return corpus_tfidf
        
def topic_models(corpus_tfidf,dictionary,num_topics=1):
    """modelling the corpus with LDA, LSI and HDP
    
    """
    LDA_model = models.LdaModel(corpus = corpus_tfidf, id2word = dictionary, num_topics=num_topics)
    LDA_model.save('LDA.model')
    LDA_model = models.LdaModel.load('LDA.model')
    
    hdp = models.HdpModel(corpus_tfidf, T=100,id2word=dictionary)
    hdp.save("HDP.model")

    # initialize a fold-in LSI transformation
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics) 

    # create a double wrapper over the original corpus:bow->tfidf->fold-in-lsi
    corpus_lsi = lsi[corpus_tfidf] 

    # save model
    lsi.save('model.lsi')
    # load model
    lsi = models.LsiModel.load('model.lsi')
    
    '''
    nodes = list(corpus_lsi)
    print nodes
    ax0 = [x[0][1] for x in nodes] 
    ax1 = [x[1][1] for x in nodes]
    
    plt.plot(ax0,ax1,'o')
    plt.show()
    '''


def doc_similarity(doc, corpus):

    
    ver_bow=dictionary.doc2bow(doc.lower().split())#return bags-of-word[(tokenid,count)....]
    print(ver_bow)
    
    lsi = models.LsiModel.load('model.lsi')        
    vec_lsi=lsi[ver_bow]
    print(vec_lsi)
    
    index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
    
    sims=index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return (sims)

def perplexity(ldamodel, testset, dictionary, size_dictionary, num_topics):
    """calculate the perplexity of a lda-model
    
    """
    
    # dictionary : {7822:'deferment', 1841:'circuitry',19202:'fabianism'...]
    #print ('the info of this ldamodel: \n')
    print ('num of testset: %s; size_dictionary: %s; num of topics: %s'%(len(testset), size_dictionary, num_topics))
    prep = 0.0
    prob_doc_sum = 0.0
    topic_word_list = [] # store the probablity of topic-word:[(u'business', 0.010020942661849608),(u'family', 0.0088027946271537413)...]
    for topic_id in range(num_topics):
        topic_word = ldamodel.show_topic(topic_id, size_dictionary)
        
        dic = {}
        for word, probability in topic_word:
            dic[word] = probability
        topic_word_list.append(dic)
    doc_topics_ist = [] #store the doc-topic tuples:[(0, 0.0006211180124223594),(1, 0.0006211180124223594),...]
    for doc in testset: 
        #doc_topics_ist.append(ldamodel.get_document_topics(doc, minimum_probability=0))
        doc_topics_ist.append(ldamodel[doc])
    testset_word_num = 0
   
    for i in range(len(testset)):
        prob_doc = 0.0 # the probablity of the doc
        doc = testset[i]
        doc_word_num = 0 # the num of words in the doc
        for word_id, num in doc:
            prob_word = 0.0 # the probablity of the word 
            doc_word_num += num
            word = dictionary[word_id]
            for topic_id in range(num_topics):
                # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                prob_topic = doc_topics_ist[i][topic_id][1]
                prob_topic_word = topic_word_list[topic_id][word]
                prob_word += prob_topic*prob_topic_word
            prob_doc += math.log(prob_word) # p(d) = sum(log(p(w)))
        prob_doc_sum += prob_doc
        testset_word_num += doc_word_num
    prep = math.exp(-prob_doc_sum/testset_word_num) # perplexity = exp(-sum(p(d)/sum(Nd))
    print ("the perplexity of this ldamodel is : %s"%prep)
    return prep

def test_perplexity(testset,num_topics):
    
    ldamodel_path = 'LDA.model'
    dictionary = corpora.Dictionary.load('docs.dict')
    lda_model = models.ldamodel.LdaModel.load(ldamodel_path)
    hdp = models.hdpmodel.HdpModel.load("HDP.model")
    # sample 1/300
    #for i in range(corpus.num_docs/300):
    #    testset.append(corpus[i*300])

    return perplexity(lda_model, testset, dictionary, len(dictionary.keys()), num_topics)
    
if __name__ == '__main__':
    texts = MyTexts()
    '''
    for text in texts:
        print text
    '''
    dictionary = get_dictionary(texts, min_count=2)
    # save and load dictionary
    '''
    dictionary.save('docs.dict')
    dictionary = corpora.Dictionary.load('docs.dict')
    print dictionary
    '''
    corpus = corpus2bow(texts,dictionary)
    corpus_tfidf = bow2tfidf(corpus)
    #doc="Human computer interaction"
    #print doc_similarity(doc, corpus)
    num_topics = 20
    for i in range(1,20):
        topic_models(corpus_tfidf,dictionary,i)
        test_perplexity(corpus_tfidf, i)
    
    
