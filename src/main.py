from sale_app import SALEApp

if __name__ == "__main__":
    app = SALEApp("src/data/logs/logs.usrlog",
                  "src/stages/second/pipeline_config.json")
    app.run()
