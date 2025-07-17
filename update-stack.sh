#!/bin/bash

# Set variables
STACK_NAME="BONESBootstrap-7951773-625540785621-us-east-1"
TEMPLATE_FILE="/Users/devsmif/dev/AdSales_Frontend_New/src/AdSalesManageAdvertiserSalesforceFrontendCDK/cdk-deploy-change-set-modified.yml"
REGION="us-east-1"

# Create a change set for the stack update
aws cloudformation create-change-set \
  --stack-name $STACK_NAME \
  --change-set-name UpdateStack-$(date +%Y%m%d%H%M%S) \
  --template-body file://$TEMPLATE_FILE \
  --capabilities CAPABILITY_NAMED_IAM \
  --region $REGION 

echo "Change set creation initiated. Check the AWS CloudFormation console to review and execute the change set."

echo "Next steps:"
echo "1. Go to the AWS CloudFormation console"
echo "2. Find the stack named $STACK_NAME"
echo "3. Review and execute the change set"
echo "4. After successful update, run: brazil-build cdk deploy --hotswap Dev-CDKV2"
