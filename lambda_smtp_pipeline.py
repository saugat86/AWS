print('Loading event')
import json
import boto3
import json
import uuid
import datetime
from boto3.dynamodb.conditions import Key

sns = boto3.client('sns')
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SMTPDeliveryNotifications')

def lambda_handler(event, context):
 
 print(json.dumps(event, separators=(',', ':')))
 
 SnsPublishTime = event['Records'][0]['Sns']['Timestamp'].split("T")[0]
 print(SnsPublishTime)
 time = event['Records'][0]['Sns']['Timestamp'][0:-5]
 time2 = time.replace("T"," ")
 print(time2)
 #SnsPublishTime = event['Records'][0]['Sns']['Timestamp']
 SESMessage = event['Records'][0]['Sns']['Message'] 
 SESMessage1 = json.loads(SESMessage)
 
 SESMessageType = SESMessage1['notificationType']
 SESMessageId = SESMessage1['mail']['messageId']
 SESSenderAddress=SESMessage1['mail']['source']
 SESDestinationAddress = SESMessage1['mail']['destination'][0]
 
 print(SESDestinationAddress)
 # resp = table.query(IndexName="record_status-RecordNumber-index",
 # KeyConditionExpression=Key('record_status').eq('ok'),
 # ScanIndexForward=False,
 # Limit=1
 # )
 # #print('Response:' + json.dumps(resp))
 # record_number = resp['Items'][0]['RecordNumber']
 # print('RecordNumber:' + str(record_number))
 # new_record_number = record_number + 1
 
 if SESMessageType == 'Delivery':
 
 sourceIp = SESMessage1['mail']['sourceIp']
 
 try:
 sub = SESMessage1['mail']['commonHeaders']['subject']
 print(sub)
 except:
 print('not found')
 sub = ' '
 
 subject = sub
 
 smtpres = SESMessage1['delivery']['smtpResponse'][:10]
 
 try:
 
 timelog = mail['commonHeaders']['date'][16:25]
 print(timelog)
 except:
 print('not found')
 timelog = ' '
 
 Date = timelog 
 
 #Date = SESMessage1['mail']['commonHeaders']['date'][16:25]
 #print(Date)
 #print(subject)
 
 b = {
 
 'SESMessageId':SESMessageId,
 'SnsPublishTime':SnsPublishTime,
 'SESSenderAddress':SESSenderAddress,
 'SESDestinationAddress':SESDestinationAddress, 
 'SESMessageType': SESMessageType,
 'SourceIP':sourceIp,
 'Subject':subject,
 'SMTPresponse':smtpres,
 'Time':Date
 
 }
 try:
 response = table.put_item(Item=b)
 print('data inserted for delivery')
 
 except Exception as e:
 print(e)
 # work on python 2.x
 #logger.error('Failed to upload to ftp: '+ str(e))
 
 
 
 elif SESMessageType == 'Bounce':
 bouncetype = SESMessage1['bounce']['bounceType']
 bouncesubtype = SESMessage1['bounce']['bounceSubType']
 sourceIp = SESMessage1['mail']['sourceIp']
 smtpresp = SESMessage1['bounce']['bouncedRecipients'][0]['diagnosticCode'][:10]
 
 try:
 BDate = SESMessage1['mail']['commonHeaders']['date'][16:26]
 except:
 print('not found')
 BDate = ''
 
 print(bouncetype)
 
 if (bouncetype == "Permanent" and bouncesubtype == "General"):
 b = {'SESMessageId':SESMessageId,
 'SnsPublishTime':SnsPublishTime,
 'SESSenderAddress':SESSenderAddress,
 'SESDestinationAddress':SESDestinationAddress, 
 'SESMessageType': SESMessageType,
 'bounceType': bouncetype,
 'bounceSubType': bouncesubtype,
 'Which Bounce?' : 'Hard Bounce',
 'sourceIP':sourceIp,
 'SMTPresponse':smtpresp,
 'BDate':BDate
 
 }
 try:
 response = table.put_item(TableName='SMTPBounceNotifications',Item=b)
 print('data inserted for bounce')
 except :
 print('Error in bounce')
 
 elif (bouncetype == "Permanent" and bouncesubtype == "NoEmail"):
 b = {'SESMessageId':SESMessageId,
 'SnsPublishTime':SnsPublishTime,
 'SESSenderAddress':SESSenderAddress,
 'SESDestinationAddress':SESDestinationAddress, 
 'SESMessageType': SESMessageType,
 'bounceType': bouncetype,
 'bounceSubType': bouncesubtype,
 'Which Bounce?' : 'Hard Bounce',
 'sourceIP':sourceIp,
 'SMTPresponse':smtpresp,
 'BDate':BDate
 }
 
 try:
 response = table.put_item(TableName='SMTPBounceNotifications',Item=b)
 print('data inserted for bounce')
 except :
 print('Error in bounce') 
 
 else:
 b = {'SESMessageId':SESMessageId,
 'SnsPublishTime':SnsPublishTime,
 'SESSenderAddress':SESSenderAddress,
 'SESDestinationAddress':SESDestinationAddress, 
 'SESMessageType': SESMessageType,
 'bounceType': bouncetype,
 'bounceSubType': bouncesubtype,
 'Which Bounce?' : 'Soft Bounce',
 'sourceIP':sourceIp,
 'SMTPresponse':smtpresp,
 'BDate':BDate
 }
 try:
 response = table.put_item(TableName='SMTPBounceNotifications',Item=b)
 print('data inserted for bounce')
 except :
 print('Error in bounce')
 
 
 elif SESMessageType == 'Complaint':
 b = {'SESMessageId':SESMessageId,
 'SnsPublishTime':SnsPublishTime,
 'SESSenderAddress':SESSenderAddress,
 'SESDestinationAddress':SESDestinationAddress, 
 'SESMessageType': SESMessageType}
 try:
 response = table.put_item(TableName='SMTPComplaintNotifications',Item=b)
 print('data inserted for Complaint')
 except :
 print('Error in Complaint')