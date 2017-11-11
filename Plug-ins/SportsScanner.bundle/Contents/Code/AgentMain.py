from UfcAgent import UfcAgent
from UfcFightNightAgent import UfcFightNightAgent
from F1Agent import F1Agent
from WsopAgent import  WsopAgent

def Log(str):
  print str

if __name__ == '__main__':
  agent = UfcFightNightAgent(Log)

  title = '1911'
  print title
  print agent.getShowMetadata(title)
  print agent.getSeasonMetadata(title, "2017")
  print agent.getEpisodeMetadata(title, "2017", "1911")

