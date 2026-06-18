from sale_app import SALEApp

if __name__ == "__main__":
    app = SALEApp("src/data/logs/s33307.usrlog",
                  "src/stages/second/pipeline_config.json")
    app.run()