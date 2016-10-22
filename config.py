import yaml


with open('anime.yml') as fd:
  anime = yaml.load(fd)

anime['settings'] = {}
for group in anime.keys():
    if group == 'settings':
        continue
    settings = anime['settings'].setdefault(group, {})
    settings['from_group'] = group
    settings['quality'] = '720p'
    settings['identified_by'] = 'sequence'


config = '''
templates:
  global:
    make_rss:
      file: ~/public_html/flexget.rss
      days: -1
      items: 100
      title: "{{{{title}}}}"
      template: 'rss'
  anime:
    series: {}

tasks:
  nyaa:
    template: [anime]
    rss: http://www.nyaa.se/?page=rss&cats=1_37&filter=1
    include:
      - twitter.yml
    assume_quality: 720p
    discover:
      what:
        - next_series_episodes:
            from_start: yes
      from:
        - nyaa:
            category: anime eng
            filter: trusted only
      interval: 12 hours
'''

print(config.format(anime))
