output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs where nodes run"
  value       = aws_subnet.private[*].id
}

output "cluster_endpoint" {
  description = "EKS API server endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.main.name
}

output "app_role_arn" {
  description = "IAM role ARN for the app ServiceAccount (IRSA)"
  value       = aws_iam_role.app.arn
}
