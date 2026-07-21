# frozen_string_literal: true

require 'html-proofer'

task :build do
  sh 'bundle exec jekyll build'
end

task :test => :build do
  # html-proofer 5.x option keys (renamed from 3.x):
  #   empty_alt_ignore → ignore_empty_alt
  #   url_ignore       → ignore_urls
  #   assume_extension → string ('.html' instead of true)
  options = {
    allow_hash_href: true,
    assume_extension: '.html',
    ignore_empty_alt: true,
    ignore_urls: [
      # LinkedIn 999s automated requests against /company/ pages; ignore to
      # avoid spurious failures. See docs/LESSONS.md.
      %r{https?://www\.linkedin\.com/company/boutlabs}
    ],
    swap_urls: {
      # Canonical/OG tags render fully-qualified boutlabs.com URLs (see
      # _includes/head.html). On a not-yet-merged PR, the page's own URL
      # isn't live in production yet, so treating it as an external link
      # 404s. Rewrite our own domain back to a relative path so it's
      # checked against the local _site build instead of a live request.
      %r{^https?://(www\.)?boutlabs\.com} => ''
    }
  }
  HTMLProofer.check_directory('./_site', options).run
end
