#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to log messages with timestamp
log() {
  local level=$1
  local message=$2
  local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  
  case $level in
    "INFO")
      echo -e "${GREEN}[INFO]${NC} $timestamp - $message"
      ;;
    "WARN")
      echo -e "${YELLOW}[WARN]${NC} $timestamp - $message"
      ;;
    "ERROR")
      echo -e "${RED}[ERROR]${NC} $timestamp - $message"
      ;;
    *)
      echo "$timestamp - $message"
      ;;
  esac
}

# Function to retry commands with exponential backoff
retry_command() {
  local max_attempts=$1
  local command=$2
  local attempt=1
  local timeout=5
  
  while true; do
    log "INFO" "Attempt $attempt: $command"
    
    # Execute the command
    eval $command && return 0
    
    attempt=$((attempt + 1))
    if [ $attempt -gt $max_attempts ]; then
      log "ERROR" "Command failed after $max_attempts attempts: $command"
      return 1
    fi
    
    log "WARN" "Command failed. Retrying in $timeout seconds..."
    sleep $timeout
    timeout=$((timeout * 2)) # Exponential backoff
  done
}

# Function to deploy to an environment
deploy_to_environment() {
  local profile=$1
  local stack_name=$2
  local options=$3
  
  log "INFO" "Deploying to $profile environment, stack: $stack_name..."
  
  if retry_command 3 "AWS_PROFILE=$profile brazil-build cdk deploy $stack_name $options"; then
    log "INFO" "Successfully deployed to $profile environment"
    return 0
  else
    log "ERROR" "Failed to deploy to $profile environment"
    return 1
  fi
}

# Function to get account ID from profile
get_account_id() {
  local profile=$1
  local account_id
  
  account_id=$(AWS_PROFILE=$profile aws sts get-caller-identity --query "Account" --output text 2>/dev/null)
  if [ $? -eq 0 ]; then
    echo "$account_id"
    return 0
  else
    return 1
  fi
}

# Function to check if CDK is properly installed
check_cdk_installation() {
  if ! command -v brazil-build &> /dev/null; then
    log "ERROR" "brazil-build command not found. Please ensure you have Brazil properly installed."
    return 1
  fi
  
  # Check if CDK is available through brazil-build
  if ! brazil-build cdk --version &> /dev/null; then
    log "ERROR" "CDK is not available through brazil-build. Please check your package dependencies."
    return 1
  fi
  
  return 0
}

# Function to list available stacks
list_stacks() {
  log "INFO" "Listing available CDK stacks..."
  
  local stack_list=$(brazil-build cdk list 2>/dev/null)
  if [ $? -ne 0 ]; then
    log "ERROR" "Failed to list CDK stacks"
    return 1
  fi
  
  echo "$stack_list"
  return 0
}

# Main script execution
main() {
  log "INFO" "Starting CDK deployment to all environments..."
  
  # Check CDK installation
  if ! check_cdk_installation; then
    exit 1
  fi
  
  # List available stacks
  STACKS=$(list_stacks)
  if [ $? -ne 0 ]; then
    exit 1
  fi
  
  echo ""
  log "INFO" "Available stacks:"
  echo "$STACKS"
  echo ""
  
  # Set development account
  if [ -z "$CDK_DEFAULT_ACCOUNT_DEV" ]; then
    DEV_ACCOUNT_ID=$(get_account_id "dev")
    if [ $? -eq 0 ]; then
      export CDK_DEFAULT_ACCOUNT_DEV=$DEV_ACCOUNT_ID
      log "INFO" "Using development account from dev profile: $CDK_DEFAULT_ACCOUNT_DEV"
    else
      log "ERROR" "Failed to get account ID from dev profile"
      log "INFO" "Please set CDK_DEFAULT_ACCOUNT_DEV environment variable manually"
      exit 1
    fi
  else
    log "INFO" "Using development account from environment: $CDK_DEFAULT_ACCOUNT_DEV"
  fi
  
  # Force dev build
  export CDK_FORCE_DEV_BUILD=1
  
  # Ask for confirmation before proceeding
  read -p "Do you want to proceed with deployment to all environments? (y/n): " confirm
  if [[ $confirm != [yY] ]]; then
    log "INFO" "Deployment cancelled by user"
    exit 0
  fi
  
  # Deploy to development environment
  deploy_to_environment "dev" "--all" "--require-approval never"
  dev_deploy_success=$?
  
  # Check if beta profile is available
  if aws configure list --profile beta &>/dev/null; then
    # Ask for confirmation before deploying to beta
    read -p "Do you want to deploy to beta environment? (y/n): " confirm_beta
    if [[ $confirm_beta == [yY] ]]; then
      deploy_to_environment "beta" "--all" "--require-approval never"
      beta_deploy_success=$?
    else
      log "INFO" "Skipping beta deployment as per user request"
      beta_deploy_success=0
    fi
  else
    log "WARN" "Beta profile not configured. Skipping beta deployment."
    beta_deploy_success=0
  fi
  
  # Check if prod profile is available
  if aws configure list --profile prod &>/dev/null; then
    # Ask for confirmation before deploying to production
    read -p "Do you want to deploy to production environment? (y/n): " confirm_prod
    if [[ $confirm_prod == [yY] ]]; then
      # Extra confirmation for production
      read -p "Are you ABSOLUTELY SURE you want to deploy to PRODUCTION? This is not reversible! (yes/no): " confirm_prod_final
      if [[ $confirm_prod_final == "yes" ]]; then
        deploy_to_environment "prod" "--all" "--require-approval never"
        prod_deploy_success=$?
      else
        log "INFO" "Production deployment cancelled"
        prod_deploy_success=0
      fi
    else
      log "INFO" "Skipping production deployment as per user request"
      prod_deploy_success=0
    fi
  else
    log "WARN" "Production profile not configured. Skipping production deployment."
    prod_deploy_success=0
  fi
  
  # Summary
  echo ""
  log "INFO" "Deployment Summary:"
  
  if [ $dev_deploy_success -eq 0 ]; then
    log "INFO" "✅ Development environment deployment: SUCCESS"
  else
    log "ERROR" "❌ Development environment deployment: FAILED"
  fi
  
  if [ $beta_deploy_success -eq 0 ]; then
    if aws configure list --profile beta &>/dev/null; then
      log "INFO" "✅ Beta environment deployment: SUCCESS"
    else
      log "INFO" "➖ Beta environment deployment: SKIPPED (profile not available)"
    fi
  else
    log "ERROR" "❌ Beta environment deployment: FAILED"
  fi
  
  if [ $prod_deploy_success -eq 0 ]; then
    if aws configure list --profile prod &>/dev/null; then
      log "INFO" "✅ Production environment deployment: SUCCESS"
    else
      log "INFO" "➖ Production environment deployment: SKIPPED (profile not available)"
    fi
  else
    log "ERROR" "❌ Production environment deployment: FAILED"
  fi
  
  # Return overall success/failure
  if [ $dev_deploy_success -eq 0 ]; then
    return 0
  else
    return 1
  fi
}

# Run the main function
main
exit $?
