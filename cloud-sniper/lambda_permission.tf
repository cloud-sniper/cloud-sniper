resource "aws_lambda_permission" "aws_lambda_permission_cloud_sniper" {
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda_function_cloud_sniper.function_name}"
  principal     = "events.amazonaws.com"
}

resource "aws_lambda_permission" "lambda_function_cloud_sniper_tagging" {
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda_function_cloud_sniper_tagging_ir.function_name}"
  principal     = "events.amazonaws.com"
}
