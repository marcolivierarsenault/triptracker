import boto3
from botocore.vendored import requests
import datetime
import json
from decimal import Decimal
from botocore.exceptions import ClientError
from io import StringIO
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('trip_price')

SENDER = "Marc-Olivier Arsenault <marcolivier.arsenault@gmail.com>"
RECIPIENT = "marcolivier.arsenault@gmail.com"
AWS_REGION = "us-east-1"
CHARSET = "UTF-8"

def lambda_handler(event, context):
    
    url = 'https://voyagesarabais.com/recherche-sud/getpricedetails?search%5Bgateway%5D=YUL&search%5BdateDep%5D=2019-12-15&search%5Bduration%5D=7day%2C8day&search%5BdestDep%5D=o&search%5BnoHotel%5D=p7&search%5Broom1%5D=a%3A4%3A%7Bi%3A0%3Bs%3A2%3A%2240%22%3Bi%3A1%3Bs%3A2%3A%2240%22%3Bi%3A2%3Bs%3A1%3A%223%22%3Bi%3A3%3Bs%3A1%3A%221%22%3B%7D&search%5Broom2%5D=&search%5Broom3%5D=&search%5Broom4%5D=&search%5Broom5%5D=&search%5Broom6%5D=&search%5Bflex%5D=N&search%5Bflexhigh%5D=3&search%5Bflexlow%5D=3&search%5Broomcallgroup%5D=%5B%7B%22_priority%22%3A9%2C%22nb_rooms%22%3A1%2C%22nb_adults%22%3A2%2C%22non_adults%22%3A%5B%223%22%2C%221%22%5D%7D%5D&search%5Bpricemax%5D=9000&search%5Bpricemin%5D=1&search%5Ballinclusive%5D=Y&search%5Bbeach%5D=&search%5Bcasino%5D=&search%5Bfamily%5D=&search%5Bgolf%5D=&search%5Bkitchenette%5D=&search%5Boceanview%5D=&search%5Bminiclub%5D=&search%5Bspa%5D=&search%5Bwedding%5D=&search%5Badultonly%5D=&search%5Bnoextrasingle%5D=&search%5Bvilla%5D=&search%5Bstar%5D=4.5&search%5Bstarmax%5D=4.5&search%5Bdirectflight%5D=&search%5Btourtodisplay%5D=CAH%2CVAT%2CVAC%2CVAX%2CSGN%2CSQV%2CSWG%2CWJV&search%5Buuid%5D=&search%5BnbRoomsMax%5D=&search%5BhotelDistanceMax%5D='

    payload = 'data=QXjaDVS1EqNQAPyXaymCS4l7cL1cAQQn8ILD11%2F6ndlZ%2FfMX%2FufEXTaHeV6sCyracChEFTl8XHzw9NfD8TjxcBJOrgXgabDpEkZOeyGaNsfYlfsXoxaj57LBWgZjpB2mpeDKsJ0iUmI5VVjv9eCeA34db0A8ASRklG9DJjZAVk8j%2BK58ctfscX7FxXppW62OhAMznyYwpeGqU9FoU%2F71SDiO7fk5Dz99S3CAd5RDB9lKTvzmSahBld5gdaz9vfedPConEhM4dpuBiIxpZ6fKZK7O1BDnBvU9Ba%2FHZJXiRNuFCNhRlvZh1lH4WrciCbh5GUW8r4vsjq6xDRJzTvsb3EGJM%2BplJMNkBcma09TrMezjOqFNtOCZ3EHBE8rwpbzA%2Bnp43SKN3No4fVcGdg1hSW1er0e8zHKV7qNEleUPVGcJ4YniN6lPWIA%2BfixcisbTUpO8HgR78ue3i0dZlwJXGyhYhxfWoz5wCrQL5JbnZadk2pILWEdT4RKiXbKcxemTi4mF7paMniWP190lJHXy8eZgV7QqaTnvx%2BwQYGNWsd5jPomwNojiNgn3zh%2B1E2XIxO7ri%2FfN7PXIehG2oplT9oHbTGqkNtPKtiQq9UsjliPEktUIbyc0%2Be8RqapxzPExGO%2BP8Qts0dbCnm7UJ3A15plV51xQq1Y6d07xJjZ4BhGiIHKw9uosLjWpHmidnaEsg%2Fle4JjPGvaZT3tgFAS6cjix2u53EIB4JwwyuGLJSxGCYa8HTz7Tm8WL741X0NfeAcIkpt6ssUJHChKkaf96kAMEG0PDxHs%2B7wDQs%2F2FQgVRsDful59Uhdw7UAWKp4yiQU25FNUlpGoG%2F1nlZGD7lDW2fb7RviM%2FQjpny6Hcxmd6JoeYuHtGOa6VdW3dcMVAxir5FXtwqb2fog0PfNydAw9EuBQwiAbzivCMaLJTr2f%2BXt4SMOadF6fZ29rn66FBIYemXUNzpHDqUoX4FlcaXO9ucgZAisAS66Mbh5xeEK7V0r33Z8oMzAnFHUeen8hoDtq2ahi3JY%2FQC5DqhEiB0eRNkC7bGPaGKXIAoq%2F1ToN4sHN8BpgKd56efidkDlK%2FyJtTid7itoGQUcLMrT0feaY455Znrfb28az3t9C8B9k63ya8BRcaX3QMkDIvsQHxciv33ROC4cA3WhqqcuUkPxRSuz9xACrzlEvXLM4QP0qBFEOvB7qeKyBXqppLE1DFLEPhc0zRyiWY30YwlgSpcQhzmmifBd8wXgLAYpouOFpYn%2BTqDEweseIKO3G2c3gbFJC5yOPGgTVLBsG7KYk%2BkCJpEW984kihzE6lTENZ32CHseFA%2FXCTZUG5FZ3M12VmtH2hKXC1IZ2UAQ4foyB1Qdi35QQJv9Ef235UyPN4c%2FeOeKR9eIlGlL9GiWhogoOEpUnE%2BDdTnKQXFWwgRRHGNXaonLog6ZNhoLCluUWOc8j6a%2BZ793ZojmWm39gkBnx0YWPFstDXoQSkIsIlwr4oN%2F8%2BhfU6N%2F%2Bd0J%2F%2Fb5zoDz0%3D&type=packageplus'

    headers = {
    'Cookie': 'Cookie: _gcl_au=1.1.596656575.1560126807; _ga=GA1.2.1347033583.1560126807; _fbp=fb.1.1560126807161.1014257493; _gaexp=GAX1.2.NFE8cllqRy-hy2p_zsZ_9A.18143.0; G_ENABLED_IDPS=google; is_all_inclusive_checked=1; PHPSESSID=0odjk0bsqoalhh20ijg3hgcqs2; _hjid=d29cb0cd-017e-4453-a112-b8ae863dbb89; _gid=GA1.2.1378798265.1565464684; _gac_UA-6397631-1=1.1565464692.CjwKCAjw1rnqBRAAEiwAr29II9bpU1twn6ZPzisvGTap3gofl973SwBnRO6CkYdpJF4F3qEYN9FTDBoCPRwQAvD_BwE; _gat_UA-6397631-1=1',
    'Origin': 'https://voyagesarabais.com',
    'Accept-Encoding': 'gzip, deflate, br' ,
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8' ,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36' ,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' ,
    'Accept': '*/*' ,
    'Referer': 'https://voyagesarabais.com/recherche-sud?gateway=YUL&dateDep=2019-12-15&duration=7day,8day&destDep=o&noHotel=p7&allinclusive=Y&beach=&casino=&family=&golf=&kitchenette=&oceanview=&miniclub=&spa=&weeding=&adultonly=&noextrasingle=&villa=&directflight=&tourtodisplay=CAH,VAT,VAC,VAX,SGN,SQV,SWG,WJV&uuid=&nbRoomsMax=&hotelDistanceMax=&star=4.5&starmax=4.5&pricemin=1&pricemax=9000&flex=N&&bedrooms[0][0]=40&bedrooms[0][1]=40&bedrooms[0][2]=3&bedrooms[0][3]=1',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive' 
    }

    r = requests.post(url, data=payload, headers=headers)
    rr = json.loads(r.text)
    
    #We sometime get cookies denied, so we have to update the data and cookies above.
    if 'totalprice' not in rr.keys():

        SUBJECT = "Voyage en Rabais - DATA UNAVAILABLE"
        BODY_TEXT = ( "Update the key bastard!")
        
        
        
        client = boto3.client('ses',region_name=AWS_REGION)
        
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        
        return(-1)
    
    #get pricing
    totalPrice = rr['totalprice']
    dd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #load it into dynamodb
    table.put_item(
    Item={
        'time': dd,
        'total_price': Decimal(round(totalPrice, 2))
        })
    
    
    # Store it into a S3 file
    string = 'time,total_price\n{},{}'.format(dd, Decimal(round(totalPrice, 2)))
    encoded_string = string.encode("utf-8")

    bucket_name = "trip-price"
    file_name = datetime.datetime.now().strftime('%s')+'.csv'
    
    s3_path = "data/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    
    # If price goes below 4000 I want a mail
    if Decimal(round(totalPrice, 2)) < 4000:
        
        SUBJECT = "Voyage en Rabais !!"
        BODY_TEXT = ( "Le prix du voyage est de: " + str(int(totalPrice)) + "$")

        # Create a new SES resource and specify a region.
        client = boto3.client('ses',region_name=AWS_REGION)
        
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    return str(Decimal(totalPrice))