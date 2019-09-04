# future statements for Python 2 compatibility
from __future__ import (
    unicode_literals, division, print_function, absolute_import)

# built in modules
import os
import sys
import datetime
from six.moves import xrange

# installed modules
import spacy
from unidecode import unidecode

# project modules
try:
    import tools
    import load
except ImportError:
    from . import tools
    from . import load

class SOLOR(object):
    def __init__(
            self, solor_fp,
            overlapping_criteria='score', threshold=0.7, window=5,
            similarity_name='jaccard', min_match_length=3,
            verbose=False):

        self.verbose = verbose
        #ontology=['loinc','snomed']
        valid_criteria = {'length', 'score'}
        err_msg = (
            '"{}" is not a valid overlapping_criteria. Choose '
            'between {}'.format(
                overlapping_criteria, ', '.join(valid_criteria)
            )
        )
        assert overlapping_criteria in valid_criteria, err_msg
        self.overlapping_criteria = overlapping_criteria

        valid_similarities = {'dice', 'jaccard', 'cosine', 'overlap'}
        err_msg = ('"{}" is not a valid similarity name. Choose between '
                   '{}'.format(similarity_name, ', '.join(valid_similarities)))
        assert not(valid_similarities in valid_similarities), err_msg
        self.similarity_name = similarity_name

        simstring_lfp = os.path.join(solor_fp,'loinc', 'loinc-simstring.db')
        id_lfp = os.path.join(solor_fp,'loinc', 'loincids.db')#change to id based on if
        simstring_sfp = os.path.join(solor_fp,'snomed', 'snomed-simstring.db')
        id_sfp = os.path.join(solor_fp,'snomed', 'snomedids.db')

        self.valid_punct = load.UNICODE_DASHES
        self.negations = load.NEGATIONS

        self.window = window
        self.ngram_length = 3
        self.threshold = threshold
        self.min_match_length = min_match_length
        self.to_lowercase_flag = os.path.exists(
            os.path.join(solor_fp, 'lowercase.flag')
        )
        self.normalize_unicode_flag = os.path.exists(
            os.path.join(solor_fp, 'normalize-unicode.flag')
        )

        self._info = None

        #self.accepted_semtypes = accepted_semtypes

        self.ss_ldb = tools.SimstringDBReader(
            simstring_lfp, similarity_name, threshold,ont='loinc'
        )
        self.ID_ldb = tools.IDDB(id_lfp)
        self.ss_sdb = tools.SimstringDBReader(
            simstring_sfp, similarity_name, threshold,ont='snomed'
        )
        self.ID_sdb = tools.IDDB(id_sfp)
        self.nlp = spacy.load('en')

    def get_info(self):
        return self.info

    @property
    def info(self):
        # useful for caching of respnses

        if self._info is None:
            self._info = {
                'threshold': self.threshold,
                'similarity_name': self.similarity_name,
                'window': self.window,
                'ngram_length': self.ngram_length,
                'min_match_length': self.min_match_length,
                #'accepted_semtypes': sorted(self.accepted_semtypes),
                'negations': sorted(self.negations),
                'valid_punct': sorted(self.valid_punct)
            }
        return self._info

    def _is_valid_token(self, tok):
        return not(
            tok.is_punct or tok.is_space or
            tok.pos_ == 'ADP' or tok.pos_ == 'DET' or tok.pos_ == 'CONJ'
        )

    def _is_valid_start_token(self, tok):
        return not(
            tok.like_num or
            (self._is_stop_term(tok) and tok.lemma_ not in self.negations) or
            tok.pos_ == 'ADP' or tok.pos_ == 'DET' or tok.pos_ == 'CONJ'
        )

    def _is_stop_term(self, tok):
        return tok.is_stop or tok.lemma_ == 'time'

    def _is_valid_end_token(self, tok):
        return not(
            tok.is_punct or tok.is_space or self._is_stop_term(tok) or
            tok.pos_ == 'ADP' or tok.pos_ == 'DET' or tok.pos_ == 'CONJ'
        )

    def _is_valid_middle_token(self, tok):
        return (
            not(tok.is_punct or tok.is_space) or
            tok.is_bracket or
            tok.text in self.valid_punct
        )

    def _is_longer_than_min(self, span):
        return (span.end_char - span.start_char) >= self.min_match_length

    def _make_ngrams(self, sent):
        sent_length = len(sent)

        # do not include teterminers inside a span
        skip_in_span = {token.i for token in sent if token.pos_ == 'DET'}

        # invalidate a span if it includes any on these  symbols
        invalid_mid_tokens = {
            token.i for token in sent if not self._is_valid_middle_token(token)
        }

        for i in xrange(sent_length):
            tok = sent[i]

            if not self._is_valid_token(tok):
                continue

            # do not consider this token by itself if it is
            # a number or a stopword.
            if self._is_valid_start_token(tok):
                compensate = False
            else:
                compensate = True

            span_end = min(sent_length, i + self.window) + 1

            # we take a shortcut if the token is the last one
            # in the sentence
            if (
                i + 1 == sent_length and            # it's the last token
                self._is_valid_end_token(tok) and   # it's a valid end token
                len(tok) >= self.min_match_length   # it's of miminum length
            ):
                yield(tok.idx, tok.idx + len(tok), tok.text)

            for j in xrange(i + 1, span_end):
                if compensate:
                    compensate = False
                    continue

                if sent[j - 1] in invalid_mid_tokens:
                    break

                if not self._is_valid_end_token(sent[j - 1]):
                    continue

                span = sent[i:j]

                if not self._is_longer_than_min(span):
                    continue

                yield (
                    span.start_char, span.end_char,
                    ''.join(token.text_with_ws for token in span
                            if token.i not in skip_in_span).strip()
                )

    def _get_all_matches(self, ngrams,i):
        matches = []
        if i == 'loinc':
            ss_db=self.ss_ldb
            ID_db=self.ID_ldb
        elif i == 'snomed':
            ss_db=self.ss_sdb
            ID_db=self.ID_sdb

        for start, end, ngram in ngrams:
            ngram_normalized = ngram

            if self.normalize_unicode_flag:
                ngram_normalized = unidecode(ngram_normalized)

            # make it lowercase
            if self.to_lowercase_flag:
                ngram_normalized = ngram_normalized.lower()

            # if the term is all uppercase, it might be the case that
            # no match is found; so we convert to lowercase;
            # however, this is never needed if the string is lowercased
            # in the step above
            if not self.to_lowercase_flag and ngram_normalized.isupper():
                ngram_normalized = ngram_normalized.lower()

            prev_cui = None
            ngram_cands = list(ss_db.get(ngram_normalized))

            ngram_matches = []

            for match in ngram_cands:
                cuisem_match = sorted(ID_db.get(match))

                for cui in cuisem_match:
                    match_similarity = tools.get_similarity(
                        x=ngram_normalized,
                        y=match,
                        n=self.ngram_length,
                        similarity_name=self.similarity_name
                    )
                    if prev_cui is not None and prev_cui == cui:
                        if match_similarity > ngram_matches[-1]['similarity']:
                            ngram_matches.pop(-1)
                        else:
                            continue

                    prev_cui = cui

                    ngram_matches.append(
                        {
                            'start': start,
                            'end': end,
                            'ngram': ngram,
                            'term': tools.safe_unicode(match),
                            'id': cui,
                            'similarity': match_similarity,
                            #'semtypes': semtypes,
                            #'preferred': preferred
                        }
                    )

            if len(ngram_matches) > 0:
                matches.append(
                    sorted(
                        ngram_matches,
                        key=lambda m: m['similarity'] ,
                        reverse=True
                    )
                )
        return matches

    @staticmethod
    def _select_score(match):
        return (match[0]['similarity'], (match[0]['end'] - match[0]['start']))

    @staticmethod
    def _select_longest(match):
        return (match[0]['similarity'], (match[0]['end'] - match[0]['start']))

    def _select_terms(self, matches):
        sort_func = (
            self._select_longest if self.overlapping_criteria == 'length'
            else self._select_score
        )

        matches = sorted(matches, key=sort_func, reverse=True)

        intervals = tools.Intervals()
        final_matches_subset = []

        for match in matches:
            match_interval = (match[0]['start'], match[0]['end'])
            if match_interval not in intervals:
                final_matches_subset.append(match)
                intervals.append(match_interval)

        return final_matches_subset

    def _make_token_sequences(self, parsed):
        for i in range(len(parsed)):
            for j in xrange(
                    i + 1, min(i + self.window, len(parsed)) + 1):
                span = parsed[i:j]
                yield (span.start_char, span.end_char, span.text)

    def _print_verbose_status(self, parsed, matches):
        if not self.verbose:
            return False

        print(
            '[{}] {:,} extracted from {:,} tokens'.format(
                datetime.datetime.now().isoformat(),
                sum(len(match_group) for match_group in matches),
                len(parsed)
            ),
            file=sys.stderr
        )
        return True

    def match(self, text,i, best_match=True, ignore_syntax=False):
        parsed = self.nlp(u'{}'.format(text))


        if ignore_syntax:
            ngrams = self._make_token_sequences(parsed)
        else:
            ngrams = self._make_ngrams(parsed)#creates start end and ngram to match


        matches = self._get_all_matches(ngrams,i)#this matches with sim and leveldb to extract

        if best_match:
            matches = self._select_terms(matches)

        self._print_verbose_status(parsed, matches)

        return matches
