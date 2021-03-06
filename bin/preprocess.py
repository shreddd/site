#!/usr/bin/env python
'''
Create _config.yml used to compile Software Carpentry web site.
'''

import os
import glob
import datetime
import time
from collections import defaultdict
import yaml
from optparse import OptionParser
from util import CONFIG_YML, STANDARD_YML, P_BLOG_EXCERPT, load_info

# Translate two-digit month identifiers into short names.
MONTHS = {
    '01' : 'Jan', '02' : 'Feb', '03' : 'Mar', '04' : 'Apr',
    '05' : 'May', '06' : 'Jun', '07' : 'Jul', '08' : 'Aug',
    '09' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'
}

# Template for recent blog posts.
RECENT_POST = '''\
<h3><a href="{{site.site}}/%(path)s">%(title)s</a></h3>
<div class="row-fluid">
  <span class="span11">
    %(excerpt)s
  </span>
  <span class="span1"></span>
</div>
<div class="row-fluid">
  <span class="span11">Posted %(date)s by %(author)s</span>
  <span class="span1">
    <a href="{{site.site}}/%(path)s">...more</a>
  </span>
</div>
'''

#----------------------------------------

def main():
    '''
    Main driver for regenerating _config.yml for web site.
    This program also creates _includes/recent_blog_posts.html.
    '''

    # Get the standard stuff.
    options, args = parse_args()
    config = load_info(os.curdir, STANDARD_YML)
    config.update({
        'month_names'     : MONTHS,
        'months'          : sorted(MONTHS.keys()),
        'site'            : options.site,
        'timestamp'       : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'today'           : options.today
    })

    # Cache the window size.
    recent_length = config['recent_length']

    # Get information from blog entries.
    config['blog'] = harvest_blog(config)

    # Select those that'll be displayed on the home page, the index page, etc.
    config['blog_recent'] = config['blog'][-recent_length:]
    config['blog_recent'].reverse()

    # Create _includes/recent_blog_posts.html for inclusion in blog index page.
    # This is done programmatically because we want snippets to be rendered properly.
    for post in config['blog_recent']:
        post['excerpt'] = get_blog_excerpt(post['path'])
    write_recent_blog_posts(config['blog_recent'])

    # Organize all posts by year and month.
    blog_lookup, blog_count = organize_blog_entries(config['blog'])
    config['blog_lookup'] = blog_lookup
    config['blog_count'] = blog_count
    config['blog_years'] = sorted(blog_lookup.keys())
    config['blog_years'].reverse()

    # Get information from legacy boot camps.
    config['bootcamps'] = harvest_bootcamps()

    # Select those that'll be displayed on the home page.
    upcoming = [bc for bc in config['bootcamps'] if bc['startdate'] >= config['today']]
    config['bootcamps_upcoming'] = upcoming[:recent_length]

    # Save.
    with open(CONFIG_YML, 'w') as writer:
        yaml.dump(config, writer)

#----------------------------------------

def parse_args():
    '''Parse command-line arguments.'''

    parser = OptionParser()
    parser.add_option('-o', '--output', dest='output', help='output directory')
    parser.add_option('-s', '--site', dest='site', help='site')
    parser.add_option('-t', '--today', dest='today', help='build date',
                      default=datetime.date.today())
    parser.add_option('-v', '--verbose', dest='verbose', help='enable verbose logging',
                      default=False, action='store_true')
    options, args = parser.parse_args()
    return options, args

#----------------------------------------

def harvest_blog(config):
    '''Harvest metadata for all blog entries.'''

    all_meta = []
    for folder in glob.glob('blog/????/??'):
        for post in glob.glob('{0}/*.html'.format(folder)):
            m = harvest_single(post)
            m['folder'] = folder
            m['author'] = config['people'][m['author']]
            m['category'] = [config['category'][c] for c in m['category']]
            all_meta.append(m)

    all_meta.sort(lambda x, y: cmp(x['date'], y['date']) and cmp(x['time'], y['time']))
    return all_meta

#----------------------------------------

def harvest_bootcamps():
    '''Harvest metadata from all boot camp index.html pages.'''
    pages = glob.glob('bootcamps/*/index.html')
    metadata = harvest(pages)
    bootcamps = []
    for f in metadata:
        bootcamps.append(metadata[f])
        bootcamps[-1]['slug'] = f.split('/')[1]
        if 'contact' not in metadata[f]: # FIXME: need to figure out how to handle missing in templates
            metadata[f]['contact'] = None
    bootcamps.sort(lambda x, y: cmp(x['slug'], y['slug']))
    return bootcamps

#----------------------------------------

def harvest(filespec):
    '''
    Get content and metadata from HTML files. Return a single metadata
    dictionary if a single path is given as input, or a dictionary
    mapping filenames to metadata dictionaries if multiple paths are
    given.
    '''

    if isinstance(filespec, basestring):
        return harvest_single(filespec)

    elif isinstance(filespec, list):
        return dict([(f, harvest_single(f)) for f in filespec])

    else:
        assert False, 'Unknown filespec "{0}"'.format(filespec)

#----------------------------------------

def harvest_single(filename):
    '''Harvest metadata from a single file.'''

    with open(filename, 'r') as reader:
        text = reader.read()
        stuff = text.split('---')[1]
        meta_dict = yaml.load(stuff)
        meta_dict['path'] = filename
        return meta_dict

#----------------------------------------

def organize_blog_entries(posts):
    '''Organize blog entries by year and month.'''

    blog_lookup = {}
    blog_count = {}
    for p in posts:
        year = '%4d' % p['date'].year
        month = '%02d' % p['date'].month
        if year not in blog_lookup:
            blog_lookup[year] = dict([(m,list()) for m in MONTHS.keys()])
            blog_count[year] = dict([(m,0) for m in MONTHS.keys()])
        blog_lookup[year][month].append(p)
        blog_count[year][month] += 1
    return blog_lookup, blog_count

#----------------------------------------

def get_blog_excerpt(path):
    '''Get excerpt from blog post for inclusion in blog index page.'''
    with open(path, 'r') as reader:
        temp = reader.read()
        temp = P_BLOG_EXCERPT.search(temp)
        assert temp, 'Blog post {0} lacks excerpt'.format(path)
        return temp.group(1)

#----------------------------------------

def write_recent_blog_posts(posts):
    '''Write out recent blog posts for inclusion in blog index page.'''
    with open('_includes/recent_blog_posts.html', 'w') as writer:
        for p in posts:
            print >> writer, RECENT_POST % p

#----------------------------------------

if __name__ == '__main__':
    main()
