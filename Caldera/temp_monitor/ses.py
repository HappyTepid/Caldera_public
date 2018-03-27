import boto3
from botocore.exceptions import ClientError

def public_send_email(subject, message, addresses):
    for recipient_address in addresses:
        SENDER = "Caldera <webmaster@rcvs.org.uk>"

        # Replace recipient@example.com with a "To" address. If your account 
        # is still in the sandbox, this address must be verified.

        AWS_REGION = "eu-west-1"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = (message)
                    
        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>Caldera notification</h1>
        <p>""" + message + """</p>
        </body>
        </html>
        """            

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses',region_name=AWS_REGION)

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient_address,
                    ],
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
                        'Data': subject,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['ResponseMetadata']['RequestId'])
    return
