import math
from collections import Counter
import json
import re
import nltk
from nltk.util import ngrams
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction, sentence_bleu
import argparse

# file=open

# def normalize(text):
#     text = text.lower()
#     # insert white space for 's
#     text = insertSpace('\'s', text)
#     # replace it's, does't, you'd ... etc
#     text = re.sub('^\'', '', text)
#     text = re.sub('\'$', '', text)
#     text = re.sub('\'\s', ' ', text)
#     text = re.sub('\s\'', ' ', text)
#     for fromx, tox in replacements:
#         text = ' ' + text + ' '
#         text = text.replace(fromx, tox)[1:-1]


# Compute BLEU score in reference response and generated response in the whole corpus
def parse_decoded_file_for_bleu(file):
    with open(file) as f:
        result = json.load(f)
    
    all_hypothesis = []
    for turn in result:
        hyps = []
        for system_respose in turn:
            hyp = system_respose.split("system : ")[1]
            if hyp in hyps:
                continue
            hyps.append(hyp)
        all_hypothesis.append(hyps)
    return all_hypothesis

def parse_test_file_for_bleu(file):
    with open(file) as f:
        result = json.load(f)

    all_responses = []
    for turn in result:
        response = []
        response_string = turn["reply"].split('system : ')[1]
        response.append(response_string)
        all_responses.append(response)
    return all_responses


class BLEUScorer(object):
    """
    Calculate a single corpus-level BLEU score (aka. system-level BLEU) for all the hypotheses and their 
    respective references.
    Instead of averaging the sentence level BLEU scores (i.e. macro-average precision), the original BLEU
    metric (Papineni et al. 2002) accounts for the micro-average precision (i.e. summing the numerators 
    and denominators for each hypothesis-reference(s) pairs before the division).
    """
    def score(self, hypothesis, corpus, n=1):
        # containers
        count = [0, 0, 0, 0]
        clip_count = [0, 0, 0, 0]
        r = 0
        c = 0
        weights = [0.25, 0.25, 0.25, 0.25]  # weights for 1-gram, 2-gram, 3-gram, 4-gram

        # accumulate ngram statistics
        for hyps, refs in zip(hypothesis, corpus):
            hyps = [hyp.split() for hyp in hyps]
            refs = [ref.split() for ref in refs]

            for idx, hyp in enumerate(hyps):
                for i in range(4):
                    # accumulate ngram counts
                    hypcnts = Counter(ngrams(hyp, i + 1))
                    cnt = sum(hypcnts.values())
                    count[i] += cnt

                    max_counts = {}
                    for ref in refs:
                        refcnts = Counter(ngrams(ref, i + 1))
                        for ng in hypcnts:
                            max_counts[ng] = max(max_counts.get(ng, 0), refcnts[ng])
                    clipcnt = dict((ng, min(count, max_counts[ng])) \
                                   for ng, count in hypcnts.items())
                    clip_count[i] += sum(clipcnt.values())

                # accumulate r & c
                bestmatch = [1000, 1000]
                for ref in refs:
                    if bestmatch[0] == 0: break
                    diff = abs(len(ref) - len(hyp))
                    if diff < bestmatch[0]:
                        bestmatch[0] = diff
                        bestmatch[1] = len(ref)
                r += bestmatch[1]
                c += len(hyp)
                if n == 1:
                    break
        # computing bleu score
        p0 = 1e-7
        bp = 1 if c > r else math.exp(1 - float(r) / float(c))
        p_ns = [float(clip_count[i]) / float(count[i] + p0) + p0 \
                for i in range(4)]
        s = math.fsum(w * math.log(p_n) \
                      for w, p_n in zip(weights, p_ns) if p_n)
        bleu = bp * math.exp(s)
        return bleu


def compute_bleu(decoded_file, test_file):
    hypothesis = parse_decoded_file_for_bleu(decoded_file)
    corpus = parse_test_file_for_bleu(test_file)
    bscorer = BLEUScorer()
    bleu = bscorer.score(hypothesis, corpus)
    return bleu


# For each turn, compare the belief state prediction with the gold belief, and compute accuracy
def parse_decoded_file_for_bs(file):
    with open(file) as f:
        result = json.load(f)

    all_predicted_bs = []
    for turn in result:
        predicted_bs = []   # of each turn
        for system_response in turn:
            system_response = system_response.strip()
            bs = system_response.split('system : ')[0]
            bs = bs.split('belief : ')[1]
            bs = ' '.join(bs.split()[:])    # removes any leading, trailing or consecutive whitespace into a single space
            # bs = bs.split(' ; ')
            bs = re.split(r'\s*;\s*|\s*,\s*', bs)
            bs_state = {}
            for slot_value in bs:
                if '=' in slot_value:
                    s_v = slot_value.split(' = ')
                    if len(s_v) == 2:
                        s, v = s_v
                        s = s.strip()
                        v = v.strip()
                        if v != 'not mentioned' and v != 'dont care' and v != "don't care":   # 'not mentioned' and 'dont care' are not counted
                            bs_state[s] = v
            if bs_state in predicted_bs:
                continue
            predicted_bs.append(bs_state)   # if bs_state already in the list then do not append
        all_predicted_bs.append(predicted_bs)
    return all_predicted_bs


def parse_test_file_for_bs(file):
    with open(file) as f:
        test_data = json.load(f)

    all_gold_bs = []
    for instance in test_data:
        bs = instance['belief'].split('belief : ')[1]
        bs = ' '.join(bs.split()[:])     
        bs = bs.split(';')
        bs_state = {}
        for slot_value in bs:
            if '=' in slot_value:
                s, v = slot_value.split('=')
                v = v.strip()
                if v != 'not mentioned' and v != 'dont care':
                    bs_state[s] = v
        all_gold_bs.append(bs_state)
    return all_gold_bs


def compare(predicted_bs, gold_bs):
    # compute score of each hypothesis
    score = 0
    for s, v in predicted_bs.items():
        if s in gold_bs and v == gold_bs[s]:
            score += 1
    return score


def best_bs(predicted_bs, gold_bs):
    best_score = 0
    best_bs = None
    for bs in predicted_bs:
        score = compare(bs, gold_bs)
        if score > best_score:
            best_score = score
            best_bs = bs
    return best_score, best_bs


def compute_accuracy(decoded_file, test_file):
    all_predicted_bs = parse_decoded_file_for_bs(decoded_file)
    all_gold_bs = parse_test_file_for_bs(test_file)
    total_turns = 0
    sum_of_correct = 0
    for predicted, gold in zip(all_predicted_bs, all_gold_bs):
        best_score_for_predicted, _ = best_bs(predicted, gold)
        counts_from_gold = len(gold.keys())
        score = float(best_score_for_predicted / counts_from_gold)
        sum_of_correct += score
        total_turns += 1
    acc = float(sum_of_correct / total_turns)
    return acc


def compute_accuracy_and_bleu(decoded_file, test_file):
    acc = compute_accuracy(decoded_file, test_file)
    bleu = compute_bleu(decoded_file, test_file)
    print(f'belief acc: {acc}\nbleu: {bleu}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--decoded_file", type=str, help="Path to the decoded file")
    parser.add_argument("--test_file", type=str, help="Path to the test file")
    args = parser.parse_args()

    compute_accuracy_and_bleu(args.decoded_file, args.test_file)