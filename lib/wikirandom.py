# wikirandom.py: Functions for downloading random articles from Wikipedia
#
# Copyright (C) 2010  Matthew D. Hoffman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, urllib.request, urllib.error, urllib.parse, re, string, time, threading

def get_random_wikipedia_article():
	"""
	Downloads a randomly selected Wikipedia article (via
	http://en.wikipedia.org/wiki/Special:Random) and strips out (most
	of) the formatting, links, etc.

	This function is a bit simpler and less robust than the code that
	was used for the experiments in "Online VB for LDA."
	"""
	failed = True
	while failed:
		article_title = None
		failed = False
		try:
			req = urllib.request.Request('http://en.wikipedia.org/wiki/Special:Random',
								  None, { 'User-Agent' : 'x'})
			f = urllib.request.urlopen(req)
			while not article_title:
				line = f.readline()
				result = re.search(r'title="Edit this page" href="/w/index.php\?title=(.*)\&amp;action=edit" /\>', line)
				if result:
					article_title = result.group(1)
					break
				elif len(line) < 1:
					sys.exit(1)

			req = urllib.request.Request('http://en.wikipedia.org/w/index.php?title=Special:Export/%s&action=submit' \
									  % article_title,
								  None, { 'User-Agent' : 'x'})
			f = urllib.request.urlopen(req)
			all = f.read()
		except (urllib.error.HTTPError, urllib.error.URLError):
			print('oops. there was a failure downloading %s. retrying...' \
				% article_title)
			failed = True
			continue
		print('downloaded %s. parsing...' % article_title)

		try:
			all = re.search(r'<text.*?>(.*)</text', all, flags=re.DOTALL).group(1)
			all = re.sub(r'\n', ' ', all)
			all = re.sub(r'\{\{.*?\}\}', r'', all)
			all = re.sub(r'\[\[Category:.*', '', all)
			all = re.sub(r'==\s*[Ss]ource\s*==.*', '', all)
			all = re.sub(r'==\s*[Rr]eferences\s*==.*', '', all)
			all = re.sub(r'==\s*[Ee]xternal [Ll]inks\s*==.*', '', all)
			all = re.sub(r'==\s*[Ee]xternal [Ll]inks and [Rr]eferences==\s*', '', all)
			all = re.sub(r'==\s*[Ss]ee [Aa]lso\s*==.*', '', all)
			all = re.sub(r'http://[^\s]*', '', all)
			all = re.sub(r'\[\[Image:.*?\]\]', '', all)
			all = re.sub(r'Image:.*?\|', '', all)
			all = re.sub(r'\[\[.*?\|*([^\|]*?)\]\]', r'\1', all)
			all = re.sub(r'\&lt;.*?&gt;', '', all)
		except:
			# Something went wrong, try again. (This is bad coding practice.)
			print('oops. there was a failure parsing %s. retrying...' \
				% article_title)
			failed = True
			continue

	return(all, article_title)

class WikiThread(threading.Thread):
	articles = list()
	article_names = list()
	lock = threading.Lock()

	def run(self):
		(article, article_name) = get_random_wikipedia_article()
		WikiThread.lock.acquire()
		WikiThread.articles.append(article)
		WikiThread.articlenames.append(article_name)
		WikiThread.lock.release()

def get_random_wikipedia_articles(n):
	"""
	Downloads n articles in parallel from Wikipedia and returns lists
	of their names and contents. Much faster than calling
	get_random_wikipedia_article() serially.
	"""
	max_threads = 8
	WikiThread.articles = list()
	WikiThread.article_names = list()
	wt_list = list()
	for i in range(0, n, max_threads):
		print('downloaded %d/%d articles...' % (i, n))
		for j in range(i, min(i+max_threads, n)):
			wt_list.append(WikiThread())
			wt_list[len(wt_list)-1].start()
		for j in range(i, min(i+max_threads, n)):
			wt_list[j].join()
	return WikiThread.articles, WikiThread.article_names

if __name__ == '__main__':
	t0 = time.time()

	(articles, article_names) = get_random_wikipedia_articles(100000)
	for i in range(0, len(articles)):
		print(article_names[i])
		file_h = open (article_names[i], 'w' )
		file_h.write (articles[i])
		file_h.close()
		t1 = time.time()
		print('took %f' % (t1 - t0))

