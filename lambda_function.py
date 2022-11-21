import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    print(event)
    ecr_client = boto3.client("ecr")
    #print(event["detail"]["repository-name"])
    #print(event["detail"]["finding-severity-counts"])
    #print(event["detail"]["finding-severity-counts"]["MEDIUM"])
    #print(event["detail"]["finding-severity-counts"]["LOW"])
    #print(event["detail"]["finding-severity-counts"]["HIGH"])
    #print(event["detail"]["image-tags"])
    ecrRepoName = event["detail"]["repository-name"]
    ecrRepoSeverityCount = event["detail"]["finding-severity-counts"]
    ecrRepoMediumCount = event["detail"]["finding-severity-counts"]["MEDIUM"]
    ecrRepoLowCount = event["detail"]["finding-severity-counts"]["LOW"]
    ecrRepoHighCount = event["detail"]["finding-severity-counts"]["HIGH"]
    body_text1 = "Account ::     086429042168<br>ECR-Repository :: " + ecrRepoName + "<br>ECR Tag ::   "
    if ecrRepoHighCount > 0 or ecrRepoLowCount > 0 or ecrRepoMediumCount > 0:
	    countTags = 0
	    for tags in event["detail"]["image-tags"]:
	    	if countTags == 0:
	    		body_text1 = body_text1 + tags
	    	else: 
	    		body_text1 = body_text1 + ", "+ tags
	    	countTags += 1
	    body_text1 = body_text1 + "<br><br>Image Sevirty Counts"
	    body_text = "<br>High ::   " + str(ecrRepoHighCount) + "<br>Medium ::  " + str(ecrRepoMediumCount) + "<br>Low :: " + str(ecrRepoLowCount)
	    RECIPIENT = ['dhruv.s10@gmail.com', 'dhruvsingh920@gmail.com']
	    if ("my-" in ecrRepoName) or ("mya-" in ecrRepoName) :
	    	RECIPIENT = ['dhruv.s10@gmail.com', 'dhruvsingh920@gmail.com']
	    sendEmail(body_text1, body_text, ecrRepoName, RECIPIENT)
    else : 
    	print("No Severity found in image")

    
def sendEmail(body_text1, body_text, ecrName, RECIPIENT):

	SENDER = "dhruv@dhruvsingh.live"
	AWS_REGION = "us-east-1"
	# Specify a configuration set. If you do not want to use a configuration
	# set, comment the following variable, and the 
	# ConfigurationSetName=CONFIGURATION_SET argument below.
	CONFIGURATION_SET = "ConfigSet"
	# The subject line for the email.
	SUBJECT = "ECR image scan complete for ECR repo: " + ecrName + " in 086429042168 account"
	# The email body for recipients with non-HTML email clients.
	BODY_TEXT = ("Please find the details about the ECR repository image severity.\r\n"
	             "Environment --> UAT \r\n"
	             +body_text1 + body_text
	            )
	            
	# The HTML body of the email.
	BODY_HTML = """<html>
	<head></head>
	<body>
	  <h3>ECR Image Sacn in UAT account.</h3>
	  <p>Please find following details ... 
	  </p>
	  <br>{body_text1}{body_text}</p><br>
	</body>
	</html>
	            """.format(body_text1=body_text1, body_text=body_text)          

	CHARSET = "UTF-8"
	client = boto3.client('ses',region_name=AWS_REGION)
	
	# Try to send the email.
	try:
	    #Provide the contents of the email.
	    response = client.send_email(
	        Destination={
	            'ToAddresses': RECIPIENT,
	        },
	        Message={
	            'Body': {
	                'Html': {
	                    'Charset': CHARSET,
	                    'Data': BODY_HTML,
	                },
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
	        # If you are not using a configuration set, comment or delete the
	        # following line
	        #ConfigurationSetName=CONFIGURATION_SET,
	    )
	# Display an error if something goes wrong.	
	except ClientError as e:
	    print(e.response['Error']['Message'])
	else:
	    print("Email sent! Message ID:"),
	    print(response['MessageId'])
