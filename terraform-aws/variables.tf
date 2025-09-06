variable "ami_id" {
  description = "The AMI ID to use for the instance"
  type        = string
  default = "ami-02f32473db05aa9b3"
}

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
  default     = "g5.4xlarge"
}

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