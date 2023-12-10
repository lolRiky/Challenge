# Basic Monitoring - Prometheus and Grafana

Visualization and analytics is provided by Grafana, which gets data feeds from Prometheus. Standalone Prometheus in most cases is not enough and needs data producers, e.g. node_exporter. Node exporter provides hardware and OS metrics

How data flows:

System <> data producer <> Prometheus <> Grafana

## ****Prerequisites:****

- Docker
- Docker privileges

## Data Producer

Deploy node_exporter and verify its functionality

```bash
$ docker run -d --network host --name=node_exporter prom/node-exporter
$ curl localhost:9100/metrics
```

## Prometheus

Configure and deploy Prometheus

`job_name` refers to a data producer

Create prometheus.yml file 

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
  - job_name: node
    static_configs:
      - targets: ["localhost:9100"]
```

```bash
docker run -d --network host -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml -v prometheus-data:/prometheus --name=prometheus prom/prometheus
```

Verify Prometheus connected to node_exporter via browser http://IP:9090, select status from menu and targets

# Grafana

Deploy Grafana and verify functionality 

```yaml
$ docker run -d --network grafana --name=grafana grafana/grafana

# Verify grafana is working properly, either through curl or browser
$ curl localhost:3000
```

### Connect Grafana and Prometheus

Navigate to http://localhost:3000, defaults creds are admin:admin

From hamburger menu select connections and search for Prometheus and click Add new data source button.

Fill connection URL and checkbox “Skip TLS certificate validation”

Click “Save & test”

### Basic dashboard

From hamburger menu select Dashboards and import dashboard with following ID: 1860

Default node_exporter dashboard can not bind Root FS on Fedora Server. Locate on imported dashboard “Root FS” and for both panels make sure mountpoint points to “/etc/hostname”

`mountpoint="/etc/hostname"`

### Alerts

From hamburger menu select Alerting → Alert rules and create a new rule

In total they will be 3 rules:

1. Root FS exceeded 50%

Query to retrieve current Root FS usage in percentages

```json
100 - ((avg_over_time(node_filesystem_avail_bytes{instance="localhost:9100",job="node",mountpoint="/etc/hostname",fstype!="rootfs"}[$__rate_interval]) * 100) / avg_over_time(node_filesystem_size_bytes{instance="localhost:9100",job="node",mountpoint="/etc/hostname",fstype!="rootfs"}[$__rate_interval]))
```

In expressions section keep only Threshold and set value to 50

In Set evaluation behavior section create a new alert folder and call it “Alert 15m”

Similarly create Evaluation group call it Alert 15m and put 15m in Interval

Set Pending period to 15m and save alarm

2. Memory usage exceeded 30%

Query to retrieve current memory usage

```json
100 - ((avg_over_time(node_memory_MemAvailable_bytes{instance="localhost:9100",job="node"}[$__rate_interval]) * 100) / avg_over_time(node_memory_MemTotal_bytes{instance="localhost:9100",job="node"}[$__rate_interval]))
```

Follow rest of the steps described in 1. Root FS

3. Load Average 15m exceeded 15%

Query to retrieve current 15m avg

```json
avg_over_time(node_load15{instance="localhost:9100",job="node"}[$__rate_interval]) * 100 / on(instance) group_left sum by (instance)(irate(node_cpu_seconds_total{instance="localhost:9100",job="node"}[$__rate_interval]))
```

Follow rest of the steps described in 1. Root FS but ************************************************************instead of 15 minutes, this alarm desired to 5m************************************************************

### Contact points

When alarm triggers, users/team will be notified on discord

Select Contact points from Alerting page and create a new contact, call it Team A.
For integration select Discord and retrieve Web hook from discord → Server settings → Integrations

In Optional Discord settings, set Title value to `{{ template "default.title" . }}` and Message content to `<@&ROLE_ID> { template "default.message" . }}`

To note, only replace “ROLE_ID” string with discord’s role, keep these characters in text box: < @ & >

### Notification policies

Lastly, from Alerting page select Notification policies and select the default policy and change Default contact point to “Team A” and click “Update default policy”

From this point, webhook should trigger and if there are any firing alarms, Team A should be notified
