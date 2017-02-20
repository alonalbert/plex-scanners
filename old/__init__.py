import inspect
from Framework.objects import MetadataSearchResult

class ShowMetadata(object):
  def getImage(self, name):
    if name is None:
      return None
    if name.lower().startswith("http"):
      return GetResultFromNetwork(name, False)
    else:
      return Resource.Load(name)

  def getShowPoster(self):
    return None

  def getSeasonPosters(self):
    return None
  def getSeasonPoster(self, season):
    posters = self.getSeasonPosters()
    if posters is None:
      return self.getShowPoster()
    if season not in posters:
      return self.getShowPoster()
    return self.getImage(posters[season])

  def getEpisodeThumbs(self):
    return None
  def getEpisodeThumb(self, season, episode):
    thumbs = self.getEpisodeThumbs()
    if thumbs is None:
      return None
    if season not in thumbs:
      return None
    thumbs = thumbs[season]
    if episode >= len(thumbs):
      return None
    return self.getImage(thumbs[episode])

class F1Metadata(ShowMetadata):
  NAME = "Formula 1"

  def getShowPoster(self):
    return self.getImage("http://fc07.deviantart.net/fs71/i/2010/097/8/9/F1_LOGO_2010_Wallpaper_3D_wide_by_rafaelj3d.jpg")
  def getSeasonPosters(self):
    return {
    "2012": "http://images.thecarconnection.com/lrg/mclaren-mp4-27-2012-formula-1-race-car_100380111_l.jpg"
  }

  def getEpisodeThumbs(self):
    return {
      "2012": [
        "Melbourne.png",
        "KualaLumpur.png",
        "Shanghai.png",
        "Sakhir.png",
        "Catalunya.png",
        "MonteCarlo.png",
        "Canada.png",
        "Europe.png",
        "Silverstone.png",
        "Hockenheim.png",
        "Budapest.png",
        "Spa.png",
        "Monza.png",
        "Singapore.png",
        "Suzuka.png",
        "Yeongam.png",
        "NewDelhi.png",
        "YasMarina.png",
        "Austin.png",
        "SaoPaulo.png",
        ]
    }

  def getEpisodeThumb(self, season, episode):
    thumbs = self.getEpisodeThumbs()
    if thumbs is None:
      return None
    if season not in thumbs:
      return None
    thumbs = thumbs[season]
    episode = episode / 100
    if episode >= len(thumbs):
      return None
    return self.getImage(thumbs[episode])


class F1ShowMetadata(ShowMetadata):
  NAME = "The F1 Show"
  def getShowPoster(self):
    return self.getImage("http://tvnewsroom.co.uk/wp-content/uploads/2012/03/Sky-Sports-F1-The-F1-Show-2012-Preview-03-09-20-00-02.jpg")
  def getSeasonPosters(self):
    return {
      "2012": "http://img.metro.co.uk/i/pix/2011/07/29/article-1311947016976-0D37149200000578-777713_636x444.jpg"
    }

class ParisRoubaixMetadata(ShowMetadata):
  NAME="Paris Roubaix"
  def getShowPoster(self):
    return self.getImage("http://www.velowire.com/images/blog/paris-roubaix/2010/affiche_paris_roubaix_2010.jpg")
  def getSeasonPosters(self):
    return {
      "2012": "http://www.retrobike.co.uk/forum/files/roubaix_178.jpg"
    }

class GiroDelTrentinoMetadata(ShowMetadata):
  NAME="Giro del Trentino"
  def getShowPoster(self):
    return self.getImage("http://t2.gstatic.com/images?q=tbn:ANd9GcRk7D8SBK_3x6YA0l1D03_vn2LrlsF1LqqlGOS3WDTIOMOpi70lcg&t=1")

class TourDeFranceMetadata(ShowMetadata):
  NAME="Tour De France"
  def getShowPoster(self):
    return self.getImage("http://sportsun.org/wp-content/uploads/2012/06/tour-symbol1.jpg")

class MotoGPMetadata(ShowMetadata):
  NAME="MotoGP"
  def getShowPoster(self):
    return self.getImage("http://s.pro-gmedia.com/videogamer/media/images/pub/large/motogp_07_logo.jpg")

class GP2Metadata(ShowMetadata):
  NAME="GP2"
  def getShowPoster(self):
    return self.getImage("http://3.bp.blogspot.com/_3XvP_r8UJOo/TJixOMAQSzI/AAAAAAAAAe8/xVTiDFvNrR0/s1600/800px-GP2_Logo.svg_.png")

class WorldTrackCyclingMetadata(ShowMetadata):
  NAME="World Track Cycling"
  def getShowPoster(self):
    return self.getImage("http://www.morethanthegames.co.uk/files/morethanthegames/cycling%20logo.JPG")
  def getSeasonPosters(self):
    return {
      "2012": "http://www4.pictures.gi.zimbio.com/Olympics+Day+7+Cycling+Track+5UL_ZZlcUb9l.jpg"
    }

class WSOPEuropeMetadata(ShowMetadata):
  NAME="World Series of Poker Europe"
  def getShowPoster(self):
    return self.getImage("http://www.wsop.com/images/logos/wsop_chip_europe_logo_lg.gif")
  def getSeasonPosters(self):
    return {
      "2011": "http://www.wsop.com/images/imagestore/flashlarge/may26-wsope-annoucement.jpg"
    }

SHOW_METADATA = {
  F1Metadata.NAME + " Sky": F1Metadata(),
  F1Metadata.NAME + " BBC": F1Metadata(),
  F1ShowMetadata.NAME: F1ShowMetadata(),
  ParisRoubaixMetadata.NAME : ParisRoubaixMetadata(),
  WorldTrackCyclingMetadata.NAME : WorldTrackCyclingMetadata(),
  WSOPEuropeMetadata.NAME : WSOPEuropeMetadata(),
  GiroDelTrentinoMetadata.NAME : GiroDelTrentinoMetadata(),
  MotoGPMetadata.NAME : MotoGPMetadata(),
  GP2Metadata.NAME : GP2Metadata(),
  TourDeFranceMetadata.NAME : TourDeFranceMetadata(),
}

class MySportsAgentTVShows(Agent.TV_Shows):
  name = 'Sports Shows'
  languages = [Locale.Language.NoLanguage]

  def search(self, results, media, lang):
    Log("Searching " + media.title)
    results.Append(MetadataSearchResult(id=media.show, core=None, name=media.show, year=None, lang=lang, score=100))

  def update(self, metadata, media, lang):
    title = media.title
    Log("Updating " + title)
    if title not in SHOW_METADATA:
      Log("No match found for " + title)
      return

    showMetadata = SHOW_METADATA[title]
    poster = showMetadata.getShowPoster()
    if poster is not None:
      metadata.posters["poster"] = Proxy.Media(poster)
    for season in media.children:
      seasonName = season.index
      seasonMetadata = metadata.seasons[seasonName]
      seasonPoster = showMetadata.getSeasonPoster(seasonName)
      if seasonPoster is not None:
        seasonMetadata.posters["poster"] = Proxy.Media(seasonPoster)
      else:
        if poster is not None:
          seasonMetadata.posters["poster"] = Proxy.Media(poster)
      for episode in season.children:
        episodeName = episode.index
        episodePoster = showMetadata.getEpisodeThumb(seasonName, int(episodeName))
        if episodePoster is not None:
          episodeMetadata = seasonMetadata.episodes[episodeName]
          episodeMetadata.thumbs["thumb"] = Proxy.Media(episodePoster)

    metadata.title = title

def GetResultFromNetwork(url, fetchContent=True):
  result = HTTP.Request(url)
  if fetchContent:
    result = result.content

  return result

