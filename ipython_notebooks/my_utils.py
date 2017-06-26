import json
import re
# utility functions we will need

def is_bad_publication(publication):
    """Identifies bad publications that should be eliminated
    from the analysis. Returns True if the title of the article contains a low quality word or
    the publication has no citations, references or authors.
    """
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
    if  bad_re.search(title):
        return True
    if not authors: # lists are 'Truthy'. Empty lists are considered False
        return True
    if not publication['citations']:
        return True
    if not publication['references']:
        return True
    
    return False

def compute_graph(DG,authors_in_recid,citations_by_recid,line):
    """Computes edges (i,j) for directed graph DG for current publication
    between (citation,publication) and (publication,reference)
    for each citation to publication and reference in publication
    """
    publication = json.loads(line)
    if not is_bad_publication(publication):
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

        #citations.append(citations_i)
        #recids.append(recid)
        #authors.append(authors_i)
        authors_in_recid[recid] = authors_i
        citations_by_recid[recid] = len(citations_i)
        
