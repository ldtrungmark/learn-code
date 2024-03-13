resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "null_resource" "build" {
  provisioner "local-exec" {
    command = "/bin/bash ./build.sh"
  }
}

resource "aws_lambda_function" "lambda-demo" {
  filename         = "/home/trungle/learn-code/terraform/demo-deploy-aws-service/lambda-demo/lambda-demo.zip"
  function_name    = "lambda-demo"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "main.handler"
  runtime          = "python3.10"
  environment {
    variables = {
      URL = var.url
    }
  }

  depends_on = [null_resource.build]
}

