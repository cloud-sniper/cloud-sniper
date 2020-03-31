import json
import boto3
import logging
import time
import datetime

log = logging.getLogger()
log.setLevel(logging.INFO)


def cloud_sniper_tagging_ir(event, context):
    
    log.info('AWS API Call via CloudTrail event: ' + str(event))
                                    
    resources = []
                
    try:        
        raw = event['raw']
        event_type = raw['eventName']
        principal = raw['userIdentity']['principalId']
        user_type = raw['userIdentity']['type']
    
        if user_type == 'IAMUser':
            user = raw['userIdentity']['userName']        
        else:
            user = principal.split(':')[1]

        ec2 = boto3.resource('ec2')

        if event_type == 'CreateVolume':
            resources.append(raw['responseElements']['volumeId'])
            log.info(resources)        
        
        elif event_type == 'RunInstances':
            items = raw['responseElements']['instancesSet']['items']
            for item in items:
                resources.append(item['instanceId'])
            log.info(resources)
            log.info('number of instances: ' + str(len(resources)))
        
            base = ec2.instances.filter(InstanceIds=resources)

        elif event_type == 'CreateImage':
            resources.append(raw['responseElements']['imageId'])
            log.info(resources)
        
        elif event_type == 'CreateSnapshot':
            resources.append(raw['responseElements']['snapshotId'])
            log.info(resources)

            for instance in base:
                for vol in instance.volumes.all():
                    resources.append(vol.id)
                for eni in instance.network_interfaces:
                    resources.append(eni.id)
                                                                
        else:
            log.warning('Event type not supported')
        
        if resources:
            for resourceid in resources:
                print('Tagging resource ' + resourceid)
            ec2.create_tags(Resources=resources, Tags=[{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}])
        
        log.info(' Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\\n')
        return True
    
    except Exception as e:
        log.error('Something went wrong: ' + str(e))
        return False
