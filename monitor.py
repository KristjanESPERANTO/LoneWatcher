import psutil
import requests
import subprocess
import time
import tomllib


with open("config.toml", "rb") as file:
    config = tomllib.load(file)

    initial_minimize_delay = config["timer"]["initial_minimize_delay"]
    status_check_interval = config["timer"]["status_check_interval"]
    all_green_interval = config["timer"]["all_green_interval"]
    alert_interval = config["timer"]["alert_interval"]


def monitor_system(monitoring_targets, gui_instance, logging):
    first_iteration = True
    while True:
        for target in monitoring_targets:
            success = check_target(target)
            target["status"] = success
            if not success:
                logging.error(
                    "check failed: %s %s %s",
                    target["type"],
                    target["name"],
                    target["address"],
                )
                gui_instance.update_status(target, False)
            else:
                gui_instance.update_status(target, True)

            statuses = [t.get("status") for t in monitoring_targets]
            if False in statuses:
                if gui_instance.root.cget("bg") != "red":
                    gui_instance.root.bell()
                    gui_instance.root.configure(bg="red")
                    gui_instance.root.attributes("-topmost", True)
                    gui_instance.root.deiconify()

            elif all(statuses):
                gui_instance.root.configure(bg="green")
                gui_instance.root.attributes("-topmost", False)
                print(first_iteration)
                if first_iteration:
                    time.sleep(initial_minimize_delay)
                    gui_instance.root.iconify()
                first_iteration = False
            else:
                gui_instance.root.configure(bg="grey")
                gui_instance.root.attributes("-topmost", False)
            time.sleep(status_check_interval)

        # Only check every minute if all is green, else check four time a minute
        if all(statuses):
            time.sleep(all_green_interval)
        else:
            time.sleep(alert_interval)


def check_target(target):
    if target["type"] == "ping":
        return check_ip(target["address"])
    elif target["type"] == "http":
        return check_website(target["address"])
    elif target["type"] == "service":
        return check_service(target["address"])
    else:
        return False


def check_ip(ip):
    """Checks if an IP address responds to ping."""
    if psutil.WINDOWS:
        params = ["ping", "-n", "1", ip]
        creation_flags = subprocess.CREATE_NO_WINDOW
    else:
        params = ["ping", "-c", "1", "-W", "2", ip]
        creation_flags = 0

    result = subprocess.run(
        params,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creation_flags,
        check=False,
    )

    output = str(result.stdout).lower()

    return "ttl" in output


def check_service(service_name):
    """Checks if the service is running."""
    if psutil.WINDOWS:
        for service in psutil.win_service_iter():
            if service.name() == service_name:
                return service.status() == "running"
    else:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.stdout.strip() == "active"
        except subprocess.CalledProcessError:
            return False
    return False


def check_website(url):
    """Checks if the website is accessible."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, timeout=5, headers=headers, verify=False)
        return response.status_code in [200, 301, 302]
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False
