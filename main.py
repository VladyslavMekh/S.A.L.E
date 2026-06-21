from sale_app import SALEApp

if __name__ == "__main__":
    app = SALEApp("data/logs/logs.usrlog",
                  "stages/second/pipeline_config.json")
    app.run()
