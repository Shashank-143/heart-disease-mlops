terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

# Build Docker image
resource "docker_image" "heart_app" {
  name = "heart-disease-mlops:latest"

  build {
    context = "."
    tag     = ["heart-disease-mlops:latest"]
  }
}

# Create application container
resource "docker_container" "heart_app" {
  name  = "heart-disease-app"
  image = docker_image.heart_app.image_id

  ports {
    internal = 8501
    external = 8501
  }

  ports {
    internal = 8000
    external = 8000
  }
}
