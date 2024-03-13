output "lambda" {
  value = aws_lambda_function.lambda-demo.invoke_arn
}