source 'https://rubygems.org'

# Jekyll. Bumped from 4.2 → 4.4 in 2026-05; see issue #27.
gem 'jekyll', '~> 4.4'

# Default Jekyll theme — we override _layouts/ where it matters.
gem 'minima', '~> 2.5'

# If you want to use GitHub Pages, remove the 'gem 'jekyll'' above and
# uncomment the line below. To upgrade, run `bundle update github-pages`.
# gem 'github-pages', group: :jekyll_plugins

group :jekyll_plugins do
  gem 'jekyll-feed', '~> 0.17'
  gem 'jekyll-sitemap', '~> 1.4'
end

group :development do
  gem 'html-proofer', '~> 5.0'
  gem 'rake', '~> 13.0'
  gem 'webrick', '~> 1.8'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
install_if -> { RUBY_PLATFORM =~ %r!mingw|mswin|java! } do
  gem 'tzinfo', '~> 2.0'
  gem 'tzinfo-data'
end

# Performance-booster for watching directories on Windows
gem 'wdm', '~> 0.1.0', :install_if => Gem.win_platform?
