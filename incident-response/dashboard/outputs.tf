output "message" {
  value = "The machine is now available at ${aws_instance.cloudsniper_dashboard.public_ip}."
}

output "public_ip" {
  value = aws_instance.cloudsniper_dashboard.public_ip
}

output "KIBANA_URL" {
  value = "http://${aws_instance.cloudsniper_dashboard.public_ip}:5601"
}