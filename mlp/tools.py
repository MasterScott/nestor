"""
author: Thurston Sexton     adapted from: "Modern NLP in Python" NB by Patrick Harrison
http://nbviewer.jupyter.org/github/skipgram/modern-nlp-in-python/blob/master/executable/Modern_NLP_in_Python.ipynb
"""

# import numpy as np
# import pandas as pd
import os
import codecs
import spacy
import itertools as it
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

nlp = spacy.load('en')


def write_to_txt(log_txt_filepath, docs):
    """
    writes NL items in iterable 'docs' to a txt file at 'log_txt_filepath'
    """
    if not os.path.isfile(log_txt_filepath):  # create new file
        description_count = 0
        # create & open a new file in write mode
        with codecs.open(log_txt_filepath, 'w', encoding='utf_8') as log_txt_file:

            # loop through all log descriptions stored in the dataframe
            for description in docs:
                # write the log as a line in the new file
                # use newline characters to delimit original text
                log_txt_file.write(unicode(description) + '\n')
                description_count += 1

        print u'''Text from {:,} maintenence logs
                  written to the new txt file.'''.format(description_count)

    else:  # inform user of existing file
        with codecs.open(log_txt_filepath, encoding='utf_8') as log_txt_file:
            for description_count, line in enumerate(log_txt_file):
                pass

        print u'Text from {:,} maintenence logs in the txt file.'.format(description_count + 1)


def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """

    return token.is_punct or token.is_space


def line_review(filename):
    """
    generator function to read in reviews from the file
    and un-escape the original line breaks in the text
    """

    with codecs.open(filename, encoding='utf_8') as f:
        for log in f:
            log = log.replace('\\n', '\n')
            yield log.replace(' -', '; ')


def lemmatized_sentence_corpus(filename):
    """
    generator function to use spaCy to parse reviews,
    lemmatize the text, and yield sentences
    """

    for parsed_log in nlp.pipe(line_review(filename),
                               batch_size=10000, n_threads=4):

        for sent in parsed_log.sents:
            yield u' '.join([token.lemma_ for token in sent
                             if not punct_space(token)])


def clean_sents(clean_filepath, raw_txt_filepath):
    if not os.path.isfile(clean_filepath):
        print "making new file..."
        with codecs.open(clean_filepath, 'w', encoding='utf_8') as f:
            for sentence in lemmatized_sentence_corpus(raw_txt_filepath):
                f.write(sentence + '\n')


def trigram_docs(raw_txt_filepath, trigram_logs_filepath, data_directory='data'):
    clean_filepath = os.path.join(data_directory,
                                  'clean_sents_all.txt')
    clean_sents(clean_filepath, raw_txt_filepath)
    unigram_sentences = LineSentence(clean_filepath)

    bigram_model = Phrases(unigram_sentences)
    bigram_sentences_filepath = os.path.join(data_directory,
                                             'bigram_sentences_all.txt')
    if not os.path.isfile(bigram_sentences_filepath):
        print "making new file..."
        with codecs.open(bigram_sentences_filepath, 'w', encoding='utf_8') as f:

            for unigram_sentence in unigram_sentences:
                bigram_sentence = u' '.join(bigram_model[unigram_sentence])

                f.write(bigram_sentence + '\n')

    bigram_sentences = LineSentence(bigram_sentences_filepath)
    trigram_model = Phrases(bigram_sentences)
    trigram_sentences_filepath = os.path.join(data_directory,
                                              'trigram_sentences_all.txt')

    if not os.path.isfile(trigram_sentences_filepath):
        print "making new file..."
        with codecs.open(trigram_sentences_filepath, 'w', encoding='utf_8') as f:

            for bigram_sentence in bigram_sentences:
                trigram_sentence = u' '.join(trigram_model[bigram_sentence])

                f.write(trigram_sentence + '\n')
    trigram_sentences = LineSentence(trigram_sentences_filepath)

    if not os.path.isfile(trigram_logs_filepath):
        print "making new file..."
        with codecs.open(trigram_logs_filepath, 'w', encoding='utf_8') as f:

            for parsed_log in nlp.pipe(line_review(raw_txt_filepath),
                                       batch_size=10000, n_threads=4):
                # lemmatize the text, removing punctuation and whitespace
                unigram_log = [token.lemma_ for token in parsed_log
                               if not punct_space(token)]

                # apply the first-order and second-order phrase models
                bigram_log = bigram_model[unigram_log]
                trigram_log = trigram_model[bigram_log]

                # remove any remaining stopwords
                trigram_log = [term for term in trigram_log
                               if term not in spacy.en.STOP_WORDS]

                # write the transformed review as a line in the new file
                trigram_log = u' '.join(trigram_log)
                if len(trigram_log) <= 1:
                    trigram_log = u'NaN'
                    print 'Replacing', trigram_log
                f.write(trigram_log + '\n')


def write_clean_docs(clean_filepath, raw_txt_filepath):
    """
    Creates a lemmatized version of the raw line-wise corpus, with punct., whitespace, and stops removed.
    :param clean_filepath: where the new file should go
    :param raw_txt_filepath: where the original corpus file is
    """
    if not os.path.isfile(clean_filepath):
        print "making new file..."
        with codecs.open(clean_filepath, 'w', encoding='utf_8') as f:
            for parsed_log in nlp.pipe(line_review(raw_txt_filepath),
                                       batch_size=10000, n_threads=4):
                # lemmatize the text, removing punctuation and whitespace
                unigram_log = [token.lemma_ for token in parsed_log
                               if not punct_space(token)]
                # remove any remaining stopwords
                unigram_log = [term for term in unigram_log
                               if term not in spacy.en.STOP_WORDS]
                # write the transformed review as a line in the new file
                unigram_log = u' '.join(unigram_log)
                if len(unigram_log) <= 1:
                    unigram_log = u'NaN'
                    print 'Replacing', unigram_log
                f.write(unigram_log + '\n')
