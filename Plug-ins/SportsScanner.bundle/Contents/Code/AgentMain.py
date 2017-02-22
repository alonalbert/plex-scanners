from UfcAgent import UfcAgent
from F1Agent import F1Agent

def Log(str):
  print str

if __name__ == '__main__':
  agent = F1Agent(Log)

  print agent.getShowMetadata('F1')
  print agent.getSeasonMetadata('F1', "2017")
  print agent.getEpisodeMetadata('F1', "2017", "1311")

