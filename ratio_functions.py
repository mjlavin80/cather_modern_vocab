from random import shuffle
import json

def dictcom_gl_ratio(token_list, dictionary):
    pre = 0
    post = 0
    passed = 0
    total = len(token_list)
    neo = {"neo": 0, 1700:0, 1750:0, 1800:0, 1850:0, 1900:0, 1950:0}

    for token in token_list:
        try:
            year = int(dictionary[token])
            if year < 1100:
                pre += 1
            elif year >= 1100 and year < 1700:
                post +=1
            elif year >= 1700 and year < 1750:
                neo["neo"] += 1
                neo[1700] += 1
            elif year >= 1750 and year < 1800:
                neo["neo"] += 1
                neo[1750] += 1
            elif year >= 1800 and year < 1850:
                neo["neo"] += 1
                neo[1800] += 1
            elif year >= 1850 and year < 1900:
                neo["neo"] += 1
                neo[1850] += 1
            elif year >= 1900 and year < 1950:
                neo["neo"] += 1
                neo[1900] += 1
            elif year >= 1950:
                neo["neo"] += 1
                neo[1950] += 1
        except:
            passed +=1
    neo["total"] = total
    ratio = 1.0*pre/post
    matched = pre+post
    results = (ratio, matched, passed, json.dumps(neo))
    return results

def oed_gl_ratio(token_list, dictionary):
    pre = 0
    post = 0
    passed = 0
    total = len(token_list)
    neo = {"neo": 0, 1700:0, 1750:0, 1800:0, 1850:0, 1900:0, 1950:0}

    for token in token_list:
        try:
            year = int(dictionary[token])
            if year < 1100:
                pre += 1
            elif year >= 1100 and year < 1700:
                post +=1
            elif year >= 1700 and year < 1750:
                neo["neo"] += 1
                neo[1700] += 1
            elif year >= 1750 and year < 1800:
                neo["neo"] += 1
                neo[1750] += 1
            elif year >= 1800 and year < 1850:
                neo["neo"] += 1
                neo[1800] += 1
            elif year >= 1850 and year < 1900:
                neo["neo"] += 1
                neo[1850] += 1
            elif year >= 1900 and year < 1950:
                neo["neo"] += 1
                neo[1900] += 1
            elif year >= 1950:
                neo["neo"] += 1
                neo[1950] += 1
        except:
            passed +=1
    neo["total"] = total
    ratio = 1.0*pre/post
    matched = pre+post
    results = (ratio, matched, passed, json.dumps(neo))
    return results

def neo_counts(token_list, dictionary):
    neo = {}
    years = {}
    for token in token_list:
        try:
            year = int(dictionary[token])
            if year >= 1700:
                try:
                    neo[token] +=1
                except:
                    neo[token] = 1
                    years[token] = year
        except:
            pass
    neo["total"] = len(token_list)
    data = (neo, years)
    return data

def walker_ratio(token_list, dictionary):
    dictionary = dict(dictionary)
    match = 0
    passed = 0
    for token in token_list:
        try:
            in_dict = dictionary[token]
            match += 1
        except:
            passed +=1
    ratio = 1.0*match/len(token_list)
    results = (ratio, match, passed)
    return results

def counts_to_shuffled(tuples):
    #convert to shuffled list
    expanded = []
    for t, c in tuples:
        e = [t for i in range(c)]
        expanded.extend(e)
    shuffle(expanded)
    return expanded

def run_all_ratios(expanded, as_set, oed_dictionary, dictcom_dictionary, walker_dictionary):
    oed_ratio_no_set, oed_matched_no_set, oed_passed_no_set, oed_neo = oed_gl_ratio(expanded, oed_dictionary)
    oed_ratio_set, oed_matched_set, oed_passed_set, oed_neo_set = oed_gl_ratio(as_set, oed_dictionary)
    gl_ratio_no_set, matched_no_set, passed_no_set, neo = dictcom_gl_ratio(expanded, dictcom_dictionary)
    gl_ratio_set, matched_set, passed_set, neo_set = dictcom_gl_ratio(as_set, dictcom_dictionary)
    walker_ratio_no_set, walker_matched_no_set, walker_passed_no_set = walker_ratio(expanded, walker_dictionary)
    walker_ratio_set, walker_matched_set, walker_passed_set = walker_ratio(as_set, walker_dictionary)
    all_results = [oed_ratio_no_set, oed_matched_no_set, oed_passed_no_set, oed_neo, oed_ratio_set, oed_matched_set, oed_passed_set, oed_neo_set, gl_ratio_no_set, matched_no_set, passed_no_set, neo, gl_ratio_set, matched_set, passed_set, neo_set, walker_ratio_no_set, walker_matched_no_set, walker_passed_no_set, walker_ratio_set, walker_matched_set, walker_passed_set]
    return all_results
