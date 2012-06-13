# tramtracker -- Real-time tracking of trams in Melbourne, Australia
#
# WebService.py - methods for talking to the SOAP service
#
# Copyright (C) 2009-2010, Danielle Madeley <danielle@madeley.id.au>
# Modifications Copyright (C) 2012-2012, Daniel Hall <daniel@danielhall.me>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from datetime import datetime
import Cache

from suds.xsd.doctor import Import, ImportDoctor
from suds.client import Client

url = 'http://ws.tramtracker.com.au/pidsservice/pids.asmx?wsdl'

parseString = lambda s: s[0] if isinstance(s, list) else s
parseFloat = lambda f: float(parseString(f))
parseBool = lambda b: parseString(b) == 'true'
parseDateTime = lambda d: datetime.strptime(parseString(d).split('.', 1)[0].split('+', 1)[0], '%Y-%m-%dT%H:%M:%S')

def load_request(data, props):
    d = {}

    for prop in props:
        if isinstance(prop, tuple):
            prop, transform = prop
        else:
            transform = parseString

        try:
            d[prop] = transform(getattr(data, prop))
        except Exception, e:
            print "ERROR (prop = %s): %s" % (prop, e)
            continue

    return d

class YarraTrams:
    def __init__(self, **kwargs):
        """Initialise the service. If guid is not provided, one will be
           requested (returned in the callback). Pass callback= or error=
           to receive notification of readiness."""

        self.guid = Cache.read('metricsathome.Data.YarraTrams-guid')

        imp = Import('http://www.w3.org/2001/XMLSchema')
        imp.filter.add('http://www.yarratrams.com.au/pidsservice/')
        doctor = ImportDoctor(imp)

        self.client = Client(url, doctor=doctor)

        if self.guid is None:
            self.guid = self.client.service.GetNewClientGuid()

        Cache.write('metricsathome.Data.YarraTrams-guid', self.guid, 2592000) # Keep for 1 month of no use

        headers = self.client.factory.create('PidsClientHeader')
        headers.ClientGuid = self.guid
        headers.ClientType = 'DASHBOARDWIDGET'
        headers.ClientVersion = '1.0'
        headers.ClientWebServiceVersion = '6.4.0.0'
        self.client.set_options(soapheaders=headers)

    def GetStopsAndRoutesUpdatesSince(self, dateSince=None):
        if dateSince is None: dateSince = datetime(year=2009, month=7, day=8)
        reply = self.client.service.GetStopsAndRoutesUpdatesSince(dateSince)
        try:
            diffgram = reply.GetStopsAndRoutesUpdatesSinceResult.diffgram
	    if diffgram == "": return []
	    stops = diffgram.dsCoreDataChanges.dtStopsChanges
            return map(lambda stop: (stop.StopNo, stop.Action), stops)

        except AttributeError, e:
            if reply.validationResult != "":
                print reply.validationResult
                return []
            else:
                raise e

    def GetStopInformation(self, stopNo):
        reply = self.client.service.GetStopInformation(stopNo)
        try:
            stopinfo = reply.GetStopInformationResult.diffgram[0].DocumentElement[0].StopInformation[0]

            d = load_request(stopinfo, [
                    'FlagStopNo',
                    'StopName',
                    'CityDirection',
                   ('Latitude', parseFloat),
                   ('Longitude', parseFloat),
                    'SuburbName',
                   ('IsCityStop', parseBool),
                   ('HasConnectingBuses', parseBool),
                   ('HasConnectingTrains', parseBool),
                   ('HasConnectingTrams', parseBool),
                    'StopLength',
                   ('IsPlatformStop', parseBool),
                    'Zones',
                ])
            d['StopNo'] = stopNo
            try:
                d['CrossRoad'], d['TravelRoad'] = d['StopName'].split(' & ', 2)
            except ValueError:
                pass
            return d

        except AttributeError, e:
            if reply.validationResult != "":
                print reply.validationResult
                return {}
            else:
                raise e

    def GetNextPredictedRoutesCollection(self, stopNo, routeNo=0, lowFloor=False):
        reply = self.client.service.GetNextPredictedRoutesCollection(stopNo, \
            routeNo, lowFloor)
        try:
            info = reply.GetNextPredictedRoutesCollectionResult.diffgram[0].DocumentElement[0].ToReturn
            return map(lambda tram: load_request(tram, [
                    'InternalRouteNo',
                    'RouteNo',
                    'HeadboardRouteNo',
                    'VehicleNo',
                    'Destination',
                   ('HasDisruption', parseBool),
                   ('IsTTAvailable', parseBool),
                   ('IsLowFloorTram', parseBool),
                   ('AirConditioned', parseBool),
                   ('DisplayAC', parseBool),
                   ('HasSpecialEvent', parseBool),
                    'SpecialEventMessage',
                   ('PredictedArrivalDateTime', parseDateTime),
                   ('RequestDateTime', parseDateTime),
                ]), info)

        except AttributeError, e:
            if reply.validationResult != "":
                print reply.validationResult
                return []
            else:
                raise e

    def GetDestinationsForRoute(self, routeNo):
        reply = self.client.service.GetDestinationsForRoute(routeNo)
        try:
            info = reply.GetDestinationsForRouteResult.diffgram[0].DocumentElement[0].RouteDestinations[0]
            return load_request(info, [
                    'UpDestination',
                    'DownDestination',
                ])

        except AttributeError, e:
            if reply.validationResult != "":
                print reply.validationResult
                return {}
            else:
                raise e

    def GetListOfStopsByRouteNoAndDirection(self, routeNo, isUpDirection):
        reply = self.client.service.GetListOfStopsByRouteNoAndDirection(routeNo,
            isUpDirection)

        print reply

    def GetNextPredictedArrivalTimeAtStopsForTramNo(self, tramNo):
        reply = self.client.service.GetNextPredictedArrivalTimeAtStopsForTramNo(tramNo)

        try:
            info = reply.GetNextPredictedArrivalTimeAtStopsForTramNoResult.diffgram.NewDataSet
            detailsreply = info.TramNoRunDetailsTable
            stopsreply = info.NextPredictedStopsDetailsTable

            details = load_request(detailsreply, [
                    'VehicleNo',
                   ('AtLayover', parseBool),
                   ('Available', parseBool),
                    'RouteNo',
                    'HeadBoardRouteNo',
                   ('Up', parseBool),
                   ('HasSpecialEvent', parseBool),
                   ('HasDisruption', parseBool),
                ])

            stops = map(lambda s: load_request(s, [
                    'StopNo',
                   ('PredictedArrivalDateTime', parseDateTime),
                ]), stopsreply)

            return (details, stops)

        except AttributeError, e:
            if reply.validationResult != "":
                print reply.validationResult
                return ()
            else:
                raise e
