variable "ami_id" {
  description = "The AMI ID to use for the instance"
  type        = string
  default = "ami-0a56dba2f7ea83cf0"
}

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
  default     = "g5.2xlarge"
}

variable "hf_token" {
  description = "Hugging Face access token"  
  type = string 
}

# variable "ami_id" {
#   description = "The AMI ID to use for the instance"
#   type        = string
#   default = "ami-0360c520857e3138f"
# }

# variable "instance_type" {
#   description = "The type of instance to use"
#   type        = string
#   default     = "t3.micro"
# }

variable "key_name" {
  description = "The name of the key pair to use for the instance"
  type        = string
  default     = "my-key"
}

variable "ebs_volume_size" {
  description = "Size of the EBS volume in GB"
  type        = number
  default     = 100
}

variable "ami_user" {
  description = "The name of the user for logging into the VM as decided by the AMI."
  type = string 
  default = "ec2-user"
}