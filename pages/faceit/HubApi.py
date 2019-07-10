
import logging
from pages.faceit.FaceitApi import FaceitApi
from pages.utils.errlog import VerifyException
from pages.models import Hub, HubScore, Player, Invites
from datetime import datetime
import json

def printJson(data):
    return(json.dumps(data, indent=2, sort_keys=True))

logger = logging.getLogger(__name__)
logging.basicConfig(filename='applog.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class HubData:
    def __init__(self, id='', game_id='', status='', name='', start_dttm='', finish_dttm=''):
        self.id = id
        self.game_id = game_id
        self.name = name
        self.status = status
        self.start_dttm = start_dttm
        self.finish_dttm = finish_dttm

    def __str__(self):
        return "hub_id={}, game_id={}, hub_name={}, status={}, hub_start_dttm={}, hub_finish_dttm={}".format(self.id,
                                                                                                      self.game_id,
                                                                                                      self.name,
                                                                                                      self.status,
                                                                                                      self.start_dttm,
                                                                                                      self.finish_dttm)
    def getId(self):
        return self.id
    def getGameId(self):
        return self.game_id
    def getName(self):
        return self.name
    def getStatus(self):
        return self.status
    def getStartDttm(self):
        return datetime.utcfromtimestamp(int(self.start_dttm))
    def getFinishDttm(self):
        return datetime.utcfromtimestamp(int(self.finish_dttm))

class HubApi(FaceitApi):

    def __init__(self):
        super().__init__()
        self.hubItems = []

    def collectHubsData(self):
        organizerId = 'ca401c56-55fe-40d9-a89e-ac3db2d1395b'
        if organizerId == '':
            organizerId = self.getOrganizer('organizerioName')

        try:
            respHubs = self.getOrganizerHubs(organizerId).json()['items']
            for respHubItem in respHubs:
                respSeason = self.getHubSeason(respHubItem['hub_id'], 1).json()

                HubDataObj = HubData(id=respHubItem['hub_id'])
                HubDataObj.game_id = respSeason['leaderboard']['game_id']
                HubDataObj.name = respHubItem['name']
                HubDataObj.status = respSeason['leaderboard']['status']
                HubDataObj.start_dttm = respSeason['leaderboard']['start_date']
                HubDataObj.finish_dttm = respSeason['leaderboard']['end_date']

                self.hubItems.append(HubDataObj)

        except (VerifyException, KeyError) as err:
            logger.error(err)

    def collectHubData(self, hubId):
        try:
            respHubs = self.getHub(hubId).json()
            for respHubItem in respHubs:
                respSeason = self.getHubSeason(respHubItem['hub_id'], 1).json()
                HubDataObj = HubData(id=respHubItem['hub_id'])
                HubDataObj.status = respSeason['leaderboard']['status']
                HubDataObj.name = respHubItem['name']
                HubDataObj.start_dttm = respSeason['leaderboard']['start_date']
                HubDataObj.finish_dttm = respSeason['leaderboard']['end_date']

                self.hubItems.append(HubDataObj)

        except (VerifyException, KeyError) as err:
            logger.error(err)

    def saveResponse(self):
        pass
        # for respHub in self.respHubs:
        #     try:
        #         self.updateHub(respHub)
        #     except Hub.DoesNotExist:
        #         self.createHub(respHub)

    def createHub(self):
        pass
        # hubObj = Hub(
        #     status=self.parseStatus(respHub['']),
        #     hub_name=
        # )
