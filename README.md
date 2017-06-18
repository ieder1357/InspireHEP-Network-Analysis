# InspireHEP Network Analysis
I perform a network analysis of papers in High Energy Physics (HEP) using PageRank.
HEP is an overall open field. The standard practice is that you post a pre-print of your manuscript on 
Arxiv.org before you submit to a journal. And there is InspireHEP, a site which lets you search for papers (amongst other things) by author name, title, date, etc.

It's often said that academics live and die by the citation sword. In my experience in our field that's very true.
InspireHEP let's you view the accumulated statistics of any author that's published a paper since the 1960's or so.
For instance, this is the InspireHEP entry for Steven Weinberg, a Nobel Prize winner for the formulation of the Standard Model of Particle Physics.

http://inspirehep.net/author/profile/S.Weinberg.1

Certainly an impressive record! He has some 70K+ citations. While certainly the number of citations in Weinberg's case seems correlated with his scientific impact, is this always true?

Feel free to take a look at the iPython notebook I'm attaching in this repository where I try to answer this question with InspireHEP's papers' metadata. In it, I attempt to evaluate the impact of a paper (and an author's collective work) through  the PageRank metric, instead of citation count or h-index (the number of papers H that an author has written which have at least H number of citations).




