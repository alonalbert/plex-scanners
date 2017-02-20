import inspect
from UfcAgent import UfcAgent
import re
from Framework.objects import MetadataSearchResult


def getImage(image):
  if image is None:
    return None
  if image.lower().startswith("http"):
    image = HTTP.Request(image).content
  else:
    image = Resource.Load(image)

  return Proxy.Media(image)


AGENTS = {
  UfcAgent.NAME: UfcAgent(Log),
}

class SportsScannerAgentTVShows(Agent.TV_Shows):
  name = 'Sports Shows'
  languages = [Locale.Language.NoLanguage]

  def search(self, results, media, lang):
    Log("Searching for " + media.title)
    results.Append(MetadataSearchResult(id=media.show, core=None, name=media.show, year=None, lang=lang, score=100))

  def update(self, metadata, media, lang):
    title = media.title
    Log("Updating " + title)
    if title not in AGENTS:
      Log("No match found for " + title)
      return

    agent = AGENTS[title]
    poster = agent.getShowMetadata()['poster']
    metadata.posters[poster] = getImage(poster)

    for season in media.children:
      seasonIndex = season.index
      seasonMetadata = metadata.seasons[seasonIndex]
      poster = agent.getSeasonMetadata(seasonIndex)['poster']
      seasonMetadata.posters[poster] = getImage(poster)

      for episode in season.children:
        episodeIndex = episode.index
        episodeMetadata = seasonMetadata.episodes[episodeIndex]
        data = agent.getEpisodeMetadata(seasonIndex, episodeIndex)
        thumb = data['thumb']
        episodeMetadata.thumbs[thumb] = getImage(thumb)
        episodeMetadata.title = data['title']
        episodeMetadata.summary = data['summary']

    metadata.title = title

