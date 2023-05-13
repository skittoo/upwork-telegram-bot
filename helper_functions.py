from urllib.parse import urlparse
import feedparser
import re
from typing import List, Dict


def validate_rss_link(link):
    """Validate it's an Upwork rss url."""
    parsed_link = urlparse(link)
    if ((parsed_link.scheme == 'https') and (parsed_link.netloc == 'www.upwork.com') and ('rss' in parsed_link.path) and (link.count("https") == 1) ):
      return True
    else:
      return False


def parse_job_listing(text: str):
    info_dict = {}
    # Remove HTML tags
    text_no_html = no_html_text(text)
    
    # Extract Budget or Hourly Range
    if "Budget" in text_no_html:
        info_dict['description'] = text_no_html[:text_no_html.find('Budget')] 
        info_dict['price'] =  re.search("Budget: (.*)", text_no_html).group(1)
        info_dict['hourly_range'] = False

    elif "Hourly Range" in text_no_html:
        info_dict['description'] = text_no_html[:text_no_html.find('Hourly Range')]
        info_dict['price'] = re.search("Hourly Range: (.*)", text_no_html).group(1)
        info_dict['hourly_range'] = True

    # Extract Posted On
    info_dict['posted_on'] = re.search("Posted On: (.*) UTC", text_no_html).group(1)

    # Extract Category
    info_dict['category'] = re.search("Category: (.*)", text_no_html).group(1)

    # Extract Skills
    info_dict['skills'] = re.search("Skills:(.*)", text_no_html).group(1)

    # Extract Country
    info_dict['country'] = re.search("Country: (.*)", text_no_html).group(1)

    return info_dict

def no_html_text(text: str):
    # Remove HTML tags
    text_no_html = re.sub("<.*?>", "", text)

    # Replace HTML entities
    text_no_html = text_no_html.replace("&nbsp;", " ")
    text_no_html = text_no_html.replace("&#039;", "'")
    text_no_html = text_no_html.replace("&amp;", "&")
    text_no_html = text_no_html.replace("&lt;", "<")
    text_no_html = text_no_html.replace("&gt;", ">")

    return text_no_html


def is_job_post_exist(job_link: str, all_jobs_info_old: List[Dict]):
    for job_dict in all_jobs_info_old:
        if job_link == job_dict['link']:
            return True
    return False


def parse_rss(rss_url: str, all_jobs_info_old: List[Dict]):
    # Parse rss url.
    feed = feedparser.parse(rss_url)
    # Saving all jobs info.
    all_jobs_info = []
    for entry in feed.entries:
        if is_job_post_exist(entry.link, all_jobs_info_old):
            continue
        info_dict = {}
        info_dict['link'] = entry.link
        info_dict['title'] = entry.title
        # Adding more information to the job post dictionary.
        info_dict.update(parse_job_listing(rss_url))
        all_jobs_info.append(info_dict)

    return all_jobs_info


