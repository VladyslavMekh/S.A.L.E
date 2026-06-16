from sale_app import SALEApp

if __name__ == "__main__":
    app = SALEApp("/Users/vladyslavmekh/Desktop/S.A.L.E/src/data/logs/s33307.usrlog",
                  "/Users/vladyslavmekh/Desktop/S.A.L.E/src/stages/second/pipeline_config.json")
    app.run()