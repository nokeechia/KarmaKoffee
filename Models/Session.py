# -*- coding: utf-8 -*-

from decimal import Decimal
from Models import Merchant, Customer
from Models.Voucher import Voucher
from random import randint
__author__ = 'Keech'
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import json
from Models import Merchant,Customer,Voucher
from os import path
import os
from settings import APP_ROOT,openYaml, returnMerchantJSON


class Session:

    user = None
    url = ""
    merchants =[]
    campaigns = []

    def __init__(self):
        print(os.path.dirname(os.path.realpath(__file__)))
        print(os.pardir)
        root = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
        print("\n\n***")


    def login(self, client):
        with openYaml() as stream:
          data = yaml.load(stream)['login']
        customerLogin = client.factory.create(data["factory"])
        customerLogin.institutionID = data["institutionID"]
        customerLogin.instrumentType = data["instrumentType"]
        customerLogin.institutionPassword = data["institutionPassword"]
        customerLogin.userProfile = data["userProfile"]
        customerLogin.instrumentNo = data["instrumentNo"]
        customerLogin.password = data['password']
        customerLoginResponse = client.service.customerLogin(customerLogin)
        print(data["institutionPassword"])
        print(customerLoginResponse)
        customer = Customer.Customer(customerLoginResponse.customerLoginOutputs.firstName, customerLoginResponse.customerLoginOutputs.lastName, customerLoginResponse.customerLoginOutputs.email, customerLoginResponse.customerLoginOutputs.internalCustomerNo)
        return customer


    def getMerchants(self, client, b):
        # merchantList = client.factory.create('merchantListParams')
        # with openYaml() as stream:
        #     data = yaml.load(stream)['login']
        # merchantList.institutionID = data["institutionID"]
        # merchantList.institutionPassword = data["institutionPassword"]
        # merchantList.userProfile = data["userProfile"]
        # with openYaml() as stream:
        #     data = yaml.load(stream)['common']
        # merchantList.userProfile = data["responseLanguage"]
        # merchantListResponse = client.service.getMerchantList(merchantList)
        # ms = []
        # print(merchantListResponse)
        # for m in merchantListResponse.merchantListSetList.merchantListSet:
        #     print(m)
        #     print(dir(m))
        #     with openYaml() as stream:
        #         data = yaml.load(stream)['exampleLocations']
        #     locations = list(data.keys())
        #     print(locations)
        #     location = locations[randint(0,5)]
        #     print(location)
        #     lat = data[location].split(",")[0]
        #     print(lat)
        #     lon = data[location].split(",")[1]
        #     #print("%.2f" % float(m.merchantLatitude))
        #     #TODO: issues with equality fixed by removal, as the location for all merchs are empty
        #     #lat = m.merchantLatitude
        #     #lon = m.merchantLongitude
        #     currentMerch = Merchant.Merchant(m.merchantId,m.merchantName, m.merchantLogoThumbnail, lat, lon)
        #     ms.append(currentMerch)
        #return ms
        return returnMerchantJSON()

    def getCampaigns(self, client):
        with openYaml() as stream:
          data = yaml.load(stream)['campaignList']
        campaignList = client.factory.create(data["factory"])
        campaignList.sourceChannel = data["sourceChannel"]
        with openYaml() as stream:
          data = yaml.load(stream)['login']
        campaignList.institutionID = data["institutionID"]
        campaignList.institutionPassword = data["institutionPassword"]
        campaignList.userProfile = data["userProfile"]
        with openYaml() as stream:
            data = yaml.load(stream)['common']
        campaignList.userProfile = data["responseLanguage"]
        campaignListResponse = client.service.getCampaignList(campaignList)
        print(campaignListResponse)
        for c in campaignListResponse.campaignSet.campaignSet:
            print(c)
            print(c.campaignId)

    def createVoucher(self, client):
        with openYaml() as stream:
          data = yaml.load(stream)['voucher']
        voucherReq = client.factory.create(data["factory"])
        voucherReq.sourceChannel = data["sourceChannel"]
        voucherReq.customerInternalNo = data["customerInternalNo"]
        voucherReq.validityMode = data["validityMode"]
        voucherReq.validityDuration = data["validityDuration"]
        voucherReq.itemBarcode = data["itemBarcode"]
        voucherReq.rewardType = data["rewardType"]
        with openYaml() as stream:
          data = yaml.load(stream)['login']
        voucherReq.institutionID = data["institutionID"]
        voucherReq.instrumentType = data["instrumentType"]
        voucherReq.institutionPassword = data["institutionPassword"]
        voucherReq.userProfile = data["userProfile"]
        with openYaml() as stream:
            data = yaml.load(stream)['common']
        voucherReq.userProfile = data["responseLanguage"]
        createVoucherResp = client.service.getvoucher(voucherReq)
        voucher = Voucher.Voucher(createVoucherResp)
        return client.service.getvoucher(voucher)

    def getSalesAdvice(self, client):
        with openYaml() as stream:
          data = yaml.load(stream)['salesadvice']
        salesAdviceReq = client.factory.create(data["factory"])
        with openYaml() as stream:
          data = yaml.load(stream)['login']
        salesAdviceReq.institutionID = data["institutionID"]
        salesAdviceReq.instrumentType = data["instrumentType"]
        salesAdviceReq.institutionPassword = data["institutionPassword"]

if __name__ == "__main__":
    session = Session()
    # session.user = session.login()
    # s = json.dumps(session.user.__dict__)
    # print(s)
    session.merchants = session.getMerchants()
    for m in session.merchants:
        s = json.dumps(m.__dict__)
        print(s)
    #session.campaigns = session.getCampaigns()
