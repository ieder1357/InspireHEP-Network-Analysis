from __future__ import division
from collections import defaultdict
import json
import re
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'
from dateutil.parser import parse
from datetime import datetime


# utility functions we will need

def is_bad_publication(publication):
    """Identifies bad publications that should be eliminated
    from the analysis. 
    Returns True if title of  article contains a low quality word or
    publication has no citations, references or authors.
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
    """ Return parsed date.
    If we get an obviously wrong date format, e.g. '02-31-1999'
    return default dummy date
    """
    try:
        return parse(creation_date, default = parse('06-25-2017'))
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
        
def compute_graph(DG, recid_info, line, date_range = None):
    """Computes edges (i,j) for directed graph DG for current publication
    between (citation,publication) and (publication,reference)
    for each citation to publication and reference in publication,
    and builds recid: info dict
    where info = {'authors': , 'num_citations': , pub_date: '}
    """
    publication = json.loads(line)
    if not is_bad_publication(publication) and is_good_date(publication, date_range):
        author = publication['authors']
        coauthor = publication['co-authors']
        recid = publication['recid']
        references = publication['references']
        citations = publication['citations']
        pub_date = fix_parse(publication['creation_date'])
        # let's merge author + coauthor into one entry
        authors = author + coauthor

        # add (citation, publication) edges
        for citation in citations:
            DG.add_edge(citation, recid)
        
        # add (publication, reference) edges
        for reference in references:
            DG.add_edge(recid,reference)

        # and update dict
        # key is recid; 
        # value is info dict 
        # info = {authors: , num_citations: , pub_date: , pr: }
        recid_info[recid]['authors'] = authors
        recid_info[recid]['num_citations'] = len(citations)
        recid_info[recid]['pub_date'] = pub_date
        recid_info[recid]['pr'] = 0.

def make_authors_hist(author_measure, measure_name, constraint_str,  num_entries):
    """Make hist of sorted (author, measure) tuple """

    x_ticks_labels, cumu_measure = zip(*author_measure[:num_entries])

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
    """ Get the normalization function for authors' metric histogram 
    By default norm = 'None' means norm = 1
    otherwise. norm = 1/len(authors)
    metric = PR or num_citations
    """
    if norm: 
        return lambda x: 1/len(x)
    else:
        return lambda x: 1
        
def author_metric_sorted(recid_info, metric = 'pr',norm = None):
    """ return (author, metric) list
    norm = None ->  defaults to normalization of (author, metric) = 1
    """
    var_type = type(recid_info.values()[0][metric]) # get the vartype for dict values
    d = defaultdict(var_type) # key is author, value is measure
    
    for _, info in recid_info.iteritems():
        for author in info['authors']:
            d[author] += info[metric]*get_norm(norm)(info['authors'])

    # and sort from high to low metric
    d_sorted = sorted(d.items(), key = lambda x: x[1], reverse = True)

    return d_sorted

def get_author_pub_dates(recid_info):
    """ return dict
    key is author; value is author's pub_dates
    """
    author_pub_dates = defaultdict(list) # key is author; value is list of pub dates
    
    for recid, info in recid_info.iteritems():
        for author in info['authors']:
            author_pub_dates[author].append(info['pub_date'])
    return author_pub_dates

def get_author_first_pub(recid_info):
    """ return dict
    key is author; value is author's first publication date
    """
    # key is author; value is author's pub's dates
    author_pub_dates = get_author_pub_dates(recid_info)

    author_first_pub = {author: min(pub_dates).year
                        for author, pub_dates in author_pub_dates.iteritems()}
    return author_first_pub

def get_first_pub_year_authors(recid_info):
    """ return dict
    key is year; value is list of authors who published
    first paper in that year
    """
    first_pub_year_authors = defaultdict(list)
    # key is author; value is author's first pub's year
    author_first_pub = get_author_first_pub(recid_info)
    
    for author, year in author_first_pub.iteritems():
        first_pub_year_authors[year].append(author)
    
    return first_pub_year_authors
