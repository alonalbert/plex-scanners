from UfcAgent import UfcAgent
from F1Agent import F1Agent

def Log(str):
  print str

if __name__ == '__main__':
  agent = F1Agent(Log)

  title = 'F1 Extras 12 Italy'
  print title
  print agent.getShowMetadata(title)
  print agent.getSeasonMetadata(title, "2017")
  print agent.getEpisodeMetadata(title, "2017", "1301")

