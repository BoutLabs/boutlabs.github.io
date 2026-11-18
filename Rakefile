# frozen_string_literal: true

require 'html-proofer'

task :build do
  sh 'bundle exec jekyll build'
end

task :test => :build do
  sh 'python3 _privacy/sync-shared.py --check'

  required = %w[
    _site/privacy/index.html
    _site/herenotes/privacy/index.html
    _site/support/index.html
    _site/support/thanks/index.html
  ]
  required.each do |path|
    abort "missing #{path}" unless File.exist?(path)
  end

  if File.exist?('_site/boutfitness/privacy/index.html') || File.exist?('_site/bootybabez/privacy/index.html')
    abort 'unpublished product privacy stub was built'
  end

  built = Dir.glob('_site/**/*.html')
  ga = built.select do |path|
    html = File.read(path)
    html.match?(/googletagmanager|google-analytics|UA-143690680|gtag\(/)
  end
  abort "Google Analytics markup found:\n#{ga.join("\n")}" unless ga.empty?

  if built.any? { |path| File.read(path).include?('static.cloudflareinsights.com') }
    abort 'Cloudflare beacon rendered; cloudflare_analytics_token should be blank'
  end

  placeholders = required.select do |path|
    html = File.read(path)
    html.include?('[OPEN') || html.include?('⚠') || html.include?('NOT READY')
  end
  abort "placeholder rendered:\n#{placeholders.join("\n")}" unless placeholders.empty?

  thanks = File.read('_site/support/thanks/index.html')
  abort 'support thanks page is missing noindex' unless thanks.include?('name="robots" content="noindex"')

  unless File.read('_site/sitemap.xml').include?('/privacy/') &&
         File.read('_site/sitemap.xml').include?('/herenotes/privacy/') &&
         File.read('_site/sitemap.xml').include?('/support/')
    abort 'sitemap is missing a privacy or support URL'
  end
  if File.read('_site/sitemap.xml').include?('/support/thanks/')
    abort 'support thanks page was added to the sitemap'
  end

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
