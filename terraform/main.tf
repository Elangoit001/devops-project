provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "devops_vm" {
  ami           = "ami-0c2b8ca1dad447f8a" # Ubuntu 20.04 (update as needed)
  instance_type = "t2.micro"
  key_name      = "your-keypair-name"     # Replace with your actual EC2 key pair name

  tags = {
    Name = "DevOps-Project-VM"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y docker.io",
      "sudo apt install -y openjdk-17-jdk",
      "sudo usermod -aG docker ubuntu",
      "curl -fsSL https://get.jenkins.io/war-stable/2.440/jenkins.war -o jenkins.war",
      "nohup java -jar jenkins.war &"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/your-key.pem") # Adjust path
      host        = self.public_ip
    }
  }
}
