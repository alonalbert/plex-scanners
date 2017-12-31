import inspect
from UfcAgent import UfcAgent
from UfcFightNightAgent import UfcFightNightAgent
from UfcOnFoxAgent import UfcOnFoxAgent
from F1Agent import F1Agent
from WsopAgent import  WsopAgent
from BellatorAgent import BellatorAgent
import re
from Framework.objects import MetadataSearchResult

PAD_THUMBNAIL = '%s://rsz.io/%s?w=500&h=280&mode=pad'


def getImage(image, isThumb=False):
  if image is None:
    return None
  if image.lower().startswith("http"):
    if isThumb:
      i = image.index(':')
      image = PAD_THUMBNAIL % (image[0:i], image[i + 3:])
    image = HTTP.Request(image).content
  else:
    image = Resource.Load(image)

  return Proxy.Media(image)


AGENTS = [
  UfcFightNightAgent(Log),
  UfcOnFoxAgent(Log),
  UfcAgent(Log),
  F1Agent(Log),
  WsopAgent(Log),
  BellatorAgent(Log),
]

class SportsScannerAgentTVShows(Agent.TV_Shows):
  name = 'Sports Shows'
  languages = [Locale.Language.NoLanguage]

  def search(self, results, media, lang):
    Log("Searching for " + media.title)
    results.Append(MetadataSearchResult(id=media.show, core=None, name=media.show, year=None, lang=lang, score=100))

  def update(self, metadata, media, lang):
    title = media.title
    Log("Updating " + title)

    agent = None
    for ag in AGENTS:
      if ag.REGEX.match(title):
        agent = ag
        break
    if agent is None:
      Log("No match found for " + title)
      return

    data = agent.getShowMetadata(title)
    poster = data['poster']
    if poster not in metadata.posters:
      metadata.posters[poster] = getImage(poster)
    if 'background' in data:
      background = data['background']
      if background not in metadata.art:
        metadata.art[background] = getImage(background)

    for season in media.children:
      seasonIndex = season.index
      seasonMetadata = metadata.seasons[seasonIndex]
      poster = agent.getSeasonMetadata(title, seasonIndex)['poster']
      if poster not in seasonMetadata.posters:
        seasonMetadata.posters[poster] = getImage(poster)

      for episode in season.children:
        episodeIndex = episode.index
        episodeMetadata = seasonMetadata.episodes[episodeIndex]
        data = agent.getEpisodeMetadata(title, seasonIndex, episodeIndex)

        if 'thumb' in data:
          thumb = data['thumb']
          if thumb not in episodeMetadata.thumbs:
            episodeMetadata.thumbs[thumb] = getImage(thumb, True)
        if 'title' in data:
          episodeMetadata.title = data['title']
        if 'summary' in data:
          episodeMetadata.summary = data['summary']

    metadata.title = title

