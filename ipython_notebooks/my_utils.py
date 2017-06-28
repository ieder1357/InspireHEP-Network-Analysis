from __future__ import division
from collections import defaultdict
import json
import re
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'
from dateutil.parser import parse


# utility functions we will need

def is_bad_publication(publication):
    """Identifies bad publications that should be eliminated
    from the analysis. Returns True if the title of the article contains a low quality word or
    the publication has no citations, references or authors.
    """
    # merge authors and co-authors into one
    authors = publication['authors'] + publication['co-authors']

    bad_title_strings = [
        'proceedings',
        'proceeding',
        'withdrawn',
        'thesis',
        'conference',
        'canceled',
        'cancelled'
    ]
    bad_re = re.compile('|'.join(bad_title_strings)) 
    title = publication['title'].lower()
    if  bad_re.search(title): # reject any paper if keyword in title
        return True
    if not authors: # lists are 'Truthy'. Empty lists are considered False
        return True
    if not publication['citations']: # reject papers with 0 citations
        return True
    if not publication['references']: # reject papers with 0 references
        return True
    
    return False

def fix_parse(creation_date):
    """ return parsed date.
    If we get an obviously wrong date format, e.g. '02-31-1999'
    return a default dummy date
    """
    try:
        return parse(creation_date)
    except:
        return parse('01-01-1900')

def is_good_date(publication, date_range):
    """ 
    return True if publication falls within date range
    """
    if date_range: # apply date range cut
        pub_date = fix_parse(publication['creation_date'])
        min_date = parse(date_range[0]) # lower end of date range
        max_date = parse(date_range[1]) # higher end of date range
        return ((pub_date > min_date) and (pub_date < max_date))
        
    else: # if date_range = None, don't apply time range cut
        return True
        
def compute_graph(DG, recid_authors, recid_citations, line, date_range = None):
    """Computes edges (i,j) for directed graph DG for current publication
    between (citation,publication) and (publication,reference)
    for each citation to publication and reference in publication
    """
    publication = json.loads(line)
    if not is_bad_publication(publication) and is_good_date(publication, date_range):
        author = publication['authors']
        coauthor = publication['co-authors']
        recid = publication['recid']
        references = publication['references']
        citations = publication['citations']
        authors = author + coauthor # let's merge author + coauthor into one entry

        # add (citation, publication) edges
        for citation in citations:
            DG.add_edge(citation, recid)
        
        # add (publication, reference) edges
        for reference in references:
            DG.add_edge(recid,reference)

        recid_authors[recid] = authors
        recid_citations[recid] = len(citations)

def make_hist_by_author(author_measure, measure_name, constraint_str,  num_entries):
    """Make hist of sorted (author, measure) tuple """

    x_ticks_labels, cumu_measure = zip(*author_measure[:num_entries]) # pythonic

    x = range(num_entries)

    plt.bar(x, cumu_measure)
    plt.ylabel('Cumulative '+measure_name)
    plt.xlabel("Author")
    title = 'Cumulative ' + measure_name + ' by Author (' + constraint_str + ')'
    plt.title(title)
    plt.xticks([i+0.5 for i, _ in enumerate(cumu_measure)],
               x_ticks_labels,
               rotation='vertical')

def get_norm(norm):
    """ Get the normalization function for measure by author  histogram 
    By default norm = 'None' means norm = 1
    otherwise. norm = 1/len(authors)
    """
    if norm: 
        return lambda x: 1/len(x)
    else:
        return lambda x: 1
        
def author_measure_dict(recid_authors, recid_measure, norm = None):
    """ return { author: measure } defaultdict
    norm = None defaults to normalization of (author, measure) = 1
    """
    var_type = type(recid_measure.values()[0]) # get the vartype for dict values
    d = defaultdict(var_type) # key is author, value is measure
    
    for recid, authors in recid_authors.iteritems():
        for author in authors:
            d[author] += recid_measure[recid]*get_norm(norm)(authors)
    
    return d

