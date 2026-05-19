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
    ]
  }
  HTMLProofer.check_directory('./_site', options).run
end
