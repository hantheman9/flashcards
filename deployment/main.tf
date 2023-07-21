
provider "google-beta" {
    credentials = "XX"
    project     = "articulate-life-393421"
    region = "us-central1"
}

resource "google_project_service" "cloudrun_api" {
  project            =   "articulate-life-393421"
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_compute_network" "default" {
  provider = google-beta
  name     = "be-static-ip-network"
}

resource "google_compute_subnetwork" "default" {
  provider      = google-beta
  name          = "be-static-ip"
  ip_cidr_range = "XX"
  network       = google_compute_network.default.id
  region        = "us-central1"
}

resource "google_project_service" "vpc" {
  provider           = google-beta
  service            = "vpcaccess.googleapis.com"
  disable_on_destroy = false
}

resource "google_vpc_access_connector" "default" {
  provider = google-beta
  name     = "be-conn"
  region   = "us-central1"

  subnet {
    name = google_compute_subnetwork.default.name
  }

  depends_on = [
    google_project_service.vpc
  ]
}

resource "google_compute_router" "default" {
  provider = google-beta
  name     = "be-static-ip-router"
  network  = google_compute_network.default.name
  region   = google_compute_subnetwork.default.region
}

resource "google_compute_address" "default" {
  provider = google-beta
  name     = "be-static-ip-addr"
  region   = google_compute_subnetwork.default.region
}

resource "google_compute_router_nat" "default" {
  provider = google-beta
  name     = "be-static-nat"
  router   = google_compute_router.default.name
  region   = google_compute_subnetwork.default.region

  nat_ip_allocate_option = "MANUAL_ONLY"
  nat_ips                = [google_compute_address.default.self_link]

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  subnetwork {
    name                    = google_compute_subnetwork.default.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

resource "google_cloud_run_v2_service" "default" {
  provider = google-beta
  name     = "be-static-ip-service"
  location = google_compute_subnetwork.default.region

  template {
    containers {
      image = "XXX"
    }
    scaling {
      max_instance_count = 5
    }
    vpc_access {
      connector = google_vpc_access_connector.default.id
      egress    = "ALL_TRAFFIC"
    }
  }
  ingress = "INGRESS_TRAFFIC_ALL"

  lifecycle {
    ignore_changes = [
      ingress, template[0].vpc_access
    ]
  }
}
