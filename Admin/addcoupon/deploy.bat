sam build -t template.yml
sam package --output-template-file packaged.yaml --s3-bucket booxwoox-lambdas
sam deploy --template-file packaged.yaml --region ap-south-1 --capabilities CAPABILITY_IAM --stack-name Addcoupon
