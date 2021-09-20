# frozen_string_literal: true

require 'html-proofer'

task :build do
  sh 'bundle exec jekyll build'
end

task :test => :build do
  options = {
    allow_hash_href: true,
    assume_extension: true,
    url_ignore: [
      /http[s]?:\/\/www.linkedin.com\/company\/boutlabs*/
    ]
  }
  HTMLProofer.check_directory('./_site', options).run
end
