import requests
import json
import pandas as pd
import sys

pd.set_option('display.max_columns', None)

url = 'http://product2.costar.com/pds/leaseComp/result/list/leaseComps'

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-length': '766',
    'content-type': 'application/json',
    'cookie': '_ga=GA1.2.1157218591.1614929435; _fbp=fb.1.1614929434950.758332580; '
              '__gads=ID=392ca57afd615c4b:T=1614929435:S=ALNI_MaiYlxnjIdlEPsBSHVDa3CzS4jz_w; '
              '_gid=GA1.2.2001130744.1615579889; gudhhv=00834C37293EEAA73A282629E1F76790; '
              'cs_newsContext=%7B%22topic%22%3A0%2C%22cultureCode%22%3A%22en-GB%22%2C%22countryCode%22%3A%22USA%22%2C'
              '%22marketId%22%3A%2264%22%2C%22isCoStarProductUser%22%3Atrue%7D; iBrowserWidth=1440; '
              'iBrowserHeight=658; selectedCulture=en-US; csgwprddc=01; GatewaySessionId=qacfrzeo4v0l2dk50ykc3gg2; '
              'is_toc=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSIsImtpZCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSJ9.eyJpc3MiOiJodHRwczovL3NlY3VyZS5jb3N0YXJncm91cC5jb20iLCJhdWQiOiJvbGRfc3VpdGUiLCJleHAiOjE2MTU2MDk5MTQsIm5iZiI6MTYxNTYwOTYxNCwibm9uY2UiOiJlZjdjNDY0MDdkYzE0ZWQ2OGVmM2JhYzQwMWE1OWNkYiIsImlhdCI6MTYxNTYwOTYxNCwic2lkIjoiZWY1ZmNhZTAzNzc1NjMzMTI3Yjg0YTJkOTRlN2Y5MGEiLCJzdWIiOiJjNTM1YTBlNi0xNzkwLTQ1ZGYtZTc0Zi0wMDAwMDE3NDQ2MjUiLCJjb250YWN0X2lkIjoiMTAzNTUwNDcxIiwic2Vzc2lvbl9pZCI6ImZjODhlMzhhYzZjZTQ1NjdiNTkyNjBkY2FjM2U1NjdiIiwiYXV0aF90aW1lIjoxNjE1NjA5NjEzLCJpZHAiOiJpZHNydiIsImFtciI6WyJwd2QiXX0.gDLb_26g8labt8N28a0RlqHvth5a4_dxYgpc4PmmGraItgL5gdEEgTbm0W3yjJoCwB2ZbaSJKQcGropE-FTcYP0Ilq5PvfXiOgstXL8sZLP2LYeTxgeFBGTSs_Hgcq-WWeiXKbxZdXiSLMbDPnxMDrgrhr6dO4MU8cnWzzDUBuJWz3FNPKwa_zW8YAVYHJrmlVKWFxNu7yv7cVd_Gx46qbGfPMlQczP7-jYrkjJrjG3WJLoqKqryxA-FQ-P91Hc0a3RW4qZyXqO9NLB6bJLJDcAg1YY0Bk9bHtiJ-99uhhSy-U27E2JkXHSFt5gqcGYK8PBytl2cgeFdVjiXcyDlKw; is_sid=ef5fcae03775633127b84a2d94e7f90a; CostarAuthCookie=UserID=149E05C24A5BDFAC0F9B24209A85E45A&UserName=559F852FEA3F4D0C9756E6441EBA38FE&Ticket=7DAF58D314A3F0B38C3699D5F9B6CFD75F0A685E2675D2E351F03C3B6E6B337D&SuperUser=282E05F1E57DA22BCFA2FE565455B994; pce=C=4A03254E24879B07139FAF01BCA8EB76&S=2897596B1C4E198391129CE9965A7B68E7CCE63DF402CAEC897755A510C47BFD40BC46F0B57CBFDC5A85432985BCDC4F&A=7F93FD7EB62178316FA1531E3F9B05EC32A6FC181DF97E4570CB651A3795AC362A947C7C535717C1CA682E3C7C7B9657&SU=EED6DB59459981AC52A01FBDE1AE992D530F9D2E627B347B925109C1B89D443884A0507CA93DD55E07E97A1B9B26B4A4; CostarProductCookiePOR=AD7B801FFC12CFF2950D203A038F5E30; UI=149E05C24A5BDFAC0F9B24209A85E45A; PrefMkt=USA; UserID=149E05C24A5BDFAC0F9B24209A85E45A; UserEmail=94FAC0C94A14D999C72B8D39F186C35F4F34CF6EA93D56B1FD18DEB5C73DEB36; ak_bmsc=252317097329C30E6C5C03E618F74BB56011A8250A410000143F4C603D300158~plV9mjjEI94GCrmXLblzq5Sep4S539WFqlX8Bn21pOoWINPfD3h+8JRmxxmv6AXc49Sh1O+YPvaMJcg3iJnZvOqLwefO6hkNHwpuPNWPtRdswWZBBXvYsJVo44V8rK4dwN7KkkfkmfIlUED5/MfU1H6dvuMB4aM40HOrF9liuuOBHpRZe+qvi9hy2vxkT3ldjp+xBik6+JNBc18NI5N3joYElHamkGFpWPXEkAXWy9Pe18BEc/FCJgYx/USBAJGuGB; bm_sv=17A62513C2F51D67E562986C132032B0~3v1T15iAe0EfK28OHD/eNus4gGBtIAYfnbAyqgQEMnHWsDWvCRceWDCEOLDMS7bk8WN1mHJjvXHjCA4i7vSd4Bvu4CjMnFmb1ECTziqNVg+65pnombDvL5kA4yStnrMdQp4bF8vMlZ8FM4lKFrgFU0HoBzCenSwe3KbvfzcFbv8=; ASP.NET_SessionId=lbbosfbtftzqkvdaxmxyat4n; CostarProductCookie=4F76F9A33C706845BA46458B178F2454; CostarProductCookieLCP=4F76F9A33C706845BA46458B178F2454; _ga=GA1.3.1157218591.1614929435; _gid=GA1.3.2001130744.1615579889; _gat_CSSuite=1; _gat_UA-60737648-3=1'.encode(
        'utf-8'),
    'culture-code': 'en-US',
    'origin': 'https://product1.costar.com',
    'pragma': 'no-cache',
    'referer': 'https://product2.costar.com/LeaseComps/Results/Index/',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36',
    'x-costar-product': '4F76F9A33C706845BA46458B178F2454',
    'x-requested-with': 'XMLHttpRequest'
}


def create_payload(num):
    data = {
        "SearchCriteria": {
            "Lease": {
                "LeaseDeal": {
                    "ExcludeSuppressedLeaseComp": 'true',
                    "AreaOccupied": {
                        "Minimum": {
                            "Value": '6000',
                            "Code": "[sft_i]"
                        }
                    }
                }
            },
            "BoundingBox": {
                "UpperLeft": {
                    "Latitude": '43.121665978055354',
                    "Longitude": '-90.49007063906251'
                },
                "LowerRight": {
                    "Latitude": '40.267613202549214',
                    "Longitude": '-85.38142806093751'
                }
            },
            "Resolution": {
                "MapHeight": '696',
                "MapWidth": '930'
            },
            "Geography": {
                "CountryCode": "US",
                "Filter": {
                    "Ids": [
                        '16980'
                    ],
                    "FilterType": '18',
                    "AdditionalData": [
                        {
                            "metroAreaId": '16980',
                            "metroAreaName": "Chicago - IL",
                            "metroAreaType": '7',
                            "boundingBox": {
                                "upperLeftLatitude": '42.669906',
                                "upperLeftLongitude": '-88.9421468',
                                "lowerRightLatitude": '40.73651',
                                "lowerRightLongitude": '-86.9293519'
                            }
                        }
                    ]
                }
            },
            "SearchGuid": "bb37b22b-c8c5-4dcc-8c14-d94b34cf0bd3"
        },
        "SortOptions": {
            "Items": {
            }
        },
        "PageSize": '100',
        "PageNumber": f'{num}'
    }
    return data


column_names = ['Sign Date', 'Start Date', 'Address', 'City', 'Floor', 'SF Leased', 'Rent/SF/Yr', 'Services', 'Rent '
                                                                                                              'Type',
                'Use', 'Lease Type', 'Tenant', 'Term', 'Exp Date', 'Lease Status', 'Deal Type', 'Move-in Date',
                'Mos on Mrkt', 'Free Rent', 'Suite', 'Leasing Rep Company', 'Leasing Rep Contact', 'Submarket',
                'Tenant Rep Contact', 'Tenant Rep Company', 'Lease Comp ID', 'Zip Code', 'Verified', 'Useable SF',
                'Tenant NAICS', 'Tenant Contact', 'TI Allowance', 'SF Office in Unit', 'Lease Source']
df = pd.DataFrame(columns=column_names)

for page in range(451):
    response = requests.post(url, headers=headers, data=json.dumps(create_payload(page + 1)))
    if response.status_code != 200:
        print('Response code != 200. Check headers and payload.')
        sys.exit(0)
    page_dict = json.loads(response.text)
    print(f'Scraping page #{page + 1}')
    for row in range(len(page_dict['Items'])):
        row_dict = {
            'Sign Date': page_dict['Items'][row]['SignDate']['DisplayValue'],
            'Start Date': page_dict['Items'][row]['StartDate']['DisplayValue'] if page_dict['Items'][row][
                'StartDate'] else '',
            'Address': page_dict['Items'][row]['Address']['DeliveryAddress'],
            'City': page_dict['Items'][row]['Address']['Locality'],
            'Floor': page_dict['Items'][row]['Floor'],
            'Zip Code': page_dict['Items'][row]['Address']['PostalCode'],
            'SF Leased': page_dict['Items'][row]['AreaLeased']['DisplayValue'],
            'Rent/SF/Yr': page_dict['Items'][row]['AskingRent']['DisplayValue'] if page_dict['Items'][row][
                'AskingRent'] else '',
            'Services': page_dict['Items'][row]['Services'],
            'Rent Type': page_dict['Items'][row]['RentType'],
            'Use': page_dict['Items'][row]['RentType'],
            'Lease Type': page_dict['Items'][row]['LeaseType'],
            'Tenant': page_dict['Items'][row]['Tenant']['Name'] if page_dict['Items'][row]['Tenant'] else '',
            'Term': page_dict['Items'][row]['LeaseTerm']['DisplayValue'] if page_dict['Items'][row][
                'LeaseTerm'] else '',
            'Exp Date': page_dict['Items'][row]['ExpirationDate']['DisplayValue'] if page_dict['Items'][row][
                'ExpirationDate'] else '',
            'Lease Status': page_dict['Items'][row]['LeaseStatus'],
            'Deal Type': page_dict['Items'][row]['DealType'],
            'Move-in Date': page_dict['Items'][row]['MoveInDate']['DisplayValue'] if page_dict['Items'][row][
                'MoveInDate'] else '',
            'Mos on Mrkt': page_dict['Items'][row]['MonthsOnMarket']['DisplayValue'] if page_dict['Items'][row][
                'MonthsOnMarket'] else '',
            'Free Rent': page_dict['Items'][row]['FreeMonths'],
            'Suite': page_dict['Items'][row]['Suite'],
            'Leasing Rep Company': page_dict['Items'][row]['LeasingRepCompany']['Name'] if page_dict['Items'][row][
                'LeasingRepCompany'] else '',
            'Leasing Rep Contact': page_dict['Items'][row]['LeasingRepContact']['Name'] if page_dict['Items'][row][
                'LeasingRepContact'] else '',
            'Submarket': page_dict['Items'][row]['Submarket'],
            'Tenant Rep Contact': page_dict['Items'][row]['TenantRepContact']['Name'] if page_dict['Items'][row][
                'TenantRepContact'] else '',
            'Tenant Rep Company': page_dict['Items'][row]['TenantRepCompany']['Name'] if page_dict['Items'][row][
                'TenantRepCompany'] else '',
            'Lease Comp ID': page_dict['Items'][row]['LeaseCompId'],
            'Verified': page_dict['Items'][row]['IsVerified']['DisplayValue'],
            'Useable SF': page_dict['Items'][row]['UseableArea']['DisplayValue'] if page_dict['Items'][row][
                'UseableArea'] else '',
            'Tenant NAICS': page_dict['Items'][row]['TenantNAICS'],
            'Tenant Contact': page_dict['Items'][row]['TenantContact'],
            'TI Allowance': page_dict['Items'][row]['TenantImprovementAllowanceRate']['DisplayValue'] if
            page_dict['Items'][row]['TenantImprovementAllowanceRate'] else '',
            'SF Office in Unit': page_dict['Items'][row]['OfficeArea']['DisplayValue'] if page_dict['Items'][row][
                'OfficeArea'] else '',
            'Lease Source': page_dict['Items'][row]['LeaseSource']
        }
        df = df.append(row_dict, ignore_index=True)

# print(df)
df.to_csv('final_chicago_sf_6000_max.csv')
