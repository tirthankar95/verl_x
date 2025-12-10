resource "aws_instance" "verl" {
	ami = var.ami_id 
	instance_type = var.instance_type
	key_name = var.key_name
	subnet_id = data.aws_subnets.default.ids[0]
	vpc_security_group_ids = [aws_security_group.allow_ssh.id]
	associate_public_ip_address = true
	provisioner "remote-exec" {
		inline = [
		"export HF_TOKEN=${var.hf_token}",
		"sudo apt-get update",
		"sudo apt-get install -y git",
		"git clone https://github.com/tirthankar95/rlf-small-lm-grid-puzzles",
		"cd rlf-small-lm-grid-puzzles",
		"./setup.sh"
		]
	}

	connection {
		type        = "ssh"
		user        = var.ami_user
		private_key = file("~/my-key.pem")
		host        = self.public_ip
	}

	tags  = {
		Name = "verl-instance"
	}
}

resource "aws_ebs_volume" "verl_disk" {
	availability_zone = aws_instance.verl.availability_zone
	size = var.ebs_volume_size
	type = "gp3"
	tags = {
		Name = "verl-disk"
	}
}

resource "aws_volume_attachment" "verl_attach" {
	volume_id = aws_ebs_volume.verl_disk.id
	instance_id = aws_instance.verl.id 
	force_detach = true 
	device_name = "/dev/sdf"
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
