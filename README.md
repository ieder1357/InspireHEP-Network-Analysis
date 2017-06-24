# InspireHEP Network Analysis
I've been learning about variuos machine learning concepts, and Networks and Graphs amongst them. They are pretty cool! As a fun learning project I perform a network analysis of papers in High Energy Physics (HEP) using PageRank.
HEP is an overall open field. The standard practice is that you post a pre-print of your manuscript on 
Arxiv.org before you submit to a journal. And there is InspireHEP, a site which lets you search for papers (amongst other things) by author name, title, date, etc.

It's often said that academics live and die by the citation sword. In my experience in our field that's very true.
InspireHEP let's you view the accumulated statistics of any author that's published a paper since the 1960's or so.
For instance, this is the InspireHEP entry for Steven Weinberg, a Nobel Prize winner for the formulation of the Standard Model of Particle Physics.

http://inspirehep.net/author/profile/S.Weinberg.1

Certainly an impressive record! He has some 70K+ citations. While certainly the number of citations in Weinberg's case seems correlated with his scientific impact, is this always true?

Feel free to take a look at the iPython notebooks I'm attaching in this repository where I try to answer this question with InspireHEP's papers' metadata. It consists of some 1.2 million papers metadata, dating back to papers from 1962! In this project, I attempt to evaluate the impact of a paper (and an author's collective work) through  the PageRank metric, instead of citation count or h-index (the number of papers H that an author has written which have at least H number of citations).

For now, there are two iPython notebooks and associated text files. They should be viewed in the following order:

1. network_analysis.ipynb: Here I begin to quantiy the importance of a paper through PageRank, as well as basic questions about the PageRank of authors as derived from their papers' PageRank.

2. pagerank_vs_total_citations.ipynb: Here I try to answer the question: Is a paper's PageRank strongly correlated with its total number of citations? Same for authors.

3. For the future. What I would really like to do is to try and quantify the following questions: What papers are the most central? Are there indicators that can help us predict papers and authors with high impact as soon as they are published? I'll keep writing questions as I come up with them. Hopefully I'll come back here and give answers to these questions too ;)

Note: While working on this project I came across this paper https://arxiv.org/pdf/physics/0604130.pdf, which to my knowledge was the first one to apply Google's search algorithm to measure the impact of a publication. They focused on those papers published on the Physical Review journals. That disclaimer aside, all of the work in this repository is my own! 


