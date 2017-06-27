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
        
def compute_graph(DG, authors_by_recid, citations_by_recid, line, date_range = None):
    """Computes edges (i,j) for directed graph DG for current publication
    between (citation,publication) and (publication,reference)
    for each citation to publication and reference in publication
    """
    publication = json.loads(line)
    if not is_bad_publication(publication) and is_good_date(publication, date_range):
        author = publication['authors']
        coauthor = publication['co-authors']
        recid = publication['recid']
        references_i = publication['references']
        citations_i = publication['citations']
        authors_i = author + coauthor # let's merge author + coauthor into one entry

        # add (citation_i, publication) edges
        for citation_i in citations_i:
            DG.add_edge(citation_i, recid)
        
        # add (publication, reference_i) edges
        for reference_i in references_i:
            DG.add_edge(recid,reference_i)

        authors_by_recid[recid] = authors_i
        citations_by_recid[recid] = len(citations_i)

def make_hist_by_author(measure_by_author, measure_name, constraint_str,  num_entries):
    """Make hist of sorted measure tuple by author """
    cumu_measure = [x_i 
                    for _, x_i in measure_by_author[:num_entries]]

    x_ticks_labels = [author_i 
                      for author_i, _ in measure_by_author[:num_entries]]

    x = range(num_entries)

    plt.bar(x, cumu_measure)
    plt.ylabel('Cumulative '+measure_name)
    plt.xlabel("Author")
    title = 'Cumulative ' + measure_name + ' by Author (' + constraint_str + ')'
    plt.title(title)
    plt.xticks([i+0.5 for i,_ in enumerate(cumu_measure)],
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
        
def measure_by_author_dict(authors_by_recid, measure_by_recid, norm = None):
    """ return { author: measure } defaultdict
    norm = None defaults to normalization of measure by author = 1
    """
    var_type = type(measure_by_recid.values()[0]) # get the vartype for dict values
    d = defaultdict(var_type) # key is author, value is measure
    
    for recid_i, authors_i in authors_by_recid.iteritems():
        for author_i in authors_i:
            d[author_i] += measure_by_recid[recid_i]*get_norm(norm)(authors_i)
    
    return d

