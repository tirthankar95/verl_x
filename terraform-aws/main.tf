resource "aws_instance" "verl" {
	ami = var.ami_id 
	instance_type = var.instance_type
	key_name = var.key_name
	eb
	subnet_id = data.aws_subnets.default.ids[0]
	vpc_security_group_ids = [aws_security_group.allow_ssh.id]
	associate_public_ip_address = true

	tags  = {
		Name = "verl-instance"
	}
}

resource "aws_ebs_volume" "data_volume" {
	size = var.ebs_volume_size
	type = "gp3"
}

resource "aws_security_group" "allow_ssh" {
	name = "allow_ssh"
	description = "Allow SSH inbound traffic"
	vpc_id = data.aws_vpc.default.id

	ingress {
		from_port   = 22
		to_port     = 22
		protocol    = "tcp"
		cidr_blocks = ["0.0.0.0/0"]
	}

	egress {
		from_port   = 0
		to_port     = 0
		protocol    = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}

	tags = {
		Name = "allow_ssh_sg"
	}
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
