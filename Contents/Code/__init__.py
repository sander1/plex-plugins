MMP_ROOT = 'http://minimalmovieposters.tumblr.com'
MMP_JSON = '%s/tagged/%%s' % MMP_ROOT

####################################################################################################
def Start():

	HTTP.CacheTime = CACHE_1WEEK

####################################################################################################
class MMPAgent(Agent.Movies):

	name = 'Minimal Movie Posters'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):

		results.Append(MetadataSearchResult(
			id = media.primary_metadata.id,
			score = 100
		))

	def update(self, metadata, media, lang):

		i = 0
		valid_names = list()

		html = HTML.ElementFromURL(MMP_JSON % (String.Quote(media.title, usePlus=True)))
		posters = html.xpath('//div[@class="post"]/div[@class="photo"]/a[@class="zoom"]/@href')

		for url in posters:

			valid_names.append(url)

			if url not in metadata.posters:

				try:
					i += 1
					metadata.posters[url] = Proxy.Preview(HTTP.Request(url, sleep=0.5).content, sort_order=i)
				except:
					pass

		metadata.posters.validate_keys(valid_names)