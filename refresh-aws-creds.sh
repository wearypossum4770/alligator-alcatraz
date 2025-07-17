#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}AWS Credential Refresh Helper${NC}"
echo "This script will help you refresh your expired AWS credentials"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    exit 1
fi

# Check if credentials are expired
echo "Checking current credentials..."
if aws sts get-caller-identity &> /dev/null; then
    echo -e "${GREEN}Your current credentials are valid!${NC}"
else
    echo -e "${YELLOW}Your AWS credentials have expired and need to be refreshed.${NC}"
    
    # Detect credential method
    if grep -q "sso_" ~/.aws/config 2>/dev/null; then
        echo "It looks like you're using AWS SSO."
        echo ""
        echo "Try running: ${GREEN}aws sso login --profile dev${NC}"
        
    elif [ -f ~/.midway/midway-config.json ] || [ -f ~/midway-config.json ]; then
        echo "It looks like you're using Amazon Midway for authentication."
        echo ""
        echo "Try running: ${GREEN}midway auth${NC}"
        
    elif command -v aws-okta &> /dev/null; then
        echo "It looks like you're using aws-okta."
        echo ""
        echo "Try running: ${GREEN}aws-okta login dev${NC}"
        
    else
        echo "Common credential refresh commands:"
        echo "  - AWS SSO: ${GREEN}aws sso login --profile dev${NC}"
        echo "  - Amazon Midway: ${GREEN}midway auth${NC}"
        echo "  - AWS with Okta: ${GREEN}aws-okta login dev${NC}"
        echo "  - AWS with SAML: ${GREEN}saml2aws login${NC}"
        echo ""
        echo "After refreshing credentials, verify with: ${GREEN}aws sts get-caller-identity${NC}"
    fi
fi

echo ""
echo "Available AWS profiles in your configuration:"
grep '^\[' ~/.aws/credentials | tr -d '[]' | sort

echo ""
echo -e "${YELLOW}After refreshing your credentials:${NC}"
echo "1. Run the following command to add Lambda permissions:"
echo -e "${GREEN}aws iam put-role-policy --role-name IibsAdminAccess-DO-NOT-DELETE --policy-name CustomCopyLambdaAccess --policy-document file://lambda-access-policy.json${NC}"
